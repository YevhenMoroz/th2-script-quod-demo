import time
import traceback
from datetime import timedelta

from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4662 import QAP_4662
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4663 import QAP_4663
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4666 import QAP_4666
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4668 import QAP_4668
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4702 import QAP_4702
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4712 import QAP_4712
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4713 import QAP_4713
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4715 import QAP_4715
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4719 import QAP_4719
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_4724 import QAP_4724
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_5304 import QAP_5304
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_5315 import QAP_5315
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_5681 import QAP_5681
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_5682 import QAP_5682
from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_5695 import QAP_5695
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunSite:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            #QAP_4662(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4663(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4666(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4668(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4715(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4719(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4724(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4712(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4702(self.web_driver_container, self.second_lvl_id).run()
            #QAP_4713(self.web_driver_container, self.second_lvl_id).run()
            #QAP_5304(self.web_driver_container, self.second_lvl_id).run()
            #QAP_5315(self.web_driver_container, self.second_lvl_id).run()
            QAP_5681(self.web_driver_container, self.second_lvl_id).run()
            #QAP_5682(self.web_driver_container, self.second_lvl_id).run()
            #QAP_5695(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Site Retail ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
