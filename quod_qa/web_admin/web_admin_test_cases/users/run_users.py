from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_test_cases.users.QAP_1640 import QAP_1640
from quod_qa.web_admin.web_admin_test_cases.users.QAP_2256 import QAP_2256
from quod_qa.web_admin.web_admin_test_cases.users.QAP_2257 import QAP_2257
from quod_qa.web_admin.web_admin_test_cases.users.QAP_2259 import QAP_2259
from quod_qa.web_admin.web_admin_test_cases.users.QAP_2405 import QAP_2405
from quod_qa.web_admin.web_admin_test_cases.users.QAP_2451 import QAP_2451
from quod_qa.web_admin.web_admin_test_cases.users.QAP_2578 import QAP_2578
from quod_qa.web_admin.web_admin_test_cases.users.QAP_3145 import QAP_3145
from quod_qa.web_admin.web_admin_test_cases.users.QAP_919 import QAP_919


class RunUsers:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'web admin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        # QAP_2451(self.web_driver_container, self.second_lvl_id).run()
        # QAP_1640(self.web_driver_container, self.second_lvl_id).run()
        # #TODO:DON'T WORK Blocker PADM-825
        # QAP_3145(self.web_driver_container, self.second_lvl_id).run()
        # QAP_2256(self.web_driver_container, self.second_lvl_id).run()
        # QAP_2578(self.web_driver_container, self.second_lvl_id).run()
        # QAP_2257(self.web_driver_container, self.second_lvl_id).run()
        # QAP_2259(self.web_driver_container, self.second_lvl_id).run()
        # QAP_2405(self.web_driver_container, self.second_lvl_id).run()
        QAP_919(self.web_driver_container, self.second_lvl_id).run()
