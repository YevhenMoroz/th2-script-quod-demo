from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_save_changes(self):
        self.find_by_xpath(ClientTierConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(ClientTierConstants.REVERT_CHANGES_XPATH).click()

    def click_on_close_wizard(self):
        self.find_by_xpath(ClientTierConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(ClientTierConstants.OK_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(ClientTierConstants.CANCEL_BUTTON_XPATH).click()
