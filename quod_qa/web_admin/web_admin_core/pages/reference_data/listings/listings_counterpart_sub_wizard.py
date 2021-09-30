from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsCounterpartSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_counterpart(self, value):
        self.set_combobox_value(ListingsConstants.COUNTERPART_TAB_COUNTERPART_XPATH, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(ListingsConstants.COUNTERPART_TAB_COUNTERPART_XPATH)
