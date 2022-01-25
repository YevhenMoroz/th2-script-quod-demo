

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ProfilePersonalDetailsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    def get_first_name(self):
        pass
    def get_last_name(self):
        pass
    def get_mobile_no(self):
        pass
    def get_email(self):
        pass
    def get_country(self):
        pass
    def get_address(self):
        pass
    def get_data_of_birth(self):
        pass