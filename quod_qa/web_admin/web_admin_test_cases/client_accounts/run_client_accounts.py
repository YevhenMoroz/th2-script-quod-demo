from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2197 import QAP_2197
from quod_qa.web_admin.web_admin_test_cases.positions.QAP_2165 import QAP_2165
from quod_qa.web_admin.web_admin_test_cases.positions.QAP_2168 import QAP_2168

from custom import basic_custom_actions as bca

class RunClientsAccounts:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'web admin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container



    def execute(self):
        QAP_2197(self.web_driver_container, self.second_lvl_id).run()
