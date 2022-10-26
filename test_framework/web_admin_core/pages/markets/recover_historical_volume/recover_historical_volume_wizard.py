import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.recover_historical_volume.recover_historical_volume_constants import \
    RecoverHistoricalVolumeConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class RecoverHistoricalVolumeWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.REVERT_CHANGES_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(RecoverHistoricalVolumeConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_go_back_button(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.GO_BACK_BUTTON_XPATH).click()

    def set_listing(self, value):
        self.set_combobox_value(RecoverHistoricalVolumeConstants.WIZARD_LISTING_XPATH, value)

    def get_listing(self):
        return self.get_text_by_xpath(RecoverHistoricalVolumeConstants.WIZARD_LISTING_XPATH)

    def click_on_query_historic_data(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.WIZARD_QUERY_HISTORIC_DATA_XPATH).click()

    def click_on_subscribe_to_quote(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.WIZARD_SUBSCRIBE_TO_QUOTE_XPATH).click()

    def click_on_subscribe_to_trade(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.WIZARD_SUBSCRIBE_TO_TRADE_XPATH).click()

    def click_on_subscribe_to_depth(self):
        self.find_by_xpath(RecoverHistoricalVolumeConstants.WIZARD_SUBSCRIBE_TO_DEPTH_XPATH).click()
