from time import time
import datetime
import pytz
from model import User


class Clocking:

    def __init__(self, tz):
        self.timezone = tz

    def current_date(self):
        """
        Helper function
        """
        def_time = datetime.datetime.today()
        sg_tz = pytz.timezone(self.timezone)
        return def_time.astimezone(sg_tz).date()

    @staticmethod
    def clock_in(ui, users):
        """
        :param user: user model object
        :return: 0 for error, 1 for success
        """
        user = users.get(
            (ui.user_id, ui.server_id),
            User(user_id=ui.user_id, server_id=ui.server_id)
        )
        if user.status == 1:
            ui.status = 0
        else:
            user.status = 1
            user.in_time = time()
            users[(ui.user_id, ui.server_id)] = user
            ui.status = 1
        return ui, users

    @staticmethod
    def new_week(user, new_date):
        """
        Helper function
        """
        old_date = user.last_updated
        diff = new_date - old_date
        return diff.days + old_date.weekday() >= 7

    @staticmethod
    def new_day(user, new_date):
        """
        Helper function
        """
        old_date = user.last_updated
        diff = new_date - old_date
        return diff.days > 0

    def clock_out(self, ui, users):
        """
        :param ui: UserInterface object
        :param users: Users  object
        :return updated ui, users
        """
        user = users.get(
            (ui.user_id, ui.server_id),
            User(user_id=ui.user_id, server_id=ui.server_id)
        )
        if user.status:
            current_time = time()
            new_date = self.current_date()
            t = current_time - user.in_time
            if user.last_updated is None or self.new_day(user, new_date):
                user.daily_time = t
            else:
                user.daily_time += t
            if user.last_updated is None or self.new_week(user, new_date):
                user.weekly_time = t
            else:
                user.weekly_time += t
            if user.last_updated is not None:
                user.total_time += t
            else:
                user.total_time = t
            user.status = 0
            user.in_time = None
            user.last_updated = new_date
            ui.status = 1
        users[(ui.user_id, ui.server_id)] = user
        return ui, users
