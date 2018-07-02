import sqlite3 as lite

DEBUG = False


class SchemaDB:
    """
        This class provides the tables and fields which a sqlite3 database has.
        In other words the schema of your database
    """

    @staticmethod
    def tables(file_db=None):
        """ Returns a list of the tables in the file_db database"""
        temp = []
        try:
            conn = lite.connect(file_db)
            curs = conn.cursor()
            sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
            curs.execute(sql)
            tables = curs.fetchall()
            if DEBUG: print(tables)
            for table in tables:
                temp.append(table[0])
            return temp

        except lite.Error:
            print(lite.Error)
            return False

    @staticmethod
    def fields(file_db=None, table_name=None):
        """
            Returns a list of the fields from a certain table in the file_db database
        """
        temp = []
        try:
            conn = lite.connect(file_db)
            curs = conn.cursor()
            sql = "PRAGMA TABLE_INFO('{}');".format(table_name)
            curs.execute(sql)
            fields = curs.fetchall()
            if DEBUG: print(fields)
            for field in fields:
                # choosing the second column due to it has the fields names
                temp.append(field[1])
            return temp

        except lite.Error:
            print(lite.Error)
            return False


# This code is for testing the class. We use comment block

"""
    schema = SchemaDB()
    my_list = schema.tables('sensorDHT.db')
    your_list = schema.fields('sensorDHT.db', 'accel')
    print(my_list)
    print(your_list)
"""

