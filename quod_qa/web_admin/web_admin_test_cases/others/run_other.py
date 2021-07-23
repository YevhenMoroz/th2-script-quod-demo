import traceback

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.others.QAP_1738 import QAP_1738
from quod_qa.web_admin.web_admin_test_cases.others.QAP_1739 import QAP_1739
from quod_qa.web_admin.web_admin_test_cases.others.QAP_1741 import QAP_1741
from quod_qa.web_admin.web_admin_test_cases.others.QAP_1831 import QAP_1831
from quod_qa.web_admin.web_admin_test_cases.others.QAP_676 import QAP_676

from quod_qa.web_admin.web_admin_test_cases.others.QAP_800 import QAP_800
from quod_qa.web_admin.web_admin_test_cases.others.QAP_801 import QAP_801
from quod_qa.web_admin.web_admin_test_cases.others.QAP_802 import QAP_802
from custom import basic_custom_actions as bca


class RunOthers:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'web admin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            QAP_676(self.web_driver_container, self.second_lvl_id).run()
            QAP_800(self.web_driver_container, self.second_lvl_id).run()
            QAP_801(self.web_driver_container, self.second_lvl_id).run()
            QAP_802(self.web_driver_container, self.second_lvl_id).run()
            QAP_1738(self.web_driver_container, self.second_lvl_id).run()
            QAP_1739(self.web_driver_container, self.second_lvl_id).run()
            QAP_1741(self.web_driver_container, self.second_lvl_id).run()
            QAP_1831(self.web_driver_container, self.second_lvl_id).run()
            print("--RunOthers finished--")
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
