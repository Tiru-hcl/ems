import pymongo
import json


class JsonRead:

    @staticmethod
    def jso():
        """
         method to read json file to read json file
         :return: dict object
        """
        with open('config.json') as config_file:
            data = json.load(config_file)
        return data


class Db:
    @staticmethod
    def conf():
        """
        To setup Db configuration
        :return: DB connection details
        """
        jso_data = JsonRead.jso()
        mongo = pymongo.MongoClient(host=jso_data['host'],
                                    port=jso_data['port'],
                                    serverSelectionTimeoutMs=1000
                                    )
        db = mongo.office
        db_conn = db.emp
        return db_conn
