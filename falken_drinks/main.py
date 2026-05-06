# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import sys

from .logger import Log
from .config import today_cet
from .controllers import ControllerDrinkLogs, ControllerDrinks, ControllerDailyHabits

Log.info("***** Loading app.py")

main = Blueprint('main', __name__)


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
@login_required
def index():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    # Get daily consumption data for the current user
    daily_consumption = ControllerDrinkLogs.get_daily_consumption(current_user.user_id)

    return render_template('home.html', daily_consumption=daily_consumption)


@main.route("/profile", methods=['GET'])
@login_required
def profile():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    return render_template(
        'profile.html',
        name=current_user.name or current_user.email,
        date_created=current_user.date_created
    )


@main.route("/daily_summary", methods=['GET'])
@login_required
def daily_summary():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    daily_summary = ControllerDrinkLogs.get_daily_summary(current_user.user_id)

    return render_template('daily_summary.html', daily_summary=daily_summary)


@main.route("/analytics", methods=['GET', 'POST'])
@login_required
def analytics():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    from datetime import datetime, timedelta

    # Get filter parameters from request
    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        group_by = request.form.get('group_by', 'day')

        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError:
            start_date = None
            end_date = None
    else:
        # Check query args first (for pagination links), then default to last 30 days
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        group_by = request.args.get('group_by', 'day')

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                end_date = today_cet()
                start_date = end_date - timedelta(days=30)
        else:
            end_date = today_cet()
            start_date = end_date - timedelta(days=30)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Get analytics data
    analytics_data = ControllerDrinkLogs.get_filtered_analytics(
        current_user.user_id,
        start_date=start_date,
        end_date=end_date,
        group_by=group_by
    )

    # Paginate grouped_data
    all_groups = analytics_data.get('grouped_data', [])
    total_groups = len(all_groups)
    total_pages = max(1, (total_groups + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    analytics_data['grouped_data'] = all_groups[(page - 1) * per_page: page * per_page]

    return render_template(
        'analytics.html',
        analytics=analytics_data,
        page=page,
        total_pages=total_pages,
        start_date=start_date,
        end_date=end_date,
        group_by=group_by
    )


@main.route("/drinks_management", methods=['GET'])
@login_required
def drinks_management():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    # Get all drinks for display
    drinks = ControllerDrinks.get_drinks()
    Log.debug(f"Drinks retrieved: {drinks}")

    return render_template('drinks_management.html', drinks=drinks)


@main.route('/daily_habits', methods=['GET'])
@login_required
def daily_habits():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    from .models import DailyHabit
    habits = ControllerDailyHabits.get_habits_by_date(current_user.user_id)

    return render_template(
        'daily_habits.html',
        habits=habits,
        texture_options=DailyHabit.TEXTURE_OPTIONS,
        today=today_cet()
    )


@main.route('/daily_habits/calendar', methods=['GET'])
@login_required
def daily_habits_calendar():
    Log.info(
        f"Method {sys._getframe().f_code.co_filename}: {sys._getframe().f_code.co_name}")
    Log.debug(f"Current user: {current_user}")

    today = today_cet()
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)

    # Keep month values in a valid range to avoid invalid-date crashes
    if month < 1 or month > 12:
        month = today.month

    calendar_data = ControllerDailyHabits.get_monthly_calendar(current_user.user_id, year, month)

    return render_template('daily_habits_calendar.html', calendar_data=calendar_data)
