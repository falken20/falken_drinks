# by Richi Rod AKA @richionline / falken20
from datetime import date
# import pprint
import sys

from .models import db, Drink, DrinkLog, User
from .logger import Log
from .config import shorten_url

Log.info("***** Loading controllers.py")

# The CRUD operations use to return a JSON response:
# return jsonify(response)


class ControllerUser:
    def __init__(self):
        pass

    @staticmethod
    def get_user(id: int):
        try:
            Log.info(
                f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
            return User.query.filter_by(id=id).first()
        except Exception as e:
            Log.error("Error in ControllerUser.get_user", err=e, sys=sys)
            return None

    @staticmethod
    def get_user_email(email: str):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_name(name: str):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return User.query.filter_by(name=name).first()

    @staticmethod
    def delete_user(id: int) -> None:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        User.query.filter_by(id=id).delete()
        db.session.commit()


class ControllerDrinks:
    def __init__(self):
        pass

    @staticmethod
    def get_drink(id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Drink.query.filter_by(id=id).first()

    @staticmethod
    def get_drink_name(name: str):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Drink.query.filter_by(drink_name=name).first()

    @staticmethod
    def get_or_create_drink(drink_name: str, alcohol_percentage: float = 0, drink_total_quantity: int = 0):
        """Get existing drink or create new one if it doesn't exist"""
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        try:
            # Try to find existing drink
            drink = Drink.query.filter_by(drink_name=drink_name).first()
            
            if not drink:
                # Create new drink if it doesn't exist
                water_percentage = 100 - alcohol_percentage
                drink_data = {
                    'drink_name': drink_name,
                    'drink_water_percentage': int(water_percentage),
                    'drink_alcohol_percentage': int(alcohol_percentage)
                }
                drink = ControllerDrinks.add_drink(drink_data)
            
            return drink
        except Exception as e:
            Log.error("Error in ControllerDrinks.get_or_create_drink", err=e, sys=sys)
            return None

    @staticmethod
    def get_drinks():
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Drink.query.all()
    
    @staticmethod
    def add_drink(drink_data: dict):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        try:
            new_drink = Drink(**drink_data)
            db.session.add(new_drink)
            db.session.commit()
            return new_drink
        except Exception as e:
            Log.error("Error in ControllerDrinks.add_drink", err=e, sys=sys)
            db.session.rollback()
            return None

    @staticmethod
    def delete_drink(id: int) -> None:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        Drink.query.filter_by(id=id).delete()
        db.session.commit()


class ControllerDrinkLogs:
    def __init__(self):
        pass

    @staticmethod
    def get_drink_log(id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return DrinkLog.query.filter_by(id=id).first()

    @staticmethod
    def get_drink_logs():
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return DrinkLog.query.all()

    @staticmethod
    def add_drink_log(drink_log_data: dict):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        Log.debug(f"drink_log_data: {drink_log_data}")

        try:
            new_drink_log = DrinkLog(**drink_log_data)
            db.session.add(new_drink_log)
            db.session.commit()
            return new_drink_log
        except Exception as e:
            Log.error("Error in ControllerDrinkLogs.add_drink_log", err=e, sys=sys)
            db.session.rollback()
            return None

    @staticmethod
    def delete_drink_log(id: int) -> None:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        DrinkLog.query.filter_by(log_id=id).delete()
        db.session.commit()

    @staticmethod
    def delete_drink_log_by_user(log_id: int, user_id: int):
        """Delete a drink log only if it belongs to the specified user"""
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        try:
            log = DrinkLog.query.filter_by(log_id=log_id, user_id=user_id).first()
            if log:
                db.session.delete(log)
                db.session.commit()
                return True
            return False
        except Exception as e:
            Log.error("Error in ControllerDrinkLogs.delete_drink_log_by_user", err=e, sys=sys)
            db.session.rollback()
            return False

    @staticmethod
    def get_daily_consumption(user_id: int, target_date: date = None):
        """Get daily consumption totals for a user on a specific date (default today)"""
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        
        if target_date is None:
            target_date = date.today()
        
        try:
            # Query all drink logs for the user on the target date
            logs = DrinkLog.query.filter_by(
                user_id=user_id,
                date_created=target_date
            ).all()
            
            # Calculate totals
            total_liquid = sum(log.drink_total_quantity for log in logs)
            total_water = sum(log.drink_water_quantity for log in logs)
            total_alcohol = sum(log.drink_alcohol_quantity for log in logs)
            
            # Calculate other beverages (non-water, non-alcohol)
            total_other = total_liquid - total_water - total_alcohol
            
            # Calculate coffee/tea separately (approximate - drinks with 0% alcohol and less than 90% water)
            total_coffee = 0
            for log in logs:
                if log.drink_alcohol_quantity == 0:
                    # Get drink info to check if it's likely coffee/tea
                    drink = Drink.query.filter_by(drink_id=log.drink_id).first()
                    if drink and drink.drink_water_percentage < 90:
                        total_coffee += log.drink_total_quantity
            
            # Adjust other beverages to exclude coffee
            total_other = max(0, total_other - total_coffee)
            
            # Daily goal (you can make this configurable per user later)
            daily_goal = 2560  # ml (approximately 8 glasses of water)
            
            # Calculate progress percentage
            progress_percentage = min(100, (total_liquid / daily_goal * 100)) if daily_goal > 0 else 0
            
            # Calculate individual percentages for progress bar
            water_percentage = (total_water / daily_goal * 100) if daily_goal > 0 else 0
            coffee_percentage = (total_coffee / daily_goal * 100) if daily_goal > 0 else 0
            alcohol_percentage = (total_alcohol / daily_goal * 100) if daily_goal > 0 else 0
            other_percentage = (total_other / daily_goal * 100) if daily_goal > 0 else 0
            
            return {
                'total_liquid': total_liquid,
                'total_water': total_water,
                'total_coffee': total_coffee,
                'total_alcohol': total_alcohol,
                'total_other': total_other,
                'daily_goal': daily_goal,
                'progress_percentage': progress_percentage,
                'water_percentage': min(100, water_percentage),
                'coffee_percentage': min(100, coffee_percentage),
                'alcohol_percentage': min(100, alcohol_percentage),
                'other_percentage': min(100, other_percentage),
                'date': target_date
            }
            
        except Exception as e:
            Log.error("Error in ControllerDrinkLogs.get_daily_consumption", err=e, sys=sys)
            return {
                'total_liquid': 0,
                'total_water': 0,
                'total_coffee': 0,
                'total_alcohol': 0,
                'total_other': 0,
                'daily_goal': 2560,
                'progress_percentage': 0,
                'water_percentage': 0,
                'coffee_percentage': 0,
                'alcohol_percentage': 0,
                'other_percentage': 0,
                'date': target_date
            }

    @staticmethod
    def get_daily_summary(user_id: int, target_date: date = None):
        """Get detailed daily summary with all drink logs for a specific date"""
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        
        if target_date is None:
            target_date = date.today()
        
        try:
            # Query all drink logs for the user on the target date with drink information
            logs = db.session.query(DrinkLog, Drink).join(
                Drink, DrinkLog.drink_id == Drink.drink_id
            ).filter(
                DrinkLog.user_id == user_id,
                DrinkLog.date_created == target_date
            ).order_by(DrinkLog.log_id.desc()).all()
            
            # Process logs into a more readable format
            drink_logs = []
            total_liquid = 0
            total_water = 0
            total_alcohol = 0
            
            for log, drink in logs:
                drink_data = {
                    'log_id': log.log_id,
                    'drink_name': drink.drink_name,
                    'total_quantity': log.drink_total_quantity,
                    'water_quantity': log.drink_water_quantity,
                    'alcohol_quantity': log.drink_alcohol_quantity,
                    'alcohol_percentage': drink.drink_alcohol_percentage,
                    'drink_image': drink.drink_image,
                    'time_logged': log.date_created  # You might want to add time field to model
                }
                drink_logs.append(drink_data)
                
                # Accumulate totals
                total_liquid += log.drink_total_quantity
                total_water += log.drink_water_quantity
                total_alcohol += log.drink_alcohol_quantity
            
            # Get consumption data for progress
            consumption_data = ControllerDrinkLogs.get_daily_consumption(user_id, target_date)
            
            return {
                'date': target_date,
                'drink_logs': drink_logs,
                'total_logs': len(drink_logs),
                'consumption_summary': consumption_data,
                'has_logs': len(drink_logs) > 0
            }
            
        except Exception as e:
            Log.error("Error in ControllerDrinkLogs.get_daily_summary", err=e, sys=sys)
            return {
                'date': target_date,
                'drink_logs': [],
                'total_logs': 0,
                'consumption_summary': ControllerDrinkLogs.get_daily_consumption(user_id, target_date),
                'has_logs': False
            }