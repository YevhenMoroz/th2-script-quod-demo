

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ProfilePreferenceSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look

    def click_on_show_order_notifications_radio_button(self):
        pass

    def click_on_hide_order_notifications_radio_button(self):
        pass

    def click_on_show_execution_notifications_radio_button(self):
        pass

    def click_on_hide_execution_notifications_radio_button(self):
        pass

    def click_on_show_other_notifications_radio_button(self):
        pass

    def click_on_hide_other_notifications_radio_button(self):
        pass

    def set_default_client_from_dropdown_list(self,default_client_name:str):
        pass








