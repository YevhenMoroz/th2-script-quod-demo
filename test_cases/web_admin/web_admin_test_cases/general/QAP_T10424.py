import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10424(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.version_and_revision = 'Version x.x.xxx.xxx.xxxxxxxxxx_xxxxxxxx'

    def test_context(self):

        login_page = LoginPage(self.web_driver_container)
        get_site_version_and_revision = login_page.get_version()
        time.sleep(1)
        self.verify("Version and revision displayed at main page", len(self.version_and_revision),
                    len(get_site_version_and_revision))
