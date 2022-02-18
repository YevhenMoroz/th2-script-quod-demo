import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.others.QAP_676 import QAP_676
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer

from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.others.QAP_6708 import QAP_6708


class RunOthers:
    def __init__(self,root_report_id):
        self.second_lvl_id = bca.create_event("WA_Others", root_report_id)
        self.web_driver_container = None

    def execute(self):

        try:
            configuration = ComponentConfiguration("WA_Others")  # look at xml (component name="web_admin_general")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_676(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            # QAP_677(self.web_driver_container, self.second_lvl_id).run()
            # QAP_678(self.web_driver_container, self.second_lvl_id).run()
            # QAP_679(self.web_driver_container, self.second_lvl_id).run()
            # QAP_800(self.web_driver_container, self.second_lvl_id).run()
            # QAP_801(self.web_driver_container, self.second_lvl_id).run()
            # QAP_802(self.web_driver_container, self.second_lvl_id).run()
            # QAP_803(self.web_driver_container, self.second_lvl_id).run()
            # QAP_834(self.web_driver_container, self.second_lvl_id).run()
            # QAP_835(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1738(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1739(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1741(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1831(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3228(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3229(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5816(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5922(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6314(self.web_driver_container, self.second_lvl_id).run()
            QAP_6708(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Others ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
            print("--RunOthers finished--")
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
