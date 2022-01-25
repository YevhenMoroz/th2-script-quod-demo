

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ProfileSecuritySubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    def set_old_password(self,old_password:str):
        pass

    def set_new_password(self,new_password:str):
        pass

    def set_confirm_password(self,confirm_password:str):
        pass