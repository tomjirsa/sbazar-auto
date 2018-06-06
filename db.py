import sqlite3

class Database:
    def __init__(self, database):
        self.db_conn = sqlite3.connect(database)
        self.cursor = self.db_conn.cursor()
        self.advert_record = {"id": "",
                 "type": "",
                 "create_date": "",
                 "edit_date": "",
                 "price": "",
                 "name": "",
                 "url_advert": "",
                 "url_image": "",
                 "new": ""}


    def createTable(self, table_name):
        """
        Create database table
        :param table_name: name of the table
        :param column_list: list of columns
        :return:
        """
        column_list = ','.join(self.advert_record.keys())
        column_list = column_list.replace("create_date", "create_date datetime")
        column_list = column_list.replace("edit_date", "edit_date datetime")
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
            query = "UPDATE %s SET new='FALSE' WHERE id=%s" % (table_name,data["id"])
            self.cursor.execute(query)
            self.db_conn.commit()
            return (False, "")

    def create_db_record(self, advertisement, search_phrase):

        url = "https://www.sbazar.cz/"+ advertisement["user"]["user_service"]["shop_url"] + "/detail/" + advertisement["seo_name"]
        if len( advertisement["images"]) > 0 :
            url_image = "https:" + advertisement["images"][0]["url"] + "?fl=exf|crr,1.33333,2|res,800,600,1|wrm,/watermark/sbazar.png,10,10|jpg,80,,1"
        else:
            url_image = "N/A"

        self.advert_record["id"] = advertisement["id"]
        self.advert_record["type"] = search_phrase
        self.advert_record["create_date"] = advertisement["create_date"]
        self.advert_record["edit_date"] = advertisement["edit_date"]
        self.advert_record["price"] = advertisement["price"]
        self.advert_record["name"] = advertisement["name"]
        self.advert_record["url_advert"] = url
        self.advert_record["url_image"] = url_image
        self.advert_record["new"] = "True"
        return self.advert_record

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

    def getNewData(self, table_name):
        """

        :param table_name: name of the table
        :return:
        """
        query = "SELECT * FROM %s WHERE new LIKE 'TRUE'" % (table_name)
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

