import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1727 import QAP_1727
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1729 import QAP_1729
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1731 import QAP_1731
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1732 import QAP_1732
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1733 import QAP_1733
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1736 import QAP_1736
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2154 import QAP_2154
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2302 import QAP_2302
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2504 import QAP_2504
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2904 import QAP_2904
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2905 import QAP_2905
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2940 import QAP_2940
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2971 import QAP_2971
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_3136 import QAP_3136
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_3399 import QAP_3399
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4153 import QAP_4153
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4709 import QAP_4709
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4861 import QAP_4861
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4862 import QAP_4862
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_5815 import QAP_5815
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_6298 import QAP_6298
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_6299 import QAP_6299
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_6934 import QAP_6934
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_755 import QAP_755
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_756 import QAP_756
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_758 import QAP_758
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_759 import QAP_759
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_760 import QAP_760
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_761 import QAP_761
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_762 import QAP_762
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_763 import QAP_763
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_6714 import QAP_6714
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1737 import QAP_1737


class ReferenceData:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Reference_Data", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Reference_Data")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()

            QAP_755(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_756(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_758(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_759(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_760(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_761(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_762(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_763(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_1727(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_1729(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_1731(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_1732(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_1733(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_1736(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            # TODO:
            # В ТК не упоминается об проверки ПДФ выгрузки. Мне кажется кейс не совсем актуален.
            # // Сделать вместо проверки ПДФ, сделать через эдит
            QAP_1737(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()

            QAP_2154(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2302(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2504(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2904(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2905(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2940(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2971(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3136(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3399(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4153(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4709(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4861(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4862(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5815(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6714(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6299(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6298(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6934(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Reference data ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
