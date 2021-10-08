from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsMiscSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_misc_0(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_0, value)

    def get_misc_0(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_0)

    def set_misc_1(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_1, value)

    def get_misc_1(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_1)

    def set_misc_2(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_2, value)

    def get_misc_2(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_2)

    def set_misc_3(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_3, value)

    def get_misc_3(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_3)

    def set_misc_4(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_4, value)

    def get_misc_4(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_4)

    def set_misc_5(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_5, value)

    def get_misc_5(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_5)

    def set_misc_6(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_6, value)

    def get_misc_6(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_6)

    def set_misc_7(self, value):
        self.set_text_by_xpath(ListingsConstants.MISC_TAB_MISC_7, value)

    def get_misc_7(self):
        self.get_text_by_xpath(ListingsConstants.MISC_TAB_MISC_7)
