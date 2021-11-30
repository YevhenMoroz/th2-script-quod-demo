import time
import traceback
from datetime import timedelta

from test_cases.web_admin.retail_web_admin_test_cases.client_accounts.QAP_4277 import QAP_4277
from test_cases.web_admin.retail_web_admin_test_cases.client_accounts.QAP_4285 import QAP_4285
from test_cases.web_admin.retail_web_admin_test_cases.client_accounts.QAP_4294 import QAP_4294
from test_cases.web_admin.retail_web_admin_test_cases.client_accounts.QAP_4315 import QAP_4315
from test_cases.web_admin.retail_web_admin_test_cases.client_accounts.QAP_4324 import QAP_4324
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_1740 import QAP_1740
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2181 import QAP_2181
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2182 import QAP_2182
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2183 import QAP_2183
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2195 import QAP_2195
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2196 import QAP_2196
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2197 import QAP_2197
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2202 import QAP_2202
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2203 import QAP_2203
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2224 import QAP_2224
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2225 import QAP_2225
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2461 import QAP_2461
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_2474 import QAP_2474

from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3007 import QAP_3007
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3104 import QAP_3104
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_4864 import QAP_4864
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5443 import QAP_5443
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5601 import QAP_5601


class RunClientsAccounts:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:

            start_time = time.monotonic()
            # QAP_4277(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4315(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4324(self.web_driver_container, self.second_lvl_id).run()
            QAP_4285(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4294(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Client/Accounts Retail ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
