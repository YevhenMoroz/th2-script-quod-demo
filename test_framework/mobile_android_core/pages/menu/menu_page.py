from test_framework.mobile_android_core.pages.menu.menu_constants import MenuConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class MenuPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    # region account
    def click_on_personal_details(self):
        self.find_by_xpath(MenuConstants.PERSONAL_DETAILS_BUTTON).click()

    def click_on_preferences(self):
        self.find_by_xpath(MenuConstants.PREFERENCES_BUTTON).click()

    def click_on_security(self):
        self.find_by_xpath(MenuConstants.SECURITY_BUTTON).click()

    def click_on_logout(self):
        self.find_by_xpath(MenuConstants.LOGOUT_BUTTON).click()
    # endregion

    # region Personal Details
    def click_pd_go_back(self):
        self.find_by_xpath(MenuConstants.PD_GO_BACK_BUTTON).click()

    def click_pd_email(self):
        self.find_by_xpath(MenuConstants.PD_EMAIL).click()

    def click_pd_mobile_no(self):
        self.find_by_xpath(MenuConstants.PD_MOBILE_NO).click()

    def clear_pd_email(self):
        self.find_by_xpath(MenuConstants.PD_EMAIL).clear()

    def clear_pd_mobile_no(self):
        self.find_by_xpath(MenuConstants.PD_MOBILE_NO).clear()

    def set_pd_email(self, keys):
        self.find_by_xpath(MenuConstants.PD_EMAIL).send_keys(keys)

    def set_pd_mobile_no(self, keys):
        self.find_by_xpath(MenuConstants.PD_MOBILE_NO).send_keys(keys)

    def set_preferred_communication_method(self, method):

        if method == "Mobile No":
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_EMAIL).click()
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_SELECTION_MOBILE_NO).click()
        else:
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_MOBILE_NO).click()
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_SELECTION_EMAIL).click()

    def pd_fill_mobile_no(self, value):
        self.click_pd_mobile_no()
        # self.wait_edit_mode(MenuConstants.PD_MOBILE_NO)
        self.clear_pd_mobile_no()
        self.set_pd_mobile_no(value)

    def pd_fill_email(self, value):
        self.click_pd_email()
        # self.wait_edit_mode(MenuConstants.PD_MOBILE_NO)
        self.clear_pd_email()
        self.set_pd_email(value)
    # endregion

    # region Preferences
    def set_default_client(self, name):
        self.click_default_client_dropdown()
        self.click_default_client_selection(name)

    def get_default_client(self):
        return self.find_by_xpath(MenuConstants.DEFAULT_CLIENT_DROP_DOWN_LIST).get_attribute('content-desc')

    def click_default_client_dropdown(self):
        self.find_by_xpath(MenuConstants.DEFAULT_CLIENT_DROP_DOWN_LIST).click()

    def click_default_client_selection(self, name):
        self.find_by_xpath(f'//android.view.View[@content-desc="{name}"]').click()

    def get_default_client_selection_xpath(self, name):
        return MenuConstants.DEFAULT_CLIENT_SELECTION_START + name + MenuConstants.DEFAULT_CLIENT_SELECTION_END

     #TODO: need to create one constant for that, currently incorrect xpath
    def click_on_go_back_button(self):
        pass
    # endregion
