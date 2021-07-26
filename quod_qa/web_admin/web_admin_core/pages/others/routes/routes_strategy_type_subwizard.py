from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_constants import RoutesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RoutesStrategyTypeSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_strategy_type_at_strategy_type_tab(self, value: tuple):
        result = tuple(self.set_checkbox_list(RoutesConstants.CHECKBOX_LIST_AT_STRATEGY_TYPE_TAB_XPATH, value))
        for item in range(len(result)):
            self.find_by_xpath(result[item]).click()

    def set_default_scenario_at_strategy_type_tab(self, value):
        self.set_combobox_value(RoutesConstants.DEFAULT_SCENARIO_AT_STRATEGY_TYPE_TAB_XPATH, value)

    def get_strategy_type_at_strategy_type_tab(self):
        return self.find_by_xpath(RoutesConstants.STRATEGY_TYPE_AT_STRATEGY_TYPE_TAB_XPATH).text

    def get_default_scenario_at_strategy_type_tab(self):
        return self.get_text_by_xpath(RoutesConstants.DEFAULT_SCENARIO_AT_STRATEGY_TYPE_TAB_XPATH)

    def click_on_strategy_type_at_strategy_type_tab(self):
        self.find_by_xpath(RoutesConstants.STRATEGY_TYPE_AT_STRATEGY_TYPE_TAB_XPATH).click()
