import pymongo, os


class DbContext:
    db = None
    collection = None
    mongo_url = ''

    def __init__(self, mongo_url, db_name:str, coll_name: str) -> None:
        client = pymongo.MongoClient(mongo_url)
        self.db = client[db_name]
        self.collection = self.db[coll_name]

    def first(self, query):
        return self.collection.find_one(query)
    
    def find(self, query: dict=None, selection: dict=None):
        return self.collection.find(query, selection)
        # if query != None:
        #     for doc in self.collection.find(query, selection):
        #         return doc

        # for doc in self.collection.find():
        #     return doc
    def callback(self):
        pass
    
    def save(self, cols) -> bool:
        try:
            self.collection.insert_one(cols)
            return True
        except:
            return False


class MessageDbContext(DbContext):
    message_cols={}
    def __init__(self, mongo_url, client_id:int, member_id:str, message: dict) -> None:
        DbContext.__init__(self,mongo_url,  'MESSAGE_DB', 'messages')
        self.mongo_url = mongo_url
        self.client_id=client_id
        self.member_id=member_id
        self.message=message

        self.callback()

    def callback(self):
        self.message_cols = {"ClientId": self.client_id, "MemberId": self.member_id, "MessageObject": self.message}
        super().save(self.message_cols)
        print('Message saved')

        MemberDbContext(self.mongo_url, self.message, self.client_id)

class MemberDbContext(DbContext):
    def __init__(self, mongo_url, message: dict, client_id: int) -> None:
        DbContext.__init__(self, mongo_url, 'MESSAGE_DB', 'members')
        self.message=message
        self.client_id=client_id
        self.callback()

    def callback(self):
        events = self.message['events']
        # dest = message['destination']

        # for event in events:
        first_event = events[0]

        # msg_type = first_event['type']

        # if msg_type == 'follow':
        #     # TODO:
            # - [ ] find the user
            # - [ ] if not exist insert it
        user_id = first_event['source']['userId']
        query = {"MemberId": user_id}

        member = self.first(query)
        if member is None:
            member_doc = {"MemberId": user_id, "ClientId": self.client_id}
            # self.collection.insert_one(member_doc)
            super().save(member_doc)
            print('Member saved')