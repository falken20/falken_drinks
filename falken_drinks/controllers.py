# by Richi Rod AKA @richionline / falken20
from datetime import date, datetime, timedelta
# import pprint
import sys

from .models import db, Drink, DrinkLog, User
from .config import today_cet
from .logger import Log

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
            return User.query.filter_by(user_id=id).first()
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
        User.query.filter_by(user_id=id).delete()
        db.session.commit()


class ControllerDrinks:
    def __init__(self):
        pass

    @staticmethod
    def get_drink(id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Drink.query.filter_by(drink_id=id).first()

    @staticmethod
    def get_drink_name(name: str, user_id: int = None):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return Drink.query.filter_by(drink_name=name, user_id=user_id).first()

    @staticmethod
    def get_or_create_drink(
        drink_name: str,
        alcohol_percentage: float = 0,
        drink_total_quantity: int = 0,
        user_id: int = None
    ):
        """Get existing drink or create new one if it doesn't exist"""
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        try:
            # Try to find existing drink for this user
            drink = Drink.query.filter_by(drink_name=drink_name, user_id=user_id).first()

            if not drink:
                # Create new drink if it doesn't exist
                water_percentage = 100 - alcohol_percentage
                drink_data = {
                    'drink_name': drink_name,
                    'drink_water_percentage': int(water_percentage),
                    'drink_alcohol_percentage': int(alcohol_percentage),
                    'user_id': user_id
                }
                drink = ControllerDrinks.add_drink(drink_data)

            return drink
        except Exception as e:
            Log.error("Error in ControllerDrinks.get_or_create_drink", err=e, sys=sys)
            return None

    @staticmethod
    def get_drinks(user_id: int = None):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        all_drinks = Drink.query.filter_by(user_id=user_id).all()
        Log.debug(f"Drinks found: {len(all_drinks)}")
        return all_drinks

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
    def seed_default_drinks(user_id: int) -> None:
        """Create the 9 default drink types for a new user"""
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        default_drinks = [
            {'drink_name': 'Water', 'drink_water_percentage': 100, 'drink_alcohol_percentage': 0,
             'counts_as_water': True, 'drink_image': 'icons8-water-96.png'},
            {'drink_name': 'Coffee', 'drink_water_percentage': 99, 'drink_alcohol_percentage': 0,
             'counts_as_water': False, 'drink_image': 'icons8-coffee-96.png'},
            {'drink_name': 'Wine', 'drink_water_percentage': 88, 'drink_alcohol_percentage': 12,
             'counts_as_water': False, 'drink_image': 'icons8-wine-96.png'},
            {'drink_name': 'Beer', 'drink_water_percentage': 93, 'drink_alcohol_percentage': 5,
             'counts_as_water': False, 'drink_image': 'icons8-beer-96.png'},
            {'drink_name': 'Cocktail', 'drink_water_percentage': 80, 'drink_alcohol_percentage': 15,
             'counts_as_water': False, 'drink_image': 'icons8-cocktail-96.png'},
            {'drink_name': 'Shot', 'drink_water_percentage': 60, 'drink_alcohol_percentage': 40,
             'counts_as_water': False, 'drink_image': 'icons8-shot-96.png'},
            {'drink_name': 'Soda', 'drink_water_percentage': 99, 'drink_alcohol_percentage': 0,
             'counts_as_water': True, 'drink_image': 'icons8-soda-96.png'},
            {'drink_name': 'Milk', 'drink_water_percentage': 88, 'drink_alcohol_percentage': 0,
             'counts_as_water': True, 'drink_image': 'icons8-milk-96.png'},
            {'drink_name': 'Energy', 'drink_water_percentage': 97, 'drink_alcohol_percentage': 0,
             'counts_as_water': False, 'drink_image': 'icons8-energy-96.png'},
        ]
        try:
            for drink_data in default_drinks:
                drink_data['user_id'] = user_id
                ControllerDrinks.add_drink(drink_data)
            Log.info(f"Seeded {len(default_drinks)} default drinks for user_id={user_id}")
        except Exception as e:
            Log.error("Error in ControllerDrinks.seed_default_drinks", err=e, sys=sys)

    @staticmethod
    def delete_drink(id: int) -> None:
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        try:
            Drink.query.filter_by(drink_id=id).delete()
            db.session.commit()
        except Exception as e:
            Log.error("Error in ControllerDrinks.delete_drink", err=e, sys=sys)
            db.session.rollback()
            raise


class ControllerDrinkLogs:
    def __init__(self):
        pass

    @staticmethod
    def get_drink_log(id: int):
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
        return DrinkLog.query.filter_by(log_id=id).first()

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
    def get_daily_consumption(user_id: int, target_date: date = None):  # noqa: C901
        """Get daily consumption totals for a user on a specific date (default today)"""
        Log.info(
            f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")

        if target_date is None:
            target_date = today_cet()

        try:
            # Single JOIN query — eliminates N+1 per-log Drink lookups
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())

            rows = db.session.query(DrinkLog, Drink).join(
                Drink, DrinkLog.drink_id == Drink.drink_id
            ).filter(
                DrinkLog.user_id == user_id,
                DrinkLog.date_created >= start_datetime,
                DrinkLog.date_created <= end_datetime
            ).all()

            # Calculate totals in a single pass
            total_liquid = 0
            total_water = 0
            total_coffee = 0
            total_alcohol = 0
            total_other = 0
            total_water_for_progress = 0

            for log, drink in rows:
                total_liquid += log.drink_total_quantity

                if drink.counts_as_water:
                    total_water_for_progress += log.drink_water_quantity

                if drink.drink_alcohol_percentage > 0:
                    total_alcohol += log.drink_total_quantity
                elif drink.drink_water_percentage >= 98:
                    total_water += log.drink_total_quantity
                elif drink.drink_water_percentage < 90:
                    total_coffee += log.drink_total_quantity
                else:
                    total_other += log.drink_total_quantity

            Log.debug(f"Total water: {total_water} ml, "
                      f"Total coffee/tea: {total_coffee} ml, "
                      f"Total alcohol: {total_alcohol} ml, "
                      f"Total other: {total_other} ml")

            Log.debug(f"Total water for progress: {total_water_for_progress} ml")

            # Daily goal (you can make this configurable per user later)
            daily_goal = 2560  # ml (approximately 8 glasses of water)

            progress_percentage = min(100, (total_water_for_progress / daily_goal * 100)) if daily_goal > 0 else 0

            # Calculate individual percentages for progress bar
            water_percentage = (total_water / daily_goal * 100) if daily_goal > 0 else 0
            coffee_percentage = (total_coffee / daily_goal * 100) if daily_goal > 0 else 0
            alcohol_percentage = (total_alcohol / daily_goal * 100) if daily_goal > 0 else 0
            other_percentage = (total_other / daily_goal * 100) if daily_goal > 0 else 0

            Log.debug(f"Total liquid: {total_liquid} ml, "
                      f"Total water: {total_water} ml, "
                      f"Total alcohol: {total_alcohol} ml, "
                      f"Total other: {total_other} ml, "
                      f"Total Water Progress: {total_water_for_progress} ml")

            return {
                'total_water_for_progress': total_water_for_progress,
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
            target_date = today_cet()

        try:
            # Query all drink logs for the user on the target date with drink information
            # Since date_created is DateTime, filter by date range
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())

            logs = db.session.query(DrinkLog, Drink).join(
                Drink, DrinkLog.drink_id == Drink.drink_id
            ).filter(
                DrinkLog.user_id == user_id,
                DrinkLog.date_created >= start_datetime,
                DrinkLog.date_created <= end_datetime
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
                    'water_percentage': drink.drink_water_percentage,
                    'counts_as_water': drink.counts_as_water,
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
                'total_liquid': total_liquid,
                'total_water': total_water,
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

    @staticmethod
    def get_filtered_analytics(  # noqa: C901
        user_id: int,
        start_date: date = None,
        end_date: date = None,
        group_by: str = 'day'
    ):
        """Get analytics data with date filters and grouping options

        Args:
            user_id: User ID
            start_date: Start date for filter (default: 30 days ago)
            end_date: End date for filter (default: today)
            group_by: Grouping option - 'day', 'week', 'month', 'year'
        """
        Log.info(f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")

        if end_date is None:
            end_date = today_cet()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        try:
            # Convert dates to datetime range
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())

            # Get all logs in date range
            logs = db.session.query(DrinkLog, Drink).join(
                Drink, DrinkLog.drink_id == Drink.drink_id
            ).filter(
                DrinkLog.user_id == user_id,
                DrinkLog.date_created >= start_datetime,
                DrinkLog.date_created <= end_datetime
            ).order_by(DrinkLog.date_created.desc()).all()

            # Process logs by grouping
            grouped_data = {}
            all_logs_detail = []
            total_water = 0
            total_liquid = 0
            total_alcohol = 0

            for log, drink in logs:
                log_date = log.date_created.date()

                # Determine group key based on group_by parameter
                if group_by == 'day':
                    group_key = log_date.strftime('%Y-%m-%d')
                    group_label = log_date.strftime('%b %d, %Y')
                elif group_by == 'week':
                    week_start = log_date - timedelta(days=log_date.weekday())
                    group_key = week_start.strftime('%Y-%m-%d')
                    group_label = f"Week of {week_start.strftime('%b %d, %Y')}"
                elif group_by == 'month':
                    group_key = log_date.strftime('%Y-%m')
                    group_label = log_date.strftime('%B %Y')
                elif group_by == 'year':
                    group_key = log_date.strftime('%Y')
                    group_label = log_date.strftime('%Y')
                else:
                    group_key = log_date.strftime('%Y-%m-%d')
                    group_label = log_date.strftime('%b %d, %Y')

                # Initialize group if not exists
                if group_key not in grouped_data:
                    grouped_data[group_key] = {
                        'label': group_label,
                        'total_liquid': 0,
                        'total_water': 0,
                        'total_alcohol': 0,
                        'total_coffee': 0,
                        'total_other': 0,
                        'log_count': 0,
                        'logs': []
                    }

                # Add to group totals
                grouped_data[group_key]['total_liquid'] += log.drink_total_quantity
                grouped_data[group_key]['total_water'] += log.drink_water_quantity
                grouped_data[group_key]['total_alcohol'] += log.drink_alcohol_quantity
                grouped_data[group_key]['log_count'] += 1

                # Add log detail to group
                log_detail = {
                    'log_id': log.log_id,
                    'drink_name': drink.drink_name,
                    'total_quantity': log.drink_total_quantity,
                    'water_quantity': log.drink_water_quantity,
                    'alcohol_quantity': log.drink_alcohol_quantity,
                    'date_created': log.date_created,
                    'drink_image': drink.drink_image
                }
                grouped_data[group_key]['logs'].append(log_detail)
                all_logs_detail.append(log_detail)

                # Overall totals
                total_liquid += log.drink_total_quantity
                total_water += log.drink_water_quantity
                total_alcohol += log.drink_alcohol_quantity

            # Convert to sorted list
            grouped_list = [
                {'key': k, **v} for k, v in grouped_data.items()
            ]
            grouped_list.sort(key=lambda x: x['key'], reverse=True)

            return {
                'start_date': start_date,
                'end_date': end_date,
                'group_by': group_by,
                'grouped_data': grouped_list,
                'all_logs': all_logs_detail,
                'total_logs': len(all_logs_detail),
                'summary': {
                    'total_liquid': total_liquid,
                    'total_water': total_water,
                    'total_alcohol': total_alcohol,
                    'avg_daily_liquid': total_liquid / max(1, (end_date - start_date).days + 1),
                    'avg_daily_water': total_water / max(1, (end_date - start_date).days + 1)
                }
            }

        except Exception as e:
            Log.error("Error in ControllerDrinkLogs.get_filtered_analytics", err=e, sys=sys)
            return {
                'start_date': start_date,
                'end_date': end_date,
                'group_by': group_by,
                'grouped_data': [],
                'all_logs': [],
                'total_logs': 0,
                'summary': {
                    'total_liquid': 0,
                    'total_water': 0,
                    'total_alcohol': 0,
                    'avg_daily_liquid': 0,
                    'avg_daily_water': 0
                }
            }
