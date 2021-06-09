from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2197 import QAP_2197


class RunClientsAccounts:
    def __init__(self, web_driver_container: WebDriverContainer):
        self.web_driver_container = web_driver_container

    def execute(self):
        QAP_2197(self.web_driver_container).run()
