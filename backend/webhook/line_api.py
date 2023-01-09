from flask import request, jsonify
from flask_restful import Resource
import base64, hashlib, hmac,os
from dotenv import load_dotenv
# from common_lib.pub_sub_client import Publisher
# from common_lib.db_context import MessageDbContext

load_dotenv('../.env')

LINE_SECRET_ID=os.environ['LINE_SECRET_ID']
# RABBITMQ_HOST=os.environ['RABBITMQ_HOST']
# LINE_WEBHOOK_EXCHANE=os.environ['LINE_WEBHOOK_EXCHANE']
# LINE_WEBHOOK_ROUTING_KEY=os.environ['LINE_WEBHOOK_ROUTING_KEY']
# MONGODB_URL=os.environ['MONGODB_URL']

class LineApi(Resource):
    def get(self, client_id):
        response = jsonify({"message": "Webhook is running...", "client_id": client_id})
        response.status_code = 200
        return response
    
    def post(self, client_id):
        data = request.get_json()
        x_line_sig = request.headers['x-line-signature']
        str_data = request.data.decode('utf-8')
        val_sig = self.validate_signature(LINE_SECRET_ID, str_data, x_line_sig)
        print(client_id)

        # TODO:
        # - [ ] check the message type
        # - [ ] save the message and return result
        # - [ ] if true publish the message
        # - [ ] return status 

        # events = data['events']
        
        if val_sig:
            # msg_db_context = MessageDbContext(MONGODB_URL)

            # result = msg_db_context.save(data)

            response = jsonify({"message": "success", "client_id": client_id, "data": data})
            response.status_code = 200

            # if result:
            #     data['_id'] = ''
            #     publisher = Publisher(RABBITMQ_HOST)
            #     publisher.run(LINE_WEBHOOK_EXCHANE, LINE_WEBHOOK_ROUTING_KEY, data)

            #     response.status_code = 200
            #     return response
            # response = jsonify({})
            # response.status_code = 500

            return response

        response = jsonify({"message": "Forbidden"})
        response.status_code = 403
        return response
    
    def validate_signature(self, channel_secret: str, body: str, x_line_sig):
        new_hash = hmac.new(channel_secret.encode('utf-8'),
                body.encode('utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(new_hash).decode('utf-8')
        return x_line_sig == signature