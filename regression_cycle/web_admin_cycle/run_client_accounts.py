import time
import traceback
from datetime import timedelta

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
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3007 import QAP_3007
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3104 import QAP_3104
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3230 import QAP_3230
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3231 import QAP_3231
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3232 import QAP_3232
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3783 import QAP_3783
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3814 import QAP_3814
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_3815 import QAP_3815
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_4051 import QAP_4051
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_4381 import QAP_4381
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_4382 import QAP_4382
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_4864 import QAP_4864
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_4983 import QAP_4983
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_4987 import QAP_4987
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5408 import QAP_5408
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5416 import QAP_5416
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5443 import QAP_5443
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5601 import QAP_5601
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5662 import QAP_5662
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5663 import QAP_5663
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5907 import QAP_5907
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5908 import QAP_5908
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5913 import QAP_5913
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5915 import QAP_5915
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_5919 import QAP_5919
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_6143 import QAP_6143
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_6278 import QAP_6278
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_6290 import QAP_6290
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_6706 import QAP_6706
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_6935 import QAP_6935
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer

from custom import basic_custom_actions as bca


class RunClientsAccounts:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Client_Accounts", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Client_Accounts")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_1740(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2181(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2182(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2183(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2195(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2196(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2197(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2202(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2203(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2224(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2225(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2461(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2474(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3007(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3104(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3230(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3231(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3232(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3783(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3814(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3815(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4051(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4381(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4382(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4864(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4983(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4987(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5408(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5416(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5443(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5601(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5662(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5663(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5907(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5908(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5913(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5915(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5919(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6143(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6278(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6290(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6706(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6935(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            end_time = time.monotonic()
            print("Run Client/Accounts ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
