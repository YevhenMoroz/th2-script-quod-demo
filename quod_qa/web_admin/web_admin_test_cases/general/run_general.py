from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.general.QAP_796 import QAP_796


class RunGeneral:
    def __init__(self, web_driver_container: WebDriverContainer):
        self.web_driver_container = web_driver_container

    def execute(self):
        QAP_796(self.web_driver_container).run()
