from pymongo import MongoClient, uri_parser


class BaseMongo(object):
    #Dinh nghia URI
    __mongo_uri = 'mongodb://chatify:chatify123@localhost:27017/chatify?directConnection=true'
    __mongo_uri_parse = uri_parser.parse_uri(__mongo_uri)
    __db_name = __mongo_uri_parse.get('database')

    #Khoi tao ket noi
    def __init__(self):
        self.collection_name = ''
        self.mongo_client = MongoClient(self.__mongo_uri, connect = False)
        self.db = self.mongo_client[self.__db_name]

    def find(self, filter_option):
        return self.db[self.collection_name].find(filter_option)

    def find_one(self, filter_option):
        return self.db[self.collection_name].find_one(filter_option)

    def insert_one(self, document):
        return self.db[self.collection_name].insert_one(document)

    def update_one(self, user_id, document):
        return self.db[self.collection_name].update_one({"_id": user_id}, {"$set": document})

    def delete_one(self, filter_option):
        return self.db[self.collection_name].delete_one({"_id": filter_option})
