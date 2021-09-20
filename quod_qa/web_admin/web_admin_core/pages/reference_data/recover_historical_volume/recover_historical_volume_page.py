import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.recover_historical_volume.recover_historical_volume_constants import \
    RecoverHistoricalVolumeConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RecoverHistoricalVolumePage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(RecoverHistoricalVolumeConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(RecoverHistoricalVolumeConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(RecoverHistoricalVolumeConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.LOGOUT_BUTTON_XPATH).click()

    def set_listing(self, value):
        self.set_text_by_xpath(RecoverHistoricalVolumeConstants.MAIN_PAGE_LISTING_FILTER_XPATH, value)

    def set_query_historic_data(self, value):
        self.select_value_from_dropdown_list(
            RecoverHistoricalVolumeConstants.MAIN_PAGE_QUERY_HISTORIC_DATA_FILTER_XPATH, value)

    def set_subscribe_to_quote(self, value):
        self.select_value_from_dropdown_list(RecoverHistoricalVolumeConstants.MAIN_PAGE_SUBSCRIBE_TO_QUOTE_FILTER_XPATH,
                                             value)

    def set_subscribe_to_trade(self, value):
        self.select_value_from_dropdown_list(RecoverHistoricalVolumeConstants.MAIN_PAGE_SUBSCRIBE_TO_TRADE_FILTER_XPATH,
                                             value)

    def set_subscribe_to_depth(self, value):
        self.select_value_from_dropdown_list(RecoverHistoricalVolumeConstants.MAIN_PAGE_SUBSCRIBE_TO_DEPTH_FILTER_XPATH,
                                             value)

    def get_listing(self):
        return self.find_by_xpath(RecoverHistoricalVolumeConstants.MAIN_PAGE_LISTING_XPATH).text

    def get_query_historic_data(self):
        return self.is_checkbox_selected(RecoverHistoricalVolumeConstants.MAIN_PAGE_QUERY_HISTORIC_DATA_XPATH)

    def get_subscribe_to_quote(self):
        return self.is_checkbox_selected(RecoverHistoricalVolumeConstants.MAIN_PAGE_SUBSCRIBE_TO_QUOTE_XPATH)

    def get_subscribe_to_trade(self):
        return self.is_checkbox_selected(RecoverHistoricalVolumeConstants.MAIN_PAGE_SUBSCRIBE_TO_TRADE_XPATH)

    def get_subscribe_to_depth(self):
        return self.is_checkbox_selected(RecoverHistoricalVolumeConstants.MAIN_PAGE_SUBSCRIBE_TO_DEPTH_XPATH)
