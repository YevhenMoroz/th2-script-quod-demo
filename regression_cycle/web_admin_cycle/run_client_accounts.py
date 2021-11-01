import time
import traceback
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_1740 import QAP_1740
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2181 import QAP_2181
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2182 import QAP_2182
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2183 import QAP_2183
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2195 import QAP_2195
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2196 import QAP_2196
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2197 import QAP_2197
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2202 import QAP_2202
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2203 import QAP_2203
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2224 import QAP_2224
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2225 import QAP_2225
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2461 import QAP_2461
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2474 import QAP_2474

from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_3007 import QAP_3007
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_3104 import QAP_3104
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_4864 import QAP_4864
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_5443 import QAP_5443
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_5601 import QAP_5601


class RunClientsAccounts:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:

            start_time = time.monotonic()
            # QAP_1740(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2181(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2182(self.web_driver_container, self.second_lvl_id).run()
            QAP_2183(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2195(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2196(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2197(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2202(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2203(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2224(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2225(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2461(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2474(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3007(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3104(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4864(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5443(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5601(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Client/Accounts ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
