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
