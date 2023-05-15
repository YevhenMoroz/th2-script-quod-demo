import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3116 import QAP_T3116
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3398 import QAP_T3398
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3544 import QAP_T3544
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3569 import QAP_T3569
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3570 import QAP_T3570
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3660 import QAP_T3660
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3687 import QAP_T3687
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3689 import QAP_T3689
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3716 import QAP_T3716
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3771 import QAP_T3771
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3773 import QAP_T3773
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3774 import QAP_T3774
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3775 import QAP_T3775
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3776 import QAP_T3776
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3778 import QAP_T3778
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3818 import QAP_T3818
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3819 import QAP_T3819
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3820 import QAP_T3820
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3821 import QAP_T3821
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3863 import QAP_T3863
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3864 import QAP_T3864
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3865 import QAP_T3865
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3866 import QAP_T3866
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3867 import QAP_T3867
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3868 import QAP_T3868
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3869 import QAP_T3869
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3870 import QAP_T3870
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3871 import QAP_T3871
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3872 import QAP_T3872
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3877 import QAP_T3877
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3886 import QAP_T3886
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3923 import QAP_T3923
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3924 import QAP_T3924
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3994 import QAP_T3994
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3995 import QAP_T3995
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3996 import QAP_T3996
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T3997 import QAP_T3997
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4000 import QAP_T4000
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4001 import QAP_T4001
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4003 import QAP_T4003
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4004 import QAP_T4004
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4005 import QAP_T4005
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4006 import QAP_T4006
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4007 import QAP_T4007
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4008 import QAP_T4008
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4814 import QAP_T4814
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4815 import QAP_T4815
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T4816 import QAP_T4816
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T7930 import QAP_T7930
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T10799 import QAP_T10799
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T10800 import QAP_T10800
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11071 import QAP_T11071
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11083 import QAP_T11083
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11084 import QAP_T11084
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11085 import QAP_T11085
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11088 import QAP_T11088
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11089 import QAP_T11089
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11090 import QAP_T11090
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11091 import QAP_T11091
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11092 import QAP_T11092
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11093 import QAP_T11093
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11094 import QAP_T11094
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11095 import QAP_T11095
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11096 import QAP_T11096
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11097 import QAP_T11097
from test_cases.web_admin.web_admin_test_cases.order_management.QAP_T11098 import QAP_T11098

class RunOrderManagement:
    def __init__(self, root_report_id, mode, version):
        if mode == 'Regression':
            self.second_lvl_id = bca.create_event(f"WA_OrderManagement" if version is None else f"WA_OrderManagement | {version}", root_report_id)
        else:
            self.second_lvl_id = bca.create_event(f"WA_OrderManagement (verification)" if version is None else f"WA_OrderManagement (verification) | {version}", root_report_id)

        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_PALGO")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[1].web_browser,
                configuration.environment.get_list_web_admin_environment()[1].site_url)
            start_time = time.monotonic()

            QAP_T3116(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3398(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3544(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3569(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3570(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3660(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3687(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3689(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3716(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3771(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3773(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3774(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3775(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3776(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3778(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3818(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3819(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3820(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3821(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3863(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3864(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3865(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3866(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3867(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3868(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3869(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3870(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3871(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3872(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3877(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3886(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3923(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3924(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3994(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3995(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3996(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3997(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4000(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4001(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4003(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4004(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4005(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4006(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4007(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4008(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4814(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4815(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4816(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7930(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T10799(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T10800(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11071(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11083(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11084(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11085(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11088(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11089(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11090(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11091(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11092(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11093(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11094(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11095(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11096(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11097(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T11098(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Order Management ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
