from database import PostgreSQLDatabase


db = PostgreSQLDatabase()
all_fields = ('user_id', 'server_id', 'status', 'in_time',
              'total_time', 'weekly_time', 'daily_time', 'last_updated')


class User:
    """
    attributes:
    + user_id
    + server_id
    + status
    + in_time
    + total_time
    + weekly_time
    + daily_time
    + last_updated

    methods:
    + to_tuple()
    """

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id", None)
        self.server_id = kwargs.get("server_id", None)
        self.status = kwargs.get("status", None)
        self.in_time = kwargs.get("in_time", None)
        self.total_time = kwargs.get("total_time", None)
        self.weekly_time = kwargs.get("weekly_time", None)
        self.daily_time = kwargs.get("daily_time", None)
        self.last_updated = kwargs.get("last_updated", None)

    def __repr__(self):
        return f"""User{self.to_tuple()}"""

    def to_tuple(self):
        return (
            self.user_id,
            self.server_id,
            self.status,
            self.in_time,
            self.total_time,
            self.weekly_time,
            self.daily_time,
            self.last_updated
        )


class Users:
    """
    A collection of user models that behave like a dictionary

    Additional methods:
    + sync()
    + not_in_db()
    + update_db()
    + load()
    """
    def __init__(self):
        self.coll = {}

    def __setitem__(self, key, value):
        self.coll[key] = value

    def __getitem__(self, key):
        return self.coll.get(key, None)

    def keys(self):
        return list(self.coll.keys())

    def values(self):
        return list(self.coll.values())

    def get(self, key, *args):
        fall_back = args[0]
        return self.coll.get(key, fall_back)

    def pop(self, key):
        if key in self.coll:
            return self.coll.pop(key)
        return None

    def sync(self):
        """
        synchronises entries in database with the attributes of the instantiated Users object
        """
        models = self.values()
        try:
            self.update_db(models)
        except:
            print("SYNC FAILED")

    @staticmethod
    def not_in_db(models):
        """
        Helper function that takes in a models object and returns a list of keys of the model
        that are not in the database
        """
        fields = ['user_id', 'server_id']
        in_db = db.select(fields, None, None)
        user_server_in_models = [
            (model.user_id, model.server_id) for model in models
        ]
        return [
            el for el in user_server_in_models if el not in in_db
        ]

    def update_db(self, models):
        """
        Updates the database with the given list of models
        """
        values_list = [
            model.to_tuple() for model in models
        ]
        constraint_value_list = [
            (model.user_id, model.server_id) for model in models
        ]
        db.update_many(
            all_fields,
            values_list,
            ("user_id", "server_id"),
            constraint_value_list
        )
        not_in = self.not_in_db(models)
        insert_values_list = [
            model.to_tuple() for model in models if (model.user_id, model.server_id) in not_in
        ]
        for values in insert_values_list:
            db.insert(all_fields, values)

    def load(self):
        """
        Returns an instance of the Users object by loading in the entries from the database
        """
        results = db.select(
            all_fields,
            None,
            None
        )
        for result in results:
            key = (result[0], result[1])
            self.coll[key] = User(
                user_id=result[0],
                server_id=result[1],
                status=result[2],
                in_time=result[3],
                total_time=result[4],
                weekly_time=result[5],
                daily_time=result[6],
                last_updated=result[7]
            )
