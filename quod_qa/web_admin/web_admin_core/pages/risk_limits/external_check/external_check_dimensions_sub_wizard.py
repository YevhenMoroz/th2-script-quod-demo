from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_constants import \
    ExternalCheckConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExternalCheckDimensionsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)


    def set_venue(self, value):
        self.set_combobox_value(ExternalCheckConstants.DIMENSIONS_VENUE_XPATH, value)

    def get_venue(self):
        return self.get_text_by_xpath(ExternalCheckConstants.DIMENSIONS_VENUE_XPATH)

    def set_client(self, value):
        self.set_combobox_value(ExternalCheckConstants.DIMENSIONS_CLIENT_XPATH,value)

    def get_client(self):
        return self.get_text_by_xpath(ExternalCheckConstants.DIMENSIONS_CLIENT_XPATH)

    def set_instr_type(self, value):
        self.set_combobox_value(ExternalCheckConstants.DIMENSIONS_INSTR_TYPE_XPATH, value)

    def get_instr_type(self):
        return self.get_text_by_xpath(ExternalCheckConstants.DIMENSIONS_INSTR_TYPE_XPATH)

    def set_client_group(self, value):
        self.set_combobox_value(ExternalCheckConstants.DIMENSIONS_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(ExternalCheckConstants.DIMENSIONS_CLIENT_GROUP_XPATH)