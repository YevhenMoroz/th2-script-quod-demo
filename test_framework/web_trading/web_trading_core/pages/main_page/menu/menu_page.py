
from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class MenuPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    def click_on_profile_button(self):
        pass

    def click_on_hide_header_button(self):
        pass

    def click_on_dark_theme_button(self):
        pass

    def click_on_contact_us_button(self):
        pass

    def click_on_logout_button(self):
        pass
