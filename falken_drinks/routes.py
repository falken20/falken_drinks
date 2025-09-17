from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import sys

from .controllers import ControllerDrinks, ControllerDrinkLogs
from .logger import Log


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/add_drink', methods=['POST'])
@login_required
def add_drink():
    try:
        data = request.get_json()
        Log.info(f"Received data: {data}")
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data received'
            }), 400
        
        # Extract data from request
        drink_name = data.get('drink_name')
        drink_total_quantity = data.get('amount', 0)
        alcohol_percentage = data.get('alcohol_percentage', 0)
        
        Log.info(f"Processing drink: {drink_name}, amount: {drink_total_quantity}, alcohol: {alcohol_percentage}")
        
        # Validate and convert data types
        try:
            drink_total_quantity = int(drink_total_quantity)
            alcohol_percentage = float(alcohol_percentage)
            drink_total_quantity = int(drink_total_quantity)
        except (ValueError, TypeError) as e:
            Log.error(f"Data type conversion error: {e}")
            return jsonify({
                'success': False,
                'message': f'Invalid data types: {str(e)}'
            }), 400
        
        if not drink_name or drink_total_quantity <= 0:
            return jsonify({
                'success': False,
                'message': 'Invalid drink name or amount'
            }), 400
        
        # Get or create drink
        drink = ControllerDrinks.get_or_create_drink(drink_name, alcohol_percentage, drink_total_quantity)
        if not drink:
            return jsonify({
                'success': False,
                'message': 'Failed to create or find drink'
            }), 500
        
        # Calculate quantities based on drink percentages
        drink_water_quantity = int((drink.drink_water_percentage / 100) * drink_total_quantity)
        drink_alcohol_quantity = int((drink.drink_alcohol_percentage / 100) * drink_total_quantity)
        
        # Prepare drink log data
        drink_log_data = {
            'drink_id': drink.drink_id,
            'user_id': current_user.user_id,
            'drink_total_quantity': drink_total_quantity,
            'drink_water_quantity': drink_water_quantity,
            'drink_alcohol_quantity': drink_alcohol_quantity
        }
        
        # Save to database using the controller method
        result = ControllerDrinkLogs.add_drink_log(drink_log_data)
        
        if result:
            return jsonify({
                'success': True,
                'message': f'Added {drink_total_quantity}ml of {drink_name}',
                'log_id': result.log_id
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save drink log'
            }), 500
            
    except Exception as e:
        Log.error("Error in add_drink route", err=e, sys=sys)
        return jsonify({
            'success': False,
            'message': 'An error occurred while saving the drink'
        }), 500
