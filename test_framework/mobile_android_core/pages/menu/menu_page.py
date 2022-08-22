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
            print (self.get_attribute_of_element_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_EMAIL,"clickable"))
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_EMAIL).click()
            self.appium_driver.wait_time(1)
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_SELECTION_MOBILE_NO).click()
        else:
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_DROPDOWN_MOBILE_NO).click()
            self.appium_driver.wait_time(1)
            self.find_by_xpath(MenuConstants.PD_PREFERRED_COMMUNICATION_METHOD_SELECTION_EMAIL).click()
        self.appium_driver.wait_time(1)

    def pd_fill_mobile_no(self, value):
        self.click_pd_mobile_no()
        self.clear_pd_mobile_no()
        self.set_pd_mobile_no(value)

    def pd_fill_email(self, value):
        self.click_pd_email()
        self.clear_pd_email()
        self.set_pd_email(value)
    # endregion

    # region Preferences
    def set_default_client(self):
        pass

    def get_default_client(self):
        pass

     #TODO: need to create one constant for that, currently incorrect xpath
    def click_on_go_back_button(self):
        pass
    # endregion
