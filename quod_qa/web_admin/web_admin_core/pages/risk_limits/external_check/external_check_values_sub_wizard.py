from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_constants import \
    ExternalCheckConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ExternalCheckValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name(self, value):
        self.set_text_by_xpath(ExternalCheckConstants.VALUES_TAB_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ExternalCheckConstants.VALUES_TAB_NAME_XPATH)
