# by Richi Rod AKA @richionline / falken20
from datetime import date
# import pprint
import sys

from .models import db, Plant, Calendar, User
from .logger import Log
from .config import shorten_url

Log.debug("Loading controllers.py")

# The CRUD operations use to return a JSON response:
# return jsonify(response)


class ControllerPlant:
    def __init__(self):
        pass

    @staticmethod
    def list_all_plants(user_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Plant.query.filter(Plant.user_id == user_id).order_by(Plant.name).all()

    @staticmethod
    def get_plant(plant_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Plant.query.filter_by(id=plant_id).first()

    @staticmethod
    def get_plant_name(plant_name: str):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Plant.query.filter_by(name=plant_name).first()

    @staticmethod
    def create_plant(plant_data: dict, current_user) -> Plant:
        try:
            Log.info(
                f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
            Log.debug(f"Params method: {locals()}")
            Log.debug(f"Creating plant: {plant_data}")
            # pprint.pprint(plant_data)
            image = ""
            if "image" in plant_data:
                image = shorten_url(
                    plant_data["image"]) if plant_data["image"] is not None else ""
            Log.debug(f"Image shortened: {image}")
            spray = False
            if "spray" in plant_data:
                spray = False if bool(plant_data['spray']) is False else True
            plant = Plant(name=plant_data["name"],
                          name_tech=plant_data["name_tech"],
                          comment=plant_data["comment"],
                          watering_summer=int(plant_data["watering_summer"]),
                          watering_winter=int(plant_data["watering_winter"]),
                          spray=spray,
                          direct_sun=int(plant_data["direct_sun"]),
                          image=image, date_created=date.today(),
                          user_id=current_user)

            if plant.name == "" or plant.name is None:
                raise ValueError("Plant name can't be empty")
            if plant.user_id == "" or plant.user_id is None:
                raise ValueError("Plant user_id can't be empty")
            if ControllerUser.get_user(plant.user_id) is None:
                raise ValueError("Plant user_id doesn't exist")
            db.session.add(plant)
            db.session.commit()
            return plant
        except Exception as err:
            Log.error("Error in ControllerPlant.create_plant",
                      err=err, sys=sys)
            raise err

    @staticmethod
    def update_plant(plant_data: dict, current_user) -> Plant:
        try:
            Log.info(
                f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
            Log.debug(f"Params method: {locals()}")
            Log.debug(f"Creating plant: {plant_data}")
            # pprint.pprint(plant_data)
            plant = ControllerPlant.get_plant(plant_data["id"])
            if plant is None:
                return None
            if ControllerUser.get_user(current_user) is None:
                raise ValueError("Plant user_id doesn't exist")
            plant.name = plant_data["name"]
            plant.name_tech = plant_data["name_tech"]
            plant.comment = plant_data["comment"]
            plant.watering_summer = int(plant_data["watering_summer"])
            plant.watering_winter = int(plant_data["watering_winter"])
            if "spray" in plant_data:
                plant.spray = False if bool(
                    plant_data['spray']) is False else True
            else:
                plant.spray = False
            plant.direct_sun = int(plant_data["direct_sun"])
            plant.image = shorten_url(
                plant_data["image"]) if plant_data["image"] != "" else ""
            plant.user_id = current_user
            db.session.commit()
            return plant
        except Exception as e:
            Log.error("Error in ControllerPlant.update_plant", err=e, sys=sys)
            raise e

    @staticmethod
    def delete_plant(plant_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        plant = ControllerPlant.get_plant(plant_id)
        if plant is None:
            return None
        db.session.delete(plant)
        db.session.commit()
        return plant


class ControllerCalendar:
    def __init__(self):
        pass

    @staticmethod
    def get_calendar(plant_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Calendar.query.filter_by(plant_id=plant_id).all()

    @staticmethod
    def get_calendar_date(date_calendar: date, plant_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Calendar.query.filter_by(date_calendar=date_calendar, plant_id=plant_id).first()

    @staticmethod
    def create_calendar(date_calendar: date, water: bool, fertilize: bool, plant_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        calendar = Calendar(date_calendar=date_calendar, water=water,
                            fertilize=fertilize, plant_id=plant_id)
        Log.debug(f"Params method: {locals()}")
        db.session.add(calendar)
        db.session.commit()
        return calendar

    @staticmethod
    def delete_calendar_date(date_calendar: date, plant_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        calendar = ControllerCalendar.get_calendar_date(
            date_calendar, plant_id)
        if calendar is None:
            return None
        db.session.delete(calendar)
        db.session.commit()
        return calendar

    @staticmethod
    def delete_calendar_plant(plant_id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        calendar = ControllerCalendar.get_calendar(plant_id)
        if len(calendar) == 0:
            return None
        for date_calendar in calendar:
            db.session.delete(date_calendar)
        db.session.commit()
        return calendar


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
