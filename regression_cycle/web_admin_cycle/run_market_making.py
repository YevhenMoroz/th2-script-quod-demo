import time
import traceback
from datetime import timedelta
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunMarketMaking:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            # QAP_1647(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1686(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1688(self.web_driver_container, self.second_lvl_id).run()

            #TODO:Error (bug)
            # QAP_1692(self.web_driver_container, self.second_lvl_id).run()

            # QAP_1693(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1695(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1756(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1757(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1758(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2004(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2011(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2022(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2030(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2040(self.web_driver_container, self.second_lvl_id).run()

            #TODO: test is blocked by bug
            # QAP_2045(self.web_driver_container, self.second_lvl_id).run()

            # QAP_2056(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2158(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2247(self.web_driver_container, self.second_lvl_id).run()

            #TODO: test is blocked by bug
            # QAP_2289(self.web_driver_container, self.second_lvl_id).run()

            # QAP_2324(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2379(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2442(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2557(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2626(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2628(self.web_driver_container, self.second_lvl_id).run()

            #TODO: test is blocked by bug
            # QAP_2649(self.web_driver_container, self.second_lvl_id).run()

            # QAP_2772(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3008(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3009(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3010(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3053(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3274(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3275(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4118(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4439(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5707(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6118(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run FXMM ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
