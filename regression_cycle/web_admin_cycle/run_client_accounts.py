import time
import traceback
from datetime import timedelta

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer

from custom import basic_custom_actions as bca


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
            # QAP_2183(self.web_driver_container, self.second_lvl_id).run()
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
            # QAP_3230(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3231(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3232(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4381(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4382(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4864(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5443(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5601(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6278(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6290(self.web_driver_container, self.second_lvl_id).run()
            end_time = time.monotonic()
            print("Run Client/Accounts ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)