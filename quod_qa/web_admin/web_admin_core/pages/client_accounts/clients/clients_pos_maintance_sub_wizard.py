from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsPosMaintenanceSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_position_maintenance(self, value):
        self.set_combobox_value(ClientsConstants.POS_MAINTENANCE_TAB_POSITION_MAINTENANCE_XPATH, value)

    def get_position_maintenance(self):
        return self.get_text_by_xpath(ClientsConstants.POS_MAINTENANCE_TAB_POSITION_MAINTENANCE_XPATH)

    def set_cash_maintenance(self, value):
        self.set_combobox_value(ClientsConstants.POS_MAINTENANCE_TAB_CASH_MAINTENANCE_XPATH, value)

    def get_cash_maintenance(self, value):
        return self.get_text_by_xpath(ClientsConstants.POS_MAINTENANCE_TAB_CASH_MAINTENANCE_XPATH)

    def set_underl_position_maintenance(self, value):
        self.set_combobox_value(ClientsConstants.POS_MAINTENANCE_TAB_UNDERL_POSITION_MAINTENANCE_XPATH, value)

    def get_underl_position_maintenance(self):
        return self.get_text_by_xpath(ClientsConstants.POS_MAINTENANCE_TAB_UNDERL_POSITION_MAINTENANCE_XPATH)

    def set_posit_price_currency(self, value):
        self.set_combobox_value(ClientsConstants.POS_MAINTENANCE_TAB_POSIT_PRICE_CURRENCY_XPATH, value)

    def get_posit_price_currency(self):
        return self.get_text_by_xpath(ClientsConstants.POS_MAINTENANCE_TAB_POSIT_PRICE_CURRENCY_XPATH)

    def click_on_validate_pos_limit(self):
        self.find_by_xpath(ClientsConstants.POS_MAINTENANCE_TAB_VALIDATE_POSLIMIT_CHECKBOX_XPATH).click()

    def click_on_validate_underl_pos_limit(self):
        self.find_by_xpath(ClientsConstants.POS_MAINTENANCE_TAB_VALIDATE_UNDERL_POSLIMIT_CHECKBOX_XPATH).click()

    def click_on_pnl_maintenance(self):
        self.find_by_xpath(ClientsConstants.POS_MAINTENANCE_TAB_PNL_MAINTENANCE_CHECKBOX_XPATH).click()
