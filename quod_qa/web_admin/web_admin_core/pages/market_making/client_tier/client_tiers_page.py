import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region more actions
    def click_on_more_actions(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_MORE_ACTIONS_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(ClientTierConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_ok_xpath(self):
        self.find_by_xpath(ClientTierConstants.OK_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_CLONE_XPATH).click()

    def click_on_delete_and_confirmation(self, confirmation):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ClientTierConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ClientTierConstants.CANCEL_BUTTON_XPATH).click()

    # endregion

    # region filter setters
    def set_name(self, value):
        self.set_text_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_NAME_FILTER_XPATH, value)

    def set_core_spot_price_strategy(self, value):
        self.set_text_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_CORE_SPOT_PRICE_STRATEGY_FILTER_XPATH, value)

    def set_enabled_schedule(self, value):
        self.select_value_from_dropdown_list(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_ENABLE_SCHEDULE_FILTER_XPATH,
                                             value)

    # endregion

    def click_on_new(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_NEW_BUTTON_XPATH).click()

    def click_on_download_csv(self):
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_DOWNLOAD_CSV_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientTierConstants.MAIN_PAGE_CLIENT_TIER_DOWNLOAD_PDF_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_refresh_page(self):
        self.find_by_xpath(ClientTierConstants.REFRESH_PAGE_BUTTON_XPATH).click()