import hashlib
import base64
from datetime import datetime

from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest
from custom import basic_custom_actions as bca
from stubs import Stubs

rep_id = bca.create_event('java_api_example ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('java api test', report_id)
        self.act_java_api = Stubs.act_java_api
        self.connectivity = '317_java_api'
        self.login = 'JavaApiUser'
        self.password = 'JavaApiUser'

    def get_hashed_password(self):
        hashed_password = hashlib.sha256()
        hashed_password.update(bytearray(self.login + self.password, 'UTF-8'))
        return base64.b64encode(hashed_password.digest()).decode('UTF-8')

    def send_login(self):
        login_message = {
            'Passwd': self.get_hashed_password(),
            'UserID': self.login,
            'LoginHost': 'TEST_HOSTNAME',
            'Origin': 'TRD',
            'AsyncSubject': 'inbox123'
        }

        self.act_java_api.sendMessage(
            request=ActJavaSubmitMessageRequest(
                message=bca.message_to_grpc('Order_Login', login_message, self.connectivity)))

    # Main method
    def execute(self):
        self.send_login()

if __name__ == '__main__':
    TestCase(rep_id).execute()
    pass