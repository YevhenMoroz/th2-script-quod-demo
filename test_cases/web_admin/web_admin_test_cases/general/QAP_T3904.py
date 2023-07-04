from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3904(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_user("user_1")

    def test_context(self):

        login_page = LoginPage(self.web_driver_container)

        excepted_result = 'System Administration Quod site'
        actual_result = login_page.get_title_text_of_login_page()

        self.verify("Title displayed correctly", excepted_result, actual_result)
