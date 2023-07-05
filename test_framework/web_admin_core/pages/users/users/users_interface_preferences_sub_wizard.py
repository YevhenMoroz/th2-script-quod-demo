import time

from selenium.webdriver import ActionChains

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersInterfacePreferencesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)
        self.user_interface_preference_table = self._UserInterfacePreferences(web_driver_container)
        self.default_interface_preference_table = self._DefaultInterfacePreferences(web_driver_container)

    class _UserInterfacePreferences(CommonPage):
        def __init__(self, web_driver_container: WebDriverContainer):
            super().__init__(web_driver_container)

        def click_on_plus_button(self):
            """
            ActionChains helps to avoid falling test when adding several quantities at once.
            (The usual "click" method fails because after adding the first entry, the cursor remains on the "edit" button
            and the pop-up of edit btn covers half of the "+" button)
            """
            element = self.find_by_xpath(UsersConstants.PLUS_BUTTON_IN_USER_INTERFACE_PREFERENCE_TABLE)
            action = ActionChains(self.web_driver_container.get_driver())
            action.move_to_element(element)
            action.click()
            action.perform()

        def click_on_checkmark_button(self):
            self.find_by_xpath(UsersConstants.CHECKMARK_BUTTON_IN_USER_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_cancel_button(self):
            self.find_by_xpath(UsersConstants.CANCEL_BUTTON_IN_USER_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_edit_button(self):
            self.find_by_xpath(UsersConstants.EDIT_BUTTON_IN_USER_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_delete_button(self):
            self.find_by_xpath(UsersConstants.DELETE_BUTTON_IN_USER_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_download_button(self):
            self.find_by_xpath(UsersConstants.DOWNLOAD_PREFERENCES_IN_USER_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_ok_button(self):
            self.find_by_xpath(UsersConstants.OK_BUTTON_XPATH).click()

        def click_on_download_button_and_get_content(self):
            self.clear_download_directory()
            self.click_on_download_button()
            self.click_on_ok_button()
            time.sleep(2)
            return self.get_txt_context()

        def set_interface_id(self, value):
            self.set_text_by_xpath(UsersConstants.INTERFACE_ID_IN_USER_INTERFACE_PREFERENCE_TABLE, value)

        def set_interface_id_filter(self, value):
            self.set_text_by_xpath(UsersConstants.INTERFACE_ID_FILTER_IN_USER_INTERFACE_PREFERENCE_TABLE, value)

        def click_on_update_button_and_app_file(self, path_to_file):
            self.find_by_xpath(UsersConstants.UPDATE_BUTTON_IN_USER_INTERFACE_PREFERENCE_TABLE).click()
            time.sleep(1)
            self.set_upload_file_path_and_confirm(path_to_file)

    class _DefaultInterfacePreferences(CommonPage):
        def __init__(self, web_driver_container: WebDriverContainer):
            super().__init__(web_driver_container)

        def click_on_plus_button(self):
            self.find_by_xpath(UsersConstants.PLUS_BUTTON_IN_DEFAULT_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_checkmark_button(self):
            self.find_by_xpath(UsersConstants.CHECKMARK_BUTTON_IN_DEFAULT_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_cancel_button(self):
            self.find_by_xpath(UsersConstants.CANCEL_BUTTON_IN_DEFAULT_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_edit_button(self):
            self.find_by_xpath(UsersConstants.EDIT_BUTTON_IN_DEFAULT_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_delete_button(self):
            self.find_by_xpath(UsersConstants.DELETE_BUTTON_IN_DEFAULT_INTERFACE_PREFERENCE_TABLE).click()

        def click_on_download_button(self):
            self.find_by_xpath(UsersConstants.DOWNLOAD_PREFERENCES_IN_DEFAULT_INTERFACE_PREFERENCE_TABLE).click()
