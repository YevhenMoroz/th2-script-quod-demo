import time

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer

from quod_qa.web_admin.web_admin_test_cases.other.QAP_800 import QAP_800
from quod_qa.web_admin.web_admin_test_cases.other.QAP_801 import QAP_801
from quod_qa.web_admin.web_admin_test_cases.other.QAP_802 import QAP_802


class RunOthers:
    def __init__(self, web_driver_container: WebDriverContainer):
        self.web_driver_container = web_driver_container

    def execute(self):
        # QAP_800(self.web_driver_container).run()
        # QAP_801(self.web_driver_container).run()
        QAP_802(self.web_driver_container).run()










