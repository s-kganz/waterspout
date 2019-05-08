import pymysql
import datetime
import dbconfig

class DBHelper:
    
    def connect(self, database="crimemap"):
        return pymysql.connect(host='localhost',
                               user=dbconfig.db_user,
                               passwd=dbconfig.db_password,
                               db=database)
    
    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()
    
    def add_input(self, data):
        connection = self.connect()
        try:
            #TODO resolve SQL injection flaw here
            query = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit() # made database change, commit needed
        finally:
            connection.close()
    
    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()

    def add_crime(self, category, date, lat, lon, desc):
        sql = '''INSERT INTO crimes (category, date, latitude, longitude, description)
        VALUES (%s, %s, %s, %s, %s);'''
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (category, date, lat, lon, desc))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close() 
    
    def get_all_crimes(self):
        connection = self.connect()
        try:
            sql = '''SELECT category, latitude, longitude, date, description
            FROM crimes;
            '''
            with connection.cursor() as cursor:
                cursor.execute(sql)
            
            named_crimes = []
            for crime in cursor:
                named_crime = {
                    'category': crime[0],
                    'latitude': crime[1],
                    'longitude': crime[2],
                    'date' : datetime.datetime.strftime(crime[3], "%Y-%m-%d"),
                    'description': crime[4]
                }
                named_crimes.append(named_crime)
            
            return named_crimes
        finally:
            connection.close()

class MockHelper():
    # Stub class used for testing without an actual database
    def connect(self, database="crimes"):
        pass
    def get_all_inputs(self):
        return []
    def add_input(self, data):
        pass
    def clear_all(self):
        pass
    def add_crime(self, category, date, lat, lon, desc):
        pass
    def get_all_crimes(self):
        return [{ 'latitude': -33.301304,
        'longitude': 26.523355,
        'date': "2000-01-01",
        'category': "mugging",
        'description': "mock description" }]