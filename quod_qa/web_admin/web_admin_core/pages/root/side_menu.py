from quod_qa.web_admin.web_admin_core.pages.client_accounts.accounts.accounts_constants import AccountsConstants
from quod_qa.web_admin.web_admin_core.pages.client_accounts.cash_accounts.cash_accounts_constants import \
    CashAccountsConstants
from quod_qa.web_admin.web_admin_core.pages.client_accounts.client_client_groups.client_client_groups_constants import \
    ClientClientGroupsConstants
from quod_qa.web_admin.web_admin_core.pages.client_accounts.client_groups.client_groups_constants import \
    ClientGroupsConstants
from quod_qa.web_admin.web_admin_core.pages.client_accounts.client_list.client_list_constants import ClientListConstants
from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from quod_qa.web_admin.web_admin_core.pages.positions.washbook.washbook_constants import WashBookConstants
from quod_qa.web_admin.web_admin_core.pages.positions.washbook_rules.washbook_rules_constants import \
    WashbookRulesConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.auto_hedger.auto_hedger_constants import \
    AutoHedgerConstants
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from quod_qa.web_admin.web_admin_core.pages.fx_market_making.quoting_sessions.quoting_sessions_constants import \
    QuotingSessionsConstants
from quod_qa.web_admin.web_admin_core.pages.general.admin_command.admin_command_constants import AdminCommendConstants
from quod_qa.web_admin.web_admin_core.pages.general.mdentitlements.mdentitlements_constants import \
    MDEntitlementsConstants
from quod_qa.web_admin.web_admin_core.pages.general.settings.settings_constants import SettingsConstants
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_constants import CommissionsConstants
from quod_qa.web_admin.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants
from quod_qa.web_admin.web_admin_core.pages.middle_office.fix_matching_profile.fix_matching_profile_constants import \
    FixMatchingProfileConstants
from quod_qa.web_admin.web_admin_core.pages.middle_office.settlement_model.settlement_model_constants import \
    SettlementModelConstants
from quod_qa.web_admin.web_admin_core.pages.order_management.execution_strategies.execution_strategies_constants import \
    ExecutionStrategiesConstants
from quod_qa.web_admin.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from quod_qa.web_admin.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants
from quod_qa.web_admin.web_admin_core.pages.others.market_data_source.market_data_source_constants import \
    MarketDataSourceConstants
from quod_qa.web_admin.web_admin_core.pages.others.routes.routes_constants import RoutesConstants
from quod_qa.web_admin.web_admin_core.pages.others.user_instr_symb_black_out.user_instr_symb_black_out_constants import \
    UserInstrSymbBlackOutConstants
from quod_qa.web_admin.web_admin_core.pages.positions.fx_positions.fx_positions_constants import FxPositionsConstants
from quod_qa.web_admin.web_admin_core.pages.positions.security_positions.security_positions_constants import \
    SecurityPositionsConstants
from quod_qa.web_admin.web_admin_core.pages.price_cleansing.crossed_venue_rates.crossed_venue_rates_constants import \
    CrossedVenueRatesConstants
from quod_qa.web_admin.web_admin_core.pages.price_cleansing.rates_following_trades.rates_following_trades_constants import \
    RatesFollowingTradesConstants
from quod_qa.web_admin.web_admin_core.pages.price_cleansing.stale_rates.stale_rates_constants import StaleRatesConstants
from quod_qa.web_admin.web_admin_core.pages.price_cleansing.unbalanced_rates.unbalanced_rates_constants import \
    UnbalancedRatesConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.instr_symbol_info.instr_symbol_info_constants import \
    InstrSymbolInfoConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.instrument_group.instrument_group_constants import \
    InstrumentGroupConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.instrument_list.instrument_list_constants import \
    InstrumentListConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_constants import \
    ListingGroupsConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.recover_historical_volume.recover_historical_volume_constants import \
    RecoverHistoricalVolumeConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_constants import SubVenuesConstants
from quod_qa.web_admin.web_admin_core.pages.reference_data.venues.venues_constants import VenuesConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_constants import \
    CumTradingLimitsConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.cumtrdlmt_counter.cumtrdlmt_counter_constants import \
    CumTrdLmtCounterConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.external_check.external_check_constants import \
    ExternalCheckConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.fx_position_limits.fx_position_limits_constants import \
    FxPositionsLimitsConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.listing_cumtrdlmt_counter.listing_cumtrdlmt_counter_constants import \
    ListingCumTrdLmtCounterConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.position_limits.positions_limits_constants import \
    PositionsLimitsConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.price_tolerance_control.price_tolerance_control_constants import \
    PriceToleranceControlConstants
from quod_qa.web_admin.web_admin_core.pages.risk_limits.trading_limits.trading_limits_constants import \
    TradingLimitsConstants
from quod_qa.web_admin.web_admin_core.pages.root.root_constants import RootConstants

from quod_qa.web_admin.web_admin_core.pages.users.user_sessions.user_sessions_constants import UserSessionsConstants
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.utils.toggle_state_enum import ToggleStateEnum
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class SideMenu(CommonPage):

    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def toggle_container(self, selector: str, expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        if expected_state == ToggleStateEnum.CLOSED:
            container = self.find_by_css_selector(selector)
            container.click()

    def click_menu_item(self, page_item_selector: str):
        page_item = self.find_by_xpath(page_item_selector)
        page_item.click()

    def open_page(self, page_item_selector: str, container_selector: str, expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.toggle_container(container_selector, expected_state)
        self.click_menu_item(page_item_selector)

    def check_is_page_opened(self, page_title_selector: str):
        self.find_by_xpath(page_title_selector)

    def open_accounts_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ACCOUNTS_ITEM_XPATH, RootConstants.CLIENT_ACCOUNTS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(AccountsConstants.ACCOUNTS_PAGE_TITLE_XPATH)

    def open_cash_accounts_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CASH_ACCOUNTS_ITEM_XPATH, RootConstants.CLIENT_ACCOUNTS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(CashAccountsConstants.CASH_ACCOUNTS_PAGE_TITLE_XPATH)

    def open_client_client_groups_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENT_CLIENT_GROUPS_ITEM_XPATH, RootConstants.CLIENT_ACCOUNTS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ClientClientGroupsConstants.CLIENT_CLIENT_GROUPS_PAGE_TITLE_XPATH)

    def open_client_groups_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENT_GROUPS_ITEM_XPATH, RootConstants.CLIENT_ACCOUNTS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ClientGroupsConstants.CLIENT_GROUPS_PAGE_TITLE_CSS_XPATH)

    def open_client_list_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENT_LIST_ITEM_XPATH, RootConstants.CLIENT_ACCOUNTS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ClientListConstants.CLIENT_LIST_PAGE_TITLE_XPATH)

    def open_clients_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENTS_ITEM_XPATH, RootConstants.CLIENT_ACCOUNTS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ClientsConstants.CLIENTS_PAGE_TITLE_XPATH)

    def open_washbook_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.WASHBOOK_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(WashBookConstants.WASHBOOK_PAGE_TITLE_XPATH)

    def open_washbook_rules_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.WASHBOOK_RULES_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(WashbookRulesConstants.WASHBOOK_RULES_PAGE_TITLE_XPATH)

    def open_auto_hedger_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.AUTO_HEDGER_ITEM_XPATH, RootConstants.FX_MARKET_MAKING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(AutoHedgerConstants.AUTO_HEDGER_PAGE_TITLE_XPATH)

    def open_client_tier_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENT_TIER_ITEM_XPATH, RootConstants.FX_MARKET_MAKING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ClientTierConstants.CLIENT_TIER_PAGE_TITLE_XPATH)

    def open_quoting_sessions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.QUOTING_SESSIONS_ITEM_XPATH, RootConstants.FX_MARKET_MAKING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(QuotingSessionsConstants.QUOTING_SESSIONS_PAGE_TITLE_XPATH)

    def open_admin_command_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ADMIN_COMMAND_ITEM_XPATH, RootConstants.GENERAL_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(AdminCommendConstants.ADMIN_COMMAND_PAGE_TITLE_XPATH)

    def open_mdentitlements_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.MDENTITLEMENTS_ITEM_XPATH, RootConstants.GENERAL_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(MDEntitlementsConstants.MDENTITLEMENTS_PAGE_TITLE_XPATH)

    def open_settings_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SETTINGS_ITEM_XPATH, RootConstants.GENERAL_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(SettingsConstants.SETTINGS_PAGE_TITLE_XPATH)

    def open_commissions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.COMMISSIONS_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(CommissionsConstants.COMMISSIONS_PAGE_TITLE_XPATH)

    def open_fees_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.FEES_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(FeesConstants.FEES_PAGE_TITLE_XPATH)

    def open_fix_matching_profile_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.FIX_MATCHING_PROFILE_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(FixMatchingProfileConstants.FIX_MATCHING_PROFILE_PAGE_TITLE_XPATH)

    def open_settlement_model_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SETTLEMENT_MODEL_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(SettlementModelConstants.SETTLEMENT_MODEL_PAGE_TITLE_XPATH)

    def open_execution_strategies_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.EXECUTION_STRATEGIES_ITEM_XPATH, RootConstants.ORDER_MANAGEMENT_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ExecutionStrategiesConstants.EXECUTION_STRATEGIES_PAGE_TITLE_XPATH)

    def open_order_management_rules_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ORDER_MANAGEMENT_RULES_ITEM_XPATH, RootConstants.ORDER_MANAGEMENT_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(OrderManagementRulesConstants.ORDER_MANAGEMENT_RULES_TITLE_XPATH)

    def open_counterparts_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.COUNTERPARTS_ITEM_XPATH, RootConstants.OTHERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(CounterpartsConstants.COUNTERPARTS_PAGE_TITLE_XPATH)

    def open_institutions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTITUTIONS_ITEM_XPATH, RootConstants.OTHERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(InstitutionsConstants.INSTITUTIONS_PAGE_TITLE_XPATH)

    def open_market_data_source_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.MARKET_DATA_SOURCE_ITEM_XPATH, RootConstants.OTHERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(MarketDataSourceConstants.MARKET_DATA_SOURCE_PAGE_TITLE_XPATH)

    def open_routes_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ROUTES_ITEM_XPATH, RootConstants.OTHERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(RoutesConstants.ROUTES_PAGE_TITLE_XPATH)

    def open_user_instr_symb_black_out_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.USER_INSTR_SYMB_BLACK_OUT_ITEM_XPATH, RootConstants.OTHERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(UserInstrSymbBlackOutConstants.USER_INSTR_SYMB_BLACK_OUT_PAGE_TITLE_XPATH)

    def open_fx_positions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.FX_POSITIONS_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(FxPositionsConstants.FX_POSITIONS_PAGE_TITLE_XPATH)

    def open_security_positions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SECURITY_POSITIONS_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(SecurityPositionsConstants.SECURITY_POSITIONS_PAGE_TITLE_XPATH)

    def open_crossed_venue_rates_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CROSSED_VENUE_RATES_ITEM_XPATH, RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(CrossedVenueRatesConstants.CROSSED_VENUE_RATES_PAGE_TITLE_XPATH)

    def open_rates_following_trades_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.RATES_FOLLOWING_TRADES_ITEM_XPATH, RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(RatesFollowingTradesConstants.RATES_FOLLOWING_TRADES_PAGE_TITLE_XPATH)

    def open_stale_rates_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.STALE_RATES_ITEM_XPATH, RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(StaleRatesConstants.STALE_RATES_PAGE_TITLE_XPATH)

    def open_unbalanced_rates_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.UNBALANCED_RATES_ITEM_XPATH, RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(UnbalancedRatesConstants.UNBALANCED_RATES_PAGE_TITLE_XPATH)

    def open_instr_symbol_info_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTR_SYMBOL_INFO_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(InstrSymbolInfoConstants.INSTR_SYMBOL_INFO_PAGE_TITLE_XPATH)

    def open_instrument_group_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTRUMENT_GROUP_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(InstrumentGroupConstants.INSTRUMENT_GROUP_PAGE_TITLE_XPATH)

    def open_instrument_list_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTRUMENT_LIST_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(InstrumentListConstants.INSTRUMENT_LIST_PAGE_TITLE_XPATH)

    def open_listing_groups_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.LISTING_GROUPS_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ListingGroupsConstants.LISTING_GROUPS_PAGE_TITLE_XPATH)

    def open_listings_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.LISTINGS_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ListingsConstants.LISTINGS_PAGE_TITLE_XPATH)

    def open_recover_historical_volume_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.RECOVER_HISTORICAL_VOLUME_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(RecoverHistoricalVolumeConstants.RECOVER_HISTORICAL_VOLUME_PAGE_TITLE_XPATH)

    def open_subvenues_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SUBVENUES_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(SubVenuesConstants.SUBVENUES_PAGE_TITLE_XPATH)

    def open_venues_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.VENUES_ITEM_XPATH, RootConstants.REFERENCE_DATA_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(VenuesConstants.VENUES_PAGE_TITLE_XPATH)

    def open_cum_trading_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CUM_TRADING_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(CumTradingLimitsConstants.CUM_TRADING_LIMITS_PAGE_TITLE_XPATH)

    def open_cumtrdlmt_counter_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CUMTRDLMT_COUNTER_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(CumTrdLmtCounterConstants.CUMTRDLMT_COUNTER_PAGE_TITLE_XPATH)

    def open_external_check_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.EXTERNAL_CHECK_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ExternalCheckConstants.EXTERNAL_CHECK_PAGE_TITLE_XPATH)

    def open_fx_position_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.FX_POSITION_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(FxPositionsLimitsConstants.FX_POSITIONS_LIMITS_PAGE_TITLE_XPATH)

    def open_listing_cumtrdlmt_counter_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.LISTING_CUMTRDLMT_COUNTER_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ListingCumTrdLmtCounterConstants.LISTING_CUMTRDLMT_COUNTER_PAGE_TITLE_XPATH)

    def open_positions_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.POSITION_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(PositionsLimitsConstants.POSITIONS_LIMITS_PAGE_TITLE_XPATH)

    def open_price_tolerance_control_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.PRICE_TOLERANCE_CONTROL_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(PriceToleranceControlConstants.PRICE_TOLERANCE_CONTROL_PAGE_TITLE_XPATH)

    def open_trading_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.TRADING_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(TradingLimitsConstants.TRADING_LIMITS_PAGE_TITLE_XPATH)

    def open_desks_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.DESKS_ITEM_XPATH, RootConstants.USERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(DesksConstants.DESKS_PAGE_TITLE_XPATH)

    def open_user_sessions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.USER_SESSIONS_ITEM_XPATH, RootConstants.USERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(UserSessionsConstants.USER_SESSIONS_PAGE_TITLE_XPATH)

    def open_users_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.USERS_ITEM_XPATH, RootConstants.USERS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(UsersConstants.USERS_PAGE_TITLE_XPATH)
