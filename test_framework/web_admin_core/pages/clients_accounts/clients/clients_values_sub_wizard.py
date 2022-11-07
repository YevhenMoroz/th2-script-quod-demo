from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_id(self, value):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_ID_XPATH, value)

    def get_id(self):
        return self.find_by_xpath(ClientsConstants.WIZARD_PAGE_TITLE_XPATH).text

    def set_name(self, value):
        self.set_text_by_xpath(ClientsConstants.VALUES_NAME_XPATH, value)

    def get_name(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_NAME_XPATH)

    def set_ext_id_client(self, value):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_EXT_ID_CLIENT_XPATH, value)

    def get_ext_id_client(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_EXT_ID_CLIENT_XPATH)

    def set_clearing_account_type(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_CLEARING_ACCOUNT_TYPE_XPATH, value)

    def get_clearing_account_type(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_CLEARING_ACCOUNT_TYPE_XPATH)

    def set_description(self, value):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_DESCRIPTION_XPATH, value)

    def get_description(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_DESCRIPTION_XPATH)

    def set_disclose_exec(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_DISCLOSE_EXEC_XPATH, value)

    def clear_disclose_exec(self):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_DISCLOSE_EXEC_XPATH, "")

    def get_disclose_exec(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_DISCLOSE_EXEC_XPATH)

    def set_client_group(self, value):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_CLIENT_GROUP_XPATH, value)

    def get_client_group(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_CLIENT_GROUP_XPATH)

    def set_invalid_tick_size_policy(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_INVALID_TICK_SIZE_POLICY_XPATH, value)

    def get_invalid_tick_size_policy(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_INVALID_TICK_SIZE_POLICY_XPATH)

    def set_virtual_account(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_VIRTUAL_ACCOUNT_XPATH, value)

    def get_virtual_account(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_VIRTUAL_ACCOUNT_XPATH)

    def set_external_odr_id_format(self, value):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_EXTERNAL_ORD_ID_FORMAT_XPATH, value)

    def get_external_ord_id_format(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_EXTERNAL_ORD_ID_FORMAT_XPATH)

    def set_booking_inst(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_BOOKING_INST_XPATH, value)

    def get_booking_inst(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_BOOKING_INST_XPATH)

    def set_allocation_preference(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_ALLOCATION_PREFERENCE_XPATH, value)

    def get_allocation_preference(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_ALLOCATION_PREFERENCE_XPATH)

    def set_confirmation_service(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_CONFIRMATION_SERVICE_XPATH, value)

    def get_confirmation_service(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_CONFIRMATION_SERVICE_XPATH)

    def set_block_approval(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_BLOCK_APPROVAL_XPATH, value)

    def get_block_approval(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_BLOCK_APPROVAL_XPATH)

    def set_rounding_direction(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_ROUNDING_DIRECTION_XPATH, value)

    def get_rounding_direction(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_ROUNDING_DIRECTION_XPATH)

    def set_fix_matching_profile(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_FIX_MATCHING_PROFILE_XPATH, value)

    def get_fix_matching_profile(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_FIX_MATCHING_PROFILE_XPATH)

    def set_counterpart(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_COUNTERPART_XPATH, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_COUNTERPART_XPATH)

    def click_on_manage_counterpart(self):
        self.find_by_xpath(ClientsConstants.VALUES_TAB_COUNTERPART_XPATH).click()

    def set_price_precision(self, value):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_PRICE_PRECISION_XPATH, value)

    def get_price_precision(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_PRICE_PRECISION_XPATH)

    def click_on_short_sell_account_checkbox(self):
        self.find_by_xpath(ClientsConstants.VALUES_TAB_SHORT_SELL_ACCOUNT_CHECKBOX_XPATH).click()

    def click_on_dummy_checkbox(self):
        self.find_by_xpath(ClientsConstants.VALUES_TAB_DUMMY_CHECKBOX_XPATH).click()

    def clear_disclose_exec_field(self):
        self.find_by_xpath(ClientsConstants.VALUES_TAB_DISCLOSE_EXEC_XPATH).clear()

    def set_allocation_matching_service(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_ALLOCATION_MATCHING_SERVICE_XPATH, value)

    def get_allocation_matching_service(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_ALLOCATION_MATCHING_SERVICE_XPATH)

    def clear_allocation_matching_service_field(self):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_ALLOCATION_MATCHING_SERVICE_XPATH, "")

    def set_external_allocation_matching_service(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_EXTERNAL_ALLOCATION_MATCHING_SERVICE_XPATH, value)

    def get_external_allocation_matching_service(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_EXTERNAL_ALLOCATION_MATCHING_SERVICE_XPATH)

    def is_external_allocation_matching_service_field_enable(self):
        return self.is_field_enabled(ClientsConstants.VALUES_TAB_EXTERNAL_ALLOCATION_MATCHING_SERVICE_XPATH)

    def click_on_manage_external_allocation_matching_service(self):
        self.find_by_xpath(ClientsConstants.VALUES_TAB_MANAGE_EXTERNAL_ALLOCATION_MATCHING_SERVICE_BUTTON_XPATH).click()

    def set_give_up_service(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_GIVE_UP_SERVICE, value)

    def get_give_up_service(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_GIVE_UP_SERVICE)

    def set_external_give_up_service(self, value):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_EXTERNAL_GIVE_UP_SERVICE, value)

    def get_external_give_up_service(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_EXTERNAL_GIVE_UP_SERVICE)

    def is_external_give_up_service_field_enable(self):
        return self.is_field_enabled(ClientsConstants.VALUES_TAB_EXTERNAL_GIVE_UP_SERVICE)

    def click_on_manage_external_give_up_service(self):
        self.find_by_xpath(ClientsConstants.VALUES_TAB_EXTERNAL_GIVE_UP_SERVICE_MANAGE_BUTTON).click()

    def set_default_account(self, name):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_DEFAULT_ACCOUNT_XPATH, name)

    def get_default_account(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_DEFAULT_ACCOUNT_XPATH)

    def clear_default_account(self):
        self.set_text_by_xpath(ClientsConstants.VALUES_TAB_DEFAULT_ACCOUNT_XPATH, "")

    def set_order_attribute(self, name):
        self.set_combobox_value(ClientsConstants.VALUES_TAB_ORDER_ATTRIBUTE, name)

    def get_order_attribute(self):
        return self.get_text_by_xpath(ClientsConstants.VALUES_TAB_ORDER_ATTRIBUTE)
