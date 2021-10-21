from conversion import id_to_name


class UserInterface:
    
    def __init__(self):
        self.msg = None
        self.status = None
        self.title = None
        self.user_id = None
        self.server_id = None
        self.name_duration = None
        self.user_name = None

    def __repr__(self):
        if self.msg is None:
            return f"UI({self.msg}, {self.status}, {self.title}, {self.user_id}," \
                   f" {self.server_id}, {self.name_duration}, {self.user_name})"
        else:
            return f"UI({self.msg}, {self.status}, {self.title}, {self.user_id}," \
                   f" {self.server_id}, {self.name_duration}, {self.user_name})"
        
    def update(self, **kwargs):
        self.msg = kwargs.get("msg", self.msg)
        self.status = kwargs.get("status", self.status)
        self.title = kwargs.get("title", self.title)
        self.user_id = kwargs.get("user_id", self.user_id)
        self.server_id = kwargs.get("server_id", self.server_id)
        self.name_duration = kwargs.get("name_duration", self.name_duration)
        if type(self.user_id) is str and "#" in self.user_id:
            self.user_name = id_to_name(self.user_id)