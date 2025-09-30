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


@api_routes.route('/api/delete_drink_log/<int:log_id>', methods=['DELETE'])
@login_required
def delete_drink_log(log_id):
    try:
        # Delete the drink log only if it belongs to the current user
        result = ControllerDrinkLogs.delete_drink_log_by_user(log_id, current_user.user_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': f'Drink log {log_id} deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Drink log not found or unauthorized'
            }), 404
            
    except Exception as e:
        Log.error("Error in delete_drink_log route", err=e, sys=sys)
        return jsonify({
            'success': False,
            'message': 'An error occurred while deleting the drink log'
        }), 500


@api_routes.route('/api/drinks', methods=['GET'])
@login_required
def get_drinks():
    """Get all drinks"""
    try:
        drinks = ControllerDrinks.get_drinks()
        drinks_data = [drink.serialize() for drink in drinks]
        
        return jsonify({
            'success': True,
            'drinks': drinks_data
        }), 200
        
    except Exception as e:
        Log.error("Error in get_drinks route", err=e, sys=sys)
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching drinks'
        }), 500


@api_routes.route('/api/drinks', methods=['POST'])
@login_required
def create_drink():
    """Create a new drink"""
    try:
        data = request.get_json()
        Log.info(f"Creating drink with data: {data}")
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data received'
            }), 400
        
        # Extract and validate data
        drink_name = data.get('drink_name', '').strip()
        drink_water_percentage = data.get('drink_water_percentage', 100)
        drink_alcohol_percentage = data.get('drink_alcohol_percentage', 0)
        drink_image = data.get('drink_image', '').strip()
        
        if not drink_name:
            return jsonify({
                'success': False,
                'message': 'Drink name is required'
            }), 400
        
        # Convert percentages to integers
        try:
            drink_water_percentage = int(drink_water_percentage)
            drink_alcohol_percentage = int(drink_alcohol_percentage)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Percentages must be valid numbers'
            }), 400
        
        # Validate percentages
        if not (0 <= drink_water_percentage <= 100) or not (0 <= drink_alcohol_percentage <= 100):
            return jsonify({
                'success': False,
                'message': 'Percentages must be between 0 and 100'
            }), 400
        
        if drink_water_percentage + drink_alcohol_percentage > 100:
            return jsonify({
                'success': False,
                'message': 'Water + alcohol percentages cannot exceed 100%'
            }), 400
        
        # Check if drink already exists
        existing_drink = ControllerDrinks.get_drink_name(drink_name)
        if existing_drink:
            return jsonify({
                'success': False,
                'message': f'Drink "{drink_name}" already exists'
            }), 409
        
        # Create drink data
        drink_data = {
            'drink_name': drink_name,
            'drink_water_percentage': drink_water_percentage,
            'drink_alcohol_percentage': drink_alcohol_percentage,
            'drink_image': drink_image if drink_image else None
        }
        
        # Save to database
        result = ControllerDrinks.add_drink(drink_data)
        
        if result:
            return jsonify({
                'success': True,
                'message': f'Drink "{drink_name}" created successfully',
                'drink': result.serialize()
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create drink'
            }), 500
            
    except Exception as e:
        Log.error("Error in create_drink route", err=e, sys=sys)
        return jsonify({
            'success': False,
            'message': 'An error occurred while creating the drink'
        }), 500


@api_routes.route('/api/drinks/<int:drink_id>', methods=['PUT'])
@login_required
def update_drink(drink_id):
    """Update an existing drink"""
    try:
        data = request.get_json()
        Log.info(f"Updating drink {drink_id} with data: {data}")
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data received'
            }), 400
        
        # Check if drink exists
        drink = ControllerDrinks.get_drink(drink_id)
        if not drink:
            return jsonify({
                'success': False,
                'message': 'Drink not found'
            }), 404
        
        # Extract and validate data
        drink_name = data.get('drink_name', drink.drink_name).strip()
        drink_water_percentage = data.get('drink_water_percentage', drink.drink_water_percentage)
        drink_alcohol_percentage = data.get('drink_alcohol_percentage', drink.drink_alcohol_percentage)
        drink_image = data.get('drink_image', drink.drink_image)
        
        if not drink_name:
            return jsonify({
                'success': False,
                'message': 'Drink name is required'
            }), 400
        
        # Convert percentages to integers
        try:
            drink_water_percentage = int(drink_water_percentage)
            drink_alcohol_percentage = int(drink_alcohol_percentage)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Percentages must be valid numbers'
            }), 400
        
        # Validate percentages
        if not (0 <= drink_water_percentage <= 100) or not (0 <= drink_alcohol_percentage <= 100):
            return jsonify({
                'success': False,
                'message': 'Percentages must be between 0 and 100'
            }), 400
        
        if drink_water_percentage + drink_alcohol_percentage > 100:
            return jsonify({
                'success': False,
                'message': 'Water + alcohol percentages cannot exceed 100%'
            }), 400
        
        # Check if new name conflicts with existing drink (excluding current drink)
        if drink_name != drink.drink_name:
            existing_drink = ControllerDrinks.get_drink_name(drink_name)
            if existing_drink:
                return jsonify({
                    'success': False,
                    'message': f'Another drink with name "{drink_name}" already exists'
                }), 409
        
        # Update drink
        drink.drink_name = drink_name
        drink.drink_water_percentage = drink_water_percentage
        drink.drink_alcohol_percentage = drink_alcohol_percentage
        drink.drink_image = drink_image if drink_image else None
        
        from .models import db
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Drink "{drink_name}" updated successfully',
            'drink': drink.serialize()
        }), 200
        
    except Exception as e:
        Log.error("Error in update_drink route", err=e, sys=sys)
        from .models import db
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while updating the drink'
        }), 500


@api_routes.route('/api/drinks/<int:drink_id>', methods=['DELETE'])
@login_required
def delete_drink(drink_id):
    """Delete a drink"""
    try:
        # Check if drink exists
        drink = ControllerDrinks.get_drink(drink_id)
        if not drink:
            return jsonify({
                'success': False,
                'message': 'Drink not found'
            }), 404
        
        # Check if drink is being used in drink logs
        from .models import DrinkLog
        logs_count = DrinkLog.query.filter_by(drink_id=drink_id).count()
        if logs_count > 0:
            return jsonify({
                'success': False,
                'message': f'Cannot delete drink "{drink.drink_name}" because it has {logs_count} log entries. Delete the logs first.'
            }), 409
        
        # Delete the drink
        drink_name = drink.drink_name
        ControllerDrinks.delete_drink(drink_id)
        
        return jsonify({
            'success': True,
            'message': f'Drink "{drink_name}" deleted successfully'
        }), 200
        
    except Exception as e:
        Log.error("Error in delete_drink route", err=e, sys=sys)
        return jsonify({
            'success': False,
            'message': 'An error occurred while deleting the drink'
        }), 500