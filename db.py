import sqlite3
import datetime

class Database:
    def __init__(self, database):
        self.db_conn = sqlite3.connect(database)
        self.cursor = self.db_conn.cursor()


    def createTable(self, table_name, column_list):
        """
        Create database table
        :param table_name: name of the table
        :param column_list: list of columns
        :return:
        """
        column_list = column_list.replace("create_date", "create_date datetime")
        query = "CREATE TABLE IF NOT EXISTS "+ table_name + " (" + column_list + ")"
        self.cursor.execute(query)

    def insertRecord(self, table_name, data):
        """
        Insert record if not exists, return new records
        :param table_name: table name
        :param data: data in column lists
        :return:
        """
        columns = ', '.join(data.keys())
        placeholders = ':'+', :'.join(data.keys())
        # Check if record with a given id not exists
        query = "SELECT * FROM %s WHERE id LIKE '%s'" % (table_name, data["id"])
        self.cursor.execute(query)
        query_result = self.cursor.fetchall()
        # If record does not exist, insert into database
        if not query_result:
            query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
            self.cursor.execute(query, data)
            self.db_conn.commit()
            return (True, data)
        else:
            return (False, "")


    def getAllData(self, table_name):
        """

        :param table_name: name of the table
        :return:
        """
        query = 'SELECT * FROM %s' % (table_name)
        query_result = self.cursor.execute(query)
        result = []
        for record in query_result:
            result.append(record)
        return result

    def getDataNDaysBack(self, table_name, number_of_days):
        """

        :param table_name: name of the table
               number_of_daysL: number of days back
        :return:
        """
        query = "SELECT * FROM %s WHERE 'create_date' > date('now', '%s days')" % (table_name,str(number_of_days))
        query_result = self.cursor.execute(query)
        result = []
        for record in query_result:
            result.append(dict(zip([key[0] for key in self.cursor.description], record)))
        return result

    def closeConnection(self):
        self.db_conn.close()