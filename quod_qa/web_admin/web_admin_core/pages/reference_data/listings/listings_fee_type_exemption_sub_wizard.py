from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsFeeTypeExemptionSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_stamp_fee_exemption(self):
        self.find_by_xpath(ListingsConstants.FEE_TYPE_EXEMPTION_TAB_STAMP_FEE_EXEMPTION_CHECKBOX_XPATH).click()

    def click_on_levy_fee_exemption(self):
        self.find_by_xpath(ListingsConstants.FEE_TYPE_EXEMPTION_TAB_LEVY_FEE_EXEMPTION_CHECKBOX_XPATH).click()

    def click_on_per_transac_fee_exemption(self):
        self.find_by_xpath(ListingsConstants.FEE_TYPE_EXEMPTION_TAB_PER_TRANSAC_FEE_EXEMPTION_CHECKBOX_XPATH).click()
