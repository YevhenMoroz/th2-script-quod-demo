import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T8215 import QAP_T8215
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T8205 import QAP_T8205
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3971 import QAP_T3971
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3945 import QAP_T3945
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3944 import QAP_T3944
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3943 import QAP_T3943
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3942 import QAP_T3942
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3941 import QAP_T3941
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3940 import QAP_T3940
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3939 import QAP_T3939
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3938 import QAP_T3938
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3937 import QAP_T3937
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3936 import QAP_T3936
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3914 import QAP_T3914
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3913 import QAP_T3913
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3861 import QAP_T3861
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3850 import QAP_T3850
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3832 import QAP_T3832
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3831 import QAP_T3831
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3830 import QAP_T3830
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3813 import QAP_T3813
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3812 import QAP_T3812
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3811 import QAP_T3811
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3810 import QAP_T3810
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3805 import QAP_T3805
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3714 import QAP_T3714
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3713 import QAP_T3713
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3682 import QAP_T3682
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3673 import QAP_T3673
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3671 import QAP_T3671
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3635 import QAP_T3635
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3633 import QAP_T3633
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3630 import QAP_T3630
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3593 import QAP_T3593
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3589 import QAP_T3589
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3588 import QAP_T3588
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3554 import QAP_T3554
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3553 import QAP_T3553
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3552 import QAP_T3552
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3551 import QAP_T3551
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3547 import QAP_T3547
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3518 import QAP_T3518
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3499 import QAP_T3499
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3490 import QAP_T3490
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3407 import QAP_T3407
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3357 import QAP_T3357
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3356 import QAP_T3356
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
            QAP_T3971(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3945(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3944(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3943(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3942(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3941(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3940(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3939(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3938(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3937(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3936(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3914(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3913(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3861(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3850(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3832(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3831(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3830(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3813(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3812(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3811(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3810(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3805(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3714(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3713(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3682(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3673(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3671(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3635(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3633(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3630(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3593(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3589(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3588(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3554(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3553(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3552(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3551(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3547(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3518(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3499(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3490(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3407(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3357(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3356(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8205(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8215(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            end_time = time.monotonic()
            print("Run Client/Accounts ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
