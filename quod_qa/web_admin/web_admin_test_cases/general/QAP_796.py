from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase

# Draft
class QAP_796(CommonTestCase):

    def test_context(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login("adm03")
        login_page.set_password("adm03")
        login_page.click_login_button()
        login_page.check_is_login_successful()
