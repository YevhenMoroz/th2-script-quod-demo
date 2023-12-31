import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.price_cleansing.crossed_reference_rates.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_BUTTON).click()

    def click_on_ok_button(self):
        self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.Wizard.CANCEL_BUTTON).click()

    def click_on_save_changes(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(Constants.Wizard.CLEAR_CHANGES_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(1)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        return True if self.find_by_xpath(Constants.Wizard.FOOTER_ERROR).text == "Incorrect or missing values" \
            else False


class ValuesTab(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.NAME)

    def click_on_remove_detected_price_update_checkbox(self):
        self.find_by_xpath(Constants.Wizard.ValuesTab.REMOVE_DETECTED_PRICE_UPDATES_CHECKBOX).click()

    def set_reference_venues(self, value):
        self.set_multiselect_field_value(Constants.Wizard.ValuesTab.REFERENCE_VENUES, value)

    def get_reference_venues(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.REFERENCE_VENUES)

    def get_all_reference_venues_from_drop_menu(self):
        self.find_by_xpath(Constants.Wizard.ValuesTab.REFERENCE_VENUES).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.ValuesTab.REFERENCE_VENUES_NAME_IN_DROP_DOWN)


class DimensionsTab(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_venue(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.VENUE, value)

    def get_venue(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.VENUE)

    def set_listing(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.LISTING, value)

    def get_listing(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.LISTING)

    def set_instr_type(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.INSTR_TYPE, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.INSTR_TYPE)

    def set_symbol(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.SYMBOL, value)

    def get_symbol(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.SYMBOL)

