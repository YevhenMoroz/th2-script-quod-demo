import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.market_making.QAP_1647 import QAP_1647
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_1693 import QAP_1693
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_1695 import QAP_1695
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_1756 import QAP_1756
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_1757 import QAP_1757
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_1758 import QAP_1758
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2004 import QAP_2004
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2011 import QAP_2011
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2022 import QAP_2022
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2030 import QAP_2030
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2040 import QAP_2040
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2056 import QAP_2056
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2158 import QAP_2158
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2247 import QAP_2247
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2324 import QAP_2324
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2379 import QAP_2379
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2442 import QAP_2442
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2557 import QAP_2557
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2626 import QAP_2626
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2628 import QAP_2628
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_2772 import QAP_2772
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_3008 import QAP_3008
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_3009 import QAP_3009
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_3010 import QAP_3010
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_3053 import QAP_3053
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_3274 import QAP_3274
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_3275 import QAP_3275
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_4118 import QAP_4118
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_4439 import QAP_4439
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_5707 import QAP_5707
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_6118 import QAP_6118
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunMarketMaking:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Market_Making", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Market_Making")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_1647(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
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
