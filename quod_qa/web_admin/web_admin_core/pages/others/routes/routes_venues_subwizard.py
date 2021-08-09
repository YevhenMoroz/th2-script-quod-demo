from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_constants import RoutesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RoutesVenuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # click on
    def click_on_existing_venue(self):
        self.find_by_xpath(RoutesConstants.EXISTING_VENUE_AT_VENUES_TAB).click()

    def click_on_check_mark_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.CHECK_MARK_AT_VENUES_TAB).click()

    def click_on_plus_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.PLUS_BUTTON_AT_VENUES_TAB_XPATH).click()

    def click_on_edit_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.EDIT_VENUE_AT_VENUES_TAB_XPATH).click()

    def click_on_delete_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.DELETE_VENUE_AT_VENUES_TAB_XPATH).click()

    # venues sub-wizard tab
    # Setters
    def set_venue_filter_at_venues_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.VENUE_FILTER_AT_VALUES_TAB_XPATH, value)

    def set_venue_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.VENUE_AT_VENUES_TAB_XPATH, value)

    def set_route_venue_name_at_venues_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.ROUTE_VENUE_NAME_AT_VENUE_WIZARD_XPATH, value)

    def set_main_security_id_source_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.MAIN_SECURITY_ID_SOURCE_VALUE_AT_VENUE_WIZARD_XPATH, value)

    def set_ord_id_format_at_venues_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.ORD_ID_FORMAT_AT_VENUE_WIZARD_XPATH, value)

    def set_mic_at_venues_tab_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.MIC_AT_VENUE_WIZARD_XPATH, value)

    def set_out_bound_currency1_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.OUT_BOUND_CURRENCY1_AT_VENUE_WIZARD_XPATH, value)

    def set_out_bound_currency2_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.OUT_BOUND_CURRENCY2_AT_VENUE_WIZARD_XPATH, value)

    def set_out_bound_currency3_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.OUT_BOUND_CURRENCY3_AT_VENUE_WIZARD_XPATH, value)

    def set_out_bound_currency4_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.OUT_BOUND_CURRENCY4_AT_VENUE_WIZARD_XPATH, value)

    def set_out_bound_currency5_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.OUT_BOUND_CURRENCY5_AT_VENUE_WIZARD_XPATH, value)

    def set_max_ord_amt_currency_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.MAX_ORD_AMT_CURRENCY_AT_VENUE_WIZARD_XPATH, value)

    def set_currency_different_than_at_venues_tab(self, value):
        self.set_combobox_value(RoutesConstants.CURRENCY_DIFFERENT_THAN_AT_VENUE_WIZARD_XPATH, value)

    def set_max_ord_amt_at_venues_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.MAX_ORD_AMT_AT_VENUE_WIZARD_XPATH, value)

    def set_max_ord_qty_at_venues_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.MAX_ORD_QTY_AT_VENUE_WIZARD_XPATH, value)

    def set_display_qty_max_pct_of_ord_qty_at_venues_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.DISPLAY_QTY_MAX_PCT_OF_ORD_QTY, value)

    # setters for checkboxes
    def set_native_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.NATIVE_CHECKBOX_AT_VENUE_WIZARD_XPATH).click()

    def set_venue_mass_cancel_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.VENUE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH).click()

    def set_listing_group_mass_cancel_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.LISTING_GROUP_MASS_CANCEL_CHECKBOX_AT_VENUE_WIZARD_XPATH).click()

    def set_individual_exec_update_transac_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.INDIVIDUAL_EXEC_UPDATE_TRANSAC_AT_VENUE_WIZARD_XPATH).click()

    def set_skip_md_validations_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.SKIP_MD_VALIDATIONS_AT_VENUE_WIZARD_XPATH).click()

    def set_sub_venue_mass_cancel_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.SUBVENUE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH).click()

    def set_instr_type_mass_cancel_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.INSTR_TYPE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH).click()

    def set_support_trading_phase_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.SUPPORT_TRADING_PHASE_AT_VENUE_WIZARD_XPATH).click()

    def set_mass_cancel_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.MASS_CANCEL_CHECKBOX_AT_VENUE_WIZARD_XPATH).click()

    def set_listing_mass_cancel_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.LISTING_MASS_CANCEL_AT_VENUE_WIZARD_XPATH).click()

    def set_instr_sub_type_mass_cancel_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.INSTR_SUB_TYPE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH).click()

    def set_ord_amt_less_than_std_mkt_size_checkbox_at_venues_tab(self):
        self.find_by_xpath(RoutesConstants.ORD_AMT_LESS_THAN_STD_MKT_SIZE_AT_VENUE_WIZARD_XPATH).click()

    # getters for checkboxes
    def get_native_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.NATIVE_CHECKBOX_AT_VENUE_WIZARD_XPATH)

    def get_venue_mass_cancel_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.VENUE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH)

    def get_listing_group_mass_cancel_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.LISTING_MASS_CANCEL_AT_VENUE_WIZARD_XPATH)

    def get_individual_exec_update_transac_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.INDIVIDUAL_EXEC_UPDATE_TRANSAC_AT_VENUE_WIZARD_XPATH)

    def get_skip_md_validations_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.SKIP_MD_VALIDATIONS_AT_VENUE_WIZARD_XPATH)

    def get_sub_venue_mass_cancel_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.SUBVENUE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH)

    def get_instr_type_mass_cancel_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.INSTR_TYPE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH)

    def get_support_trading_phase_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.SUPPORT_TRADING_PHASE_AT_VENUE_WIZARD_XPATH)

    def get_mass_cancel_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.MASS_CANCEL_CHECKBOX_AT_VENUE_WIZARD_XPATH)

    def get_listing_mass_cancel_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.LISTING_MASS_CANCEL_AT_VENUE_WIZARD_XPATH)

    def get_instr_sub_type_mass_cancel_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.INSTR_SUB_TYPE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH)

    def get_ord_amt_less_than_std_mkt_size_checkbox_at_venues_tab(self):
        return self.is_checkbox_selected(RoutesConstants.ORD_AMT_LESS_THAN_STD_MKT_SIZE_AT_VENUE_WIZARD_XPATH)

    # getters
    def get_venue_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.VENUE_AT_VENUES_TAB_XPATH)

    def get_route_venue_name_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.ROUTE_VENUE_NAME_AT_VENUE_WIZARD_XPATH)

    def get_main_security_id_source_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.MAIN_SECURITY_ID_SOURCE_VALUE_AT_VENUE_WIZARD_XPATH)

    def get_ord_id_format_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.ORD_ID_FORMAT_AT_VENUE_WIZARD_XPATH)

    def get_mic_at_venues_tab_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.MIC_AT_VENUE_WIZARD_XPATH)

    def get_out_bound_currency1_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.OUT_BOUND_CURRENCY1_AT_VENUE_WIZARD_XPATH)

    def get_out_bound_currency2_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.OUT_BOUND_CURRENCY2_AT_VENUE_WIZARD_XPATH)

    def get_out_bound_currency3_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.OUT_BOUND_CURRENCY3_AT_VENUE_WIZARD_XPATH)

    def get_out_bound_currency4_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.OUT_BOUND_CURRENCY4_AT_VENUE_WIZARD_XPATH)

    def get_out_bound_currency5_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.OUT_BOUND_CURRENCY5_AT_VENUE_WIZARD_XPATH)

    def get_max_ord_amt_currency_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.MAX_ORD_AMT_CURRENCY_AT_VENUE_WIZARD_XPATH)

    def get_currency_different_than_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.CURRENCY_DIFFERENT_THAN_AT_VENUE_WIZARD_XPATH)

    def get_max_ord_amt_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.MAX_ORD_AMT_AT_VENUE_WIZARD_XPATH)

    def get_max_ord_qty_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.MAX_ORD_QTY_AT_VENUE_WIZARD_XPATH)

    def get_display_qty_max_pct_of_ord_qty_at_venues_tab(self):
        return self.get_text_by_xpath(RoutesConstants.DISPLAY_QTY_MAX_PCT_OF_ORD_QTY)

    # --trading phase wizard--
    def click_on_plus_at_trading_phase_wizard(self):
        self.find_by_xpath(RoutesConstants.PLUS_BUTTON_AT_VENUE_WIZARD_XPATH).click()

    def click_on_checkmark_at_trading_phase_wizard(self):
        self.find_by_xpath(RoutesConstants.CHECK_MARK_BUTTON_AT_VENUE_SUB_WIZARD_XPATH).click()

    def click_on_cancel_at_trading_phase_wizard(self):
        self.find_by_xpath(RoutesConstants.CLOSE_AT_VENUE_SUB_WIZARD_XPATH).click()

    def click_on_edit_at_trading_phase_wizard(self):
        self.find_by_xpath(RoutesConstants.EDIT_VENUE_AT_VENUES_TAB_XPATH).click()

    def click_on_delete_at_trading_phase_wizard(self):
        self.find_by_xpath(RoutesConstants.DELETE_BUTTON_AT_VENUE_SUB_WIZARD_XPATH).click()

    def click_on_manage_type_tif_at_trading_phase_wizard(self):
        self.find_by_xpath(RoutesConstants.MANAGE_TYPE_TIF_BUTTON_AT_VENUE_SUB_WIZARD_XPATH).click()

    # setters
    def set_trading_phase_at_trading_phase_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.TRADING_PHASE_VALUE_AT_VENUE_SUB_WIZARD_XPATH, value)

    def set_ord_type_at_trading_phase_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.ORD_TYPE_VALUE_AT_VENUE_SUB_WIZARD_XPATH, value)

    def set_output_ord_type_at_trading_phase_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.OUTPUT_ORD_TYPE_VALUE_AT_VENUE_SUB_WIZARD_XPATH, value)

    # filters
    def set_trading_phase_filter_at_trading_phase_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.TRADING_PHASE_FILTER_AT_VENUE_SUB_WIZARD_XPATH, value)

    def set_ord_type_filter_at_trading_phase_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.ORD_TYPE_FILTER_AT_VENUE_SUB_WIZARD_XPATH, value)

    def set_output_ord_type_filter_at_trading_phase_wizard(self, value):
        self.set_text_by_xpath(RoutesConstants.OUTPUT_ORD_TYPE_FILTER_AT_VENUE_SUB_WIZARD_XPATH, value)

    # getters
    def get_trading_phase_at_trading_phase_wizard(self):
        return self.find_by_xpath(RoutesConstants.TRADING_PHASE_VALUE_AT_VENUE_SUB_WIZARD_XPATH).text

    def get_ord_type_at_trading_phase_wizard(self):
        return self.find_by_xpath(RoutesConstants.ORD_TYPE_VALUE_AT_VENUE_SUB_WIZARD_XPATH).text

    def get_output_ord_type_at_trading_phase_wizard(self):
        return self.find_by_xpath(RoutesConstants.OUTPUT_ORD_TYPE_VALUE_AT_VENUE_SUB_WIZARD_XPATH).text
