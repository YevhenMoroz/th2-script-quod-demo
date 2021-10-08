import time
import traceback
from datetime import timedelta
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_1647 import QAP_1647
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_1688 import QAP_1688
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_1693 import QAP_1693
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_1695 import QAP_1695
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_1756 import QAP_1756
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_1757 import QAP_1757
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_1758 import QAP_1758
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2004 import QAP_2004
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2011 import QAP_2011
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2022 import QAP_2022
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2030 import QAP_2030
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2040 import QAP_2040
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2045 import QAP_2045
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2056 import QAP_2056
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2158 import QAP_2158
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2247 import QAP_2247
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2289 import QAP_2289
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2379 import QAP_2379
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2442 import QAP_2442
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2557 import QAP_2557
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2626 import QAP_2626
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2628 import QAP_2628
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2649 import QAP_2649
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_2772 import QAP_2772
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_3008 import QAP_3008
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_3009 import QAP_3009
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_3010 import QAP_3010
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_3274 import QAP_3274
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_3275 import QAP_3275
from quod_qa.web_admin.web_admin_test_cases.fx_market_making.QAP_4439 import QAP_4439


class RunFxMarketMaking:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            #QAP_1647(self.web_driver_container, self.second_lvl_id).run()
            #QAP_1688(self.web_driver_container, self.second_lvl_id).run()
            #QAP_1693(self.web_driver_container, self.second_lvl_id).run()
            #QAP_1695(self.web_driver_container, self.second_lvl_id).run()
            QAP_1756(self.web_driver_container, self.second_lvl_id).run()
            # QAP_1757(self.web_driver_container, self.second_lvl_id).run()
            #QAP_1758(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2004(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2011(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2022(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2030(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2040(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2045(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2056(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2158(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2247(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2557(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2289(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2379(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2442(self.web_driver_container, self.second_lvl_id).run()
            #QAP_2626(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2628(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2649(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2772(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3008(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3009(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3010(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3274(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3275(self.web_driver_container, self.second_lvl_id).run()
            QAP_4439(self.web_driver_container, self.second_lvl_id).run()
            end_time = time.monotonic()
            print("Run FXMM ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
