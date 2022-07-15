import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.site.QAP_4173 import QAP_4173
from test_cases.web_admin.web_admin_test_cases.site.QAP_4174 import QAP_4174
from test_cases.web_admin.web_admin_test_cases.site.QAP_4662 import QAP_4662
from test_cases.web_admin.web_admin_test_cases.site.QAP_4663 import QAP_4663
from test_cases.web_admin.web_admin_test_cases.site.QAP_4664 import QAP_4664
from test_cases.web_admin.web_admin_test_cases.site.QAP_4666 import QAP_4666
from test_cases.web_admin.web_admin_test_cases.site.QAP_4668 import QAP_4668
from test_cases.web_admin.web_admin_test_cases.site.QAP_4702 import QAP_4702
from test_cases.web_admin.web_admin_test_cases.site.QAP_4712 import QAP_4712
from test_cases.web_admin.web_admin_test_cases.site.QAP_4713 import QAP_4713
from test_cases.web_admin.web_admin_test_cases.site.QAP_4715 import QAP_4715
from test_cases.web_admin.web_admin_test_cases.site.QAP_4719 import QAP_4719
from test_cases.web_admin.web_admin_test_cases.site.QAP_4724 import QAP_4724
from test_cases.web_admin.web_admin_test_cases.site.QAP_5304 import QAP_5304
from test_cases.web_admin.web_admin_test_cases.site.QAP_5315 import QAP_5315
from test_cases.web_admin.web_admin_test_cases.site.QAP_5364 import QAP_5364
from test_cases.web_admin.web_admin_test_cases.site.QAP_5578 import QAP_5578
from test_cases.web_admin.web_admin_test_cases.site.QAP_5579 import QAP_5579
from test_cases.web_admin.web_admin_test_cases.site.QAP_5580 import QAP_5580
from test_cases.web_admin.web_admin_test_cases.site.QAP_5583 import QAP_5583
from test_cases.web_admin.web_admin_test_cases.site.QAP_5586 import QAP_5586
from test_cases.web_admin.web_admin_test_cases.site.QAP_5640 import QAP_5640
from test_cases.web_admin.web_admin_test_cases.site.QAP_5681 import QAP_5681
from test_cases.web_admin.web_admin_test_cases.site.QAP_5682 import QAP_5682
from test_cases.web_admin.web_admin_test_cases.site.QAP_5695 import QAP_5695
from test_cases.web_admin.web_admin_test_cases.site.QAP_6346 import QAP_6346


class RunSite:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Site", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Site")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            # PRET tests which need refactoring
            # QAP_4662(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5304(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5315(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4668(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4715(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4712(self.web_driver_container, self.second_lvl_id).run()

            # PRET ATs
            QAP_4663(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4666(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4719(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4724(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4702(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4713(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5681(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5682(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5695(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()

            # WA ATs
            QAP_4173(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4174(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4664(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5364(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5578(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5579(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5580(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5583(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5586(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5640(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6346(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            end_time = time.monotonic()
            print("Run Site ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
