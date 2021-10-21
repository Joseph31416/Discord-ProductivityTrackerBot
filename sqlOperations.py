class Sql:

    def __init__(self, tb_name):
        self.tb_name = "\"" + tb_name + "\""

    def insert(self, fields):
        """
        :param fields: tuple(str) containing name of fields to be inserted
        :return: string of sql query
        """
        num_of_placeholders = len(fields)
        insert_str = f"INSERT INTO {self.tb_name} "
        fields_str = "(" + ", ".join(fields) + ") "
        value_str = "VALUES (" + ", ".join(("%s", ) * num_of_placeholders) + ")"
        query = insert_str + fields_str + value_str + ";"
        return query

    def select(self, fields, constraint_key=None):
        """
        :param fields: tuple(str) containing name of fields to be inserted
        :param constraint_key: tuple(str) containing fields which are constraints
        :return: sql query string
        """
        fields_str = ", ".join(fields)
        if constraint_key is not None:
            select_str = "SELECT " + fields_str + f" FROM {self.tb_name} WHERE "
            constraint = []
            for key in constraint_key:
                temp = f"{key}=%s"
                constraint.append(temp)
            constraint_str = " AND ".join(constraint)
            query = select_str + constraint_str + ";"
        else:
            query = "SELECT " + fields_str + f" FROM {self.tb_name};"
        return query

    def delete(self, constraint_key=None):
        """
        :param constraint_key: tuple(str) containing fields which are constraints
        :return: sql query string
        """
        delete_str = f"DELETE FROM {self.tb_name} WHERE "
        constraint_list = [f"{key}=%s" for key in constraint_key]
        constraint_str = " AND ".join(constraint_list)
        query = delete_str + constraint_str + ";"
        return query

    def update(self, fields, constraint_key=None):
        """
        :param fields: tuple(str) containing fileds to be updated
        :param constraint_key: tuple(str) containing fields which are constraints
        :return: sql query string
        """
        update_str = f"UPDATE {self.tb_name} SET "
        field_list = [f"{field}=%s" for field in fields]
        field_str = ", ".join(field_list)
        constraint_list = [f"{key}=%s" for key in constraint_key]
        constraint_str = " WHERE " + " AND ".join(constraint_list)
        query = update_str + field_str + constraint_str + ";"
        return query

    def drop_table(self):
        return f"DROP TABLE {self.tb_name};"
