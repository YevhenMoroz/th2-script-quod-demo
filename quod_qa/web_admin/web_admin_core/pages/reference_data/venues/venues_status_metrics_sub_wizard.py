from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class VenuesStatusMetricsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_warning_threshold(self, value):
        self.set_text_by_xpath(VenuesConstants.STATUS_METRICS_TAB_WARNING_THRESHOLD_XPATH, value)

    def get_warning_threshold(self):
        return self.get_text_by_xpath(VenuesConstants.STATUS_METRICS_TAB_WARNING_THRESHOLD_XPATH)

    def set_error_threshold(self, value):
        self.set_text_by_xpath(VenuesConstants.STATUS_METRICS_TAB_ERROR_THRESHOLD_XPATH, value)

    def get_error_threshold(self):
        return self.get_text_by_xpath(VenuesConstants.STATUS_METRICS_TAB_ERROR_THRESHOLD_XPATH)

    def click_on_enable_metric(self):
        self.find_by_xpath(VenuesConstants.STATUS_METRICS_TAB_ENABLE_METRIC_CHECKBOX_XPATH).click()

    def is_enable_metric_selected(self):
        self.is_checkbox_selected(VenuesConstants.STATUS_METRICS_TAB_ENABLE_METRIC_CHECKBOX_XPATH)

