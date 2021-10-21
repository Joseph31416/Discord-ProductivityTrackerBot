from conversion import id_to_name, sec_to_hours


class TimeOptions:
    """
    A class containing methods that return the ui and users object after
    updating the entries of the objects based on the required time operations
    """

    def __init__(self):
        self.msg = None

    @staticmethod
    def time_help(ui):
        ui.status = 0
        return ui

    @staticmethod
    def time_total(ui, users, clock, name=None):
        """
        updates the ui object through using the data in the users object to display
        total accumulated time
        """
        if name is None:
            ui.title = "Total"
            keys = [
                key for key in users.keys() if key[1] == ui.server_id
            ]
            if len(keys) > 0:
                ui.status = 1
        else:
            user_id = None
            keys = []
            for key in users.keys():
                if name.lower() in key[0].lower() and ui.server_id == key[1]:
                    keys.append(key)
                    user_id = key[0]
                    user_name = id_to_name(user_id)
                    break
            if user_id is None:
                ui.status = 2
            else:
                ui.title = f"{user_name}'s Total's"
                ui.status = 1

        ui.name_duration = {
            id_to_name(key[0]): sec_to_hours(users[key].total_time) for key in keys
        }
        return ui, users

    @staticmethod
    def time_weekly(ui, users, clock, name=None):
        """
        updates the ui object through using the data in the users object to display
        weekly accumulated time
        """
        if name is None:
            keys = [
                key for key in users.keys() if key[1] == ui.server_id
            ]
            ui.title = "This Week's"
            ui.status = 1
        else:
            user_id = None
            keys = []
            for key in users.keys():
                if name.lower() in key[0].lower() and ui.server_id == key[1]:
                    keys.append(key)
                    user_id = key[0]
                    user_name = id_to_name(user_id)
                    break
            if user_id is None:
                ui.status = 2
            else:
                ui.title = f"{user_name}'s Week's"
                ui.status = 1
        date_today = clock.current_date()
        name_duration = {}
        if ui.status != 2:
            for key in keys:
                user = users[key]
                if clock.new_week(user, date_today):
                    user.weekly_time = 0
                    users[key] = user
                name_duration[id_to_name(key[0])] = sec_to_hours(user.weekly_time)
            if len(name_duration) == 0:
                ui.status = 0
            else:
                ui.status = 1
        ui.name_duration = name_duration
        return ui, users

    @staticmethod
    def time_daily(ui, users, clock, name=None):
        """
        updates the ui object through using the data in the users object to display
        daily accumulated time
        """
        if name is None:
            keys = [
                key for key in users.keys() if key[1] == ui.server_id
            ]
            ui.title = "Today's"
            ui.status = 1
        else:
            user_id = None
            keys = []
            for key in users.keys():
                if name.lower() in key[0].lower() and ui.server_id == key[1]:
                    keys.append(key)
                    user_id = key[0]
                    user_name = id_to_name(user_id)
                    break
            if user_id is None:
                ui.status = 2
            else:
                ui.status = 1
                ui.title = f"{user_name}'s Today's"
        date_today = clock.current_date()
        name_duration = {}
        if ui.status != 2:
            for key in keys:
                user = users[key]
                if clock.new_day(user, date_today):
                    user.daily_time = 0
                    users[key] = user
                name_duration[id_to_name(key[0])] = sec_to_hours(user.daily_time)
            if len(name_duration) == 0:
                ui.status = 0
            else:
                ui.status = 1
        ui.name_duration = name_duration
        return ui, users

    @staticmethod
    def is_help(msg_parts):
        """
        Helper function
        """
        return len(msg_parts) == 1

    @staticmethod
    def has_name(msg_parts):
        """
        Helper function
        """
        return len(msg_parts) == 3

    @staticmethod
    def is_total(msg_parts):
        """
        Helper function
        """
        return msg_parts[1] == "total"

    @staticmethod
    def is_weekly(msg_parts):
        """
        Helper function
        """
        return msg_parts[1] == "weekly"

    @staticmethod
    def is_daily(msg_parts):
        """
        Helper function
        """
        return msg_parts[1] == "daily"

    def update(self, ui, users, clock):
        """
        updates the ui object based on the data in the users object
        """
        self.msg = ui.msg
        msg_parts = self.msg.strip().split()
        name = None
        if self.is_help(msg_parts):
            ui = self.time_help(ui)
        else:
            if self.has_name(msg_parts):
                name = msg_parts[2]
            if self.is_total(msg_parts):
                ui, users = self.time_total(ui, users, clock, name)
            elif self.is_weekly(msg_parts):
                ui, users = self.time_weekly(ui, users, clock, name)
            elif self.is_daily(msg_parts):
                ui, users = self.time_daily(ui, users, clock, name)
            else:
                ui = self.time_help(ui)
        return ui, users
