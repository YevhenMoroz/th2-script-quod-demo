import time
import traceback
from datetime import timedelta

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1737 import QAP_1737


class ReferenceData:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()

            # QAP_755(self.web_driver_container, self.second_lvl_id).run()
            # QAP_756(self.web_driver_container, self.second_lvl_id).run()
            # QAP_758(self.web_driver_container, self.second_lvl_id).run()
            # QAP_759(self.web_driver_container, self.second_lvl_id).run()
            # QAP_760(self.web_driver_container, self.second_lvl_id).run()
            # QAP_761(self.web_driver_container, self.second_lvl_id).run()
            # QAP_762(self.web_driver_container, self.second_lvl_id).run()
            # QAP_763(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1727(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1729(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1731(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1732(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1733(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1736(self.web_driver_container, self.second_lvl_id).run()

# В ТК не упоминается об проверки ПДФ выгрузки. Мне кажется кейс не совсем актуален.
# // Сделать вместо проверки ПДФ, сделать через эдит
            QAP_1737(self.web_driver_container, self.second_lvl_id).run()

            # QAP_2154(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2302(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2504(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2904(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2905(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2940(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2971(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3136(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3399(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4153(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4709(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4861(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4862(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5815(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6299(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6298(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Reference data ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)




