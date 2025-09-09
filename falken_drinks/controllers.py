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
    def get_or_create_drink(drink_name: str, alcohol_percentage: float = 0):
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
        DrinkLog.query.filter_by(id=id).delete()
        db.session.commit()