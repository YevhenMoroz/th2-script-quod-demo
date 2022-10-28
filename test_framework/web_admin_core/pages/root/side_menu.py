import time

from test_framework.web_admin_core.pages.clients_accounts.accounts.accounts_constants import AccountsConstants
from test_framework.web_admin_core.pages.clients_accounts.cash_accounts.cash_accounts_constants import \
    CashAccountsConstants
from test_framework.web_admin_core.pages.clients_accounts.external_client_groups_ids.constants import \
    ExternalClientGroupIDsConstants
from test_framework.web_admin_core.pages.clients_accounts.client_groups.client_groups_constants import \
    ClientGroupsConstants
from test_framework.web_admin_core.pages.clients_accounts.client_lists.constants import ClientListsConstants
from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.positions.cash_positions.cash_positions_constants import \
    CashPositionsConstants
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_constants import \
    OrderVelocityLimitConstants
from test_framework.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from test_framework.web_admin_core.pages.positions.wash_books.wash_books_constants import WashBookConstants
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_constants import \
    WashBookRulesConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_constants import \
    AutoHedgerConstants
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_constants import \
    QuotingSessionsConstants
from test_framework.web_admin_core.pages.general.system_commands.system_commands_constants import \
    SystemCommandsConstants
from test_framework.web_admin_core.pages.general.entitlements.constants import \
    EntitlementsConstants
from test_framework.web_admin_core.pages.general.settings.settings_constants import SettingsConstants
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_constants import CommissionsConstants
from test_framework.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.constants import \
    AllocationMatchingProfilesConstants
from test_framework.web_admin_core.pages.middle_office.settlement_models.constants import \
    SettlementModelsConstants
from test_framework.web_admin_core.pages.order_management.execution_strategies.execution_strategies_constants import \
    ExecutionStrategiesConstants
from test_framework.web_admin_core.pages.order_management.order_management_rules.order_management_rules_constants import \
    OrderManagementRulesConstants
from test_framework.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from test_framework.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants
from test_framework.web_admin_core.pages.markets.market_data_sources.constants import \
    MarketDataSourcesConstants
from test_framework.web_admin_core.pages.markets.routes.constants import RoutesConstants
from test_framework.web_admin_core.pages.others.user_instr_symb_black_out.user_instr_symb_black_out_constants import \
    UserInstrSymbBlackOutConstants
from test_framework.web_admin_core.pages.positions.fx_positions.fx_positions_constants import FxPositionsConstants
from test_framework.web_admin_core.pages.positions.security_positions.security_positions_constants import \
    SecurityPositionsConstants
from test_framework.web_admin_core.pages.price_cleansing.crossed_venue_rates.crossed_venue_rates_constants import \
    CrossedVenueRatesConstants
from test_framework.web_admin_core.pages.price_cleansing.rates_following_trades.rates_following_trades_constants import \
    RatesFollowingTradesConstants
from test_framework.web_admin_core.pages.price_cleansing.stale_rates.stale_rates_constants import StaleRatesConstants
from test_framework.web_admin_core.pages.price_cleansing.unbalanced_rates.unbalanced_rates_constants import \
    UnbalancedRatesConstants
from test_framework.web_admin_core.pages.markets.instrument_symbols.constants import \
    InstrumentSymbolsConstants
from test_framework.web_admin_core.pages.markets.venue_lists.constants import \
    VenueListsConstants
from test_framework.web_admin_core.pages.markets.instrument_groups.constants import \
    InstrumentGroupsConstants
from test_framework.web_admin_core.pages.markets.instrument_lists.constants import \
    InstrumentListsConstants
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_constants import \
    ListingGroupsConstants
from test_framework.web_admin_core.pages.markets.listings.listings_constants import ListingsConstants
from test_framework.web_admin_core.pages.markets.recover_historical_volume.recover_historical_volume_constants import \
    RecoverHistoricalVolumeConstants
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_constants import SubVenuesConstants
from test_framework.web_admin_core.pages.markets.venues.venues_constants import VenuesConstants
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limits.cum_trading_limits_constants import \
    CumTradingLimitsConstants
from test_framework.web_admin_core.pages.risk_limits.cum_trading_limit_counters.constants import \
    CumTradingLimitCountersConstants
from test_framework.web_admin_core.pages.risk_limits.external_checks.constants import \
    ExternalChecksConstants
from test_framework.web_admin_core.pages.risk_limits.fx_position_limits.fx_position_limits_constants import \
    FxPositionsLimitsConstants
from test_framework.web_admin_core.pages.risk_limits.listing_cum_trading_limit_counters.constants import \
    ListingCumTradingLimitCountersConstants
from test_framework.web_admin_core.pages.risk_limits.position_limits.position_limits_constants import \
    PositionsLimitsConstants
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.constants import Constants \
    as RiskLimitDimensionsConstants
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.constants import \
    OrderToleranceLimitsConstants
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_constants import \
    TradingLimitsConstants
from test_framework.web_admin_core.pages.risk_limits.buying_power.constants import Constants as BuyingPower
from test_framework.web_admin_core.pages.root.root_constants import RootConstants
from test_framework.web_admin_core.pages.site.locations.locations_constants import LocationsConstants
from test_framework.web_admin_core.pages.site.zones.zones_constants import ZonesConstants

from test_framework.web_admin_core.pages.users.user_sessions.user_sessions_constants import UserSessionsConstants
from test_framework.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_framework.web_admin_core.utils.toggle_state_enum import ToggleStateEnum
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


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

    def open_page(self, page_item_selector: str, container_selector: str,
                  expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.toggle_container(container_selector, expected_state)
        self.click_menu_item(page_item_selector)

    def check_is_page_opened(self, page_title_selector: str):
        self.find_by_xpath(page_title_selector)

    def open_accounts_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ACCOUNTS_ITEM_XPATH, RootConstants.CLIENTS_ACCOUNTS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(AccountsConstants.ACCOUNTS_PAGE_TITLE_XPATH)

    def open_cash_accounts_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CASH_ACCOUNTS_ITEM_XPATH, RootConstants.CLIENTS_ACCOUNTS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(CashAccountsConstants.CASH_ACCOUNTS_PAGE_TITLE_XPATH)

    def open_client_client_groups_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.EXTERNAL_CLIENT_GROUP_IDS_ITEM_XPATH, RootConstants.CLIENTS_ACCOUNTS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ExternalClientGroupIDsConstants.EXTERNAL_CLIENT_GROUP_ID_PAGE_TITLE_XPATH)

    def open_client_groups_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENT_GROUPS_ITEM_XPATH, RootConstants.CLIENTS_ACCOUNTS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ClientGroupsConstants.CLIENT_GROUPS_PAGE_TITLE_CSS_XPATH)

    def open_client_list_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENT_LISTS_ITEM_XPATH, RootConstants.CLIENTS_ACCOUNTS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ClientListsConstants.CLIENT_LIST_PAGE_TITLE_XPATH)

    def open_clients_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENTS_ITEM_XPATH, RootConstants.CLIENTS_ACCOUNTS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ClientsConstants.CLIENTS_PAGE_TITLE_XPATH)

    def open_washbook_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.WASHBOOK_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(WashBookConstants.WASHBOOK_PAGE_TITLE_XPATH)

    def open_washbook_rules_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.WASHBOOK_RULES_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(WashBookRulesConstants.WASH_BOOK_RULES_PAGE_TITLE_XPATH)

    def open_auto_hedger_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.AUTO_HEDGER_ITEM_XPATH, RootConstants.FX_MARKET_MAKING_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(AutoHedgerConstants.AUTO_HEDGER_PAGE_TITLE_XPATH)

    def open_client_tier_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CLIENT_TIER_ITEM_XPATH, RootConstants.FX_MARKET_MAKING_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ClientTierConstants.CLIENT_TIER_PAGE_TITLE_XPATH)

    def open_quoting_sessions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.QUOTING_SESSIONS_ITEM_XPATH, RootConstants.FX_MARKET_MAKING_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(QuotingSessionsConstants.QUOTING_SESSIONS_PAGE_TITLE_XPATH)

    def open_system_commands_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SYSTEM_COMMANDS_ITEM_XPATH, RootConstants.GENERAL_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(SystemCommandsConstants.SYSTEM_COMMANDS_PAGE_TITLE_XPATH)

    def open_entitlements_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ENTITLEMENTS_ITEM_XPATH, RootConstants.GENERAL_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(EntitlementsConstants.ENTITLEMENTS_PAGE_TITLE_XPATH)

    def open_settings_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SETTINGS_ITEM_XPATH, RootConstants.GENERAL_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(SettingsConstants.SETTINGS_PAGE_TITLE_XPATH)

    def open_commissions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.COMMISSIONS_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(CommissionsConstants.COMMISSIONS_PAGE_TITLE_XPATH)

    def open_fees_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.FEES_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(FeesConstants.FEES_PAGE_TITLE_XPATH)

    def open_allocation_matching_profiles_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ALLOCATION_MATCHING_PROFILES_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(AllocationMatchingProfilesConstants.ALLOCATION_MATCHING_PROFILES_PAGE_TITLE_XPATH)

    def open_settlement_models_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SETTLEMENT_MODELS_ITEM_XPATH, RootConstants.MIDDLE_OFFICE_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(SettlementModelsConstants.SETTLEMENT_MODELS_PAGE_TITLE_XPATH)

    def open_execution_strategies_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.EXECUTION_STRATEGIES_ITEM_XPATH,
                       RootConstants.ORDER_MANAGEMENT_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ExecutionStrategiesConstants.EXECUTION_STRATEGIES_PAGE_TITLE_XPATH)

    def click_on_execution_strategies_when_order_management_tab_is_open(self):
        self.click_menu_item(RootConstants.EXECUTION_STRATEGIES_ITEM_XPATH)

    def open_order_management_rules_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ORDER_MANAGEMENT_RULES_ITEM_XPATH,
                       RootConstants.ORDER_MANAGEMENT_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(OrderManagementRulesConstants.ORDER_MANAGEMENT_RULES_TITLE_XPATH)

    def click_on_order_management_rules_when_order_management_tab_is_open(self):
        self.click_menu_item(RootConstants.ORDER_MANAGEMENT_RULES_ITEM_XPATH)

    def open_counterparts_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.COUNTERPARTS_ITEM_XPATH, RootConstants.OTHERS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(CounterpartsConstants.COUNTERPARTS_PAGE_TITLE_XPATH)

    def open_market_data_source_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.MARKET_DATA_SOURCE_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(MarketDataSourcesConstants.MARKET_DATA_SOURCE_PAGE_TITLE_XPATH)

    def open_routes_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ROUTES_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(RoutesConstants.ROUTES_PAGE_TITLE_XPATH)

    def open_user_instr_symb_black_out_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.USER_INSTR_SYMB_BLACK_OUT_ITEM_XPATH, RootConstants.OTHERS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(UserInstrSymbBlackOutConstants.USER_INSTR_SYMB_BLACK_OUT_PAGE_TITLE_XPATH)

    def open_fx_positions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.FX_POSITIONS_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(FxPositionsConstants.FX_POSITIONS_PAGE_TITLE_XPATH)

    def open_security_positions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SECURITY_POSITIONS_ITEM_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(SecurityPositionsConstants.SECURITY_POSITIONS_PAGE_TITLE_XPATH)

    def open_crossed_venue_rates_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CROSSED_VENUE_RATES_ITEM_XPATH, RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(CrossedVenueRatesConstants.CROSSED_VENUE_RATES_PAGE_TITLE_XPATH)

    def open_rates_following_trades_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.RATES_FOLLOWING_TRADES_ITEM_XPATH,
                       RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(RatesFollowingTradesConstants.RATES_FOLLOWING_TRADES_PAGE_TITLE_XPATH)

    def open_stale_rates_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.STALE_RATES_ITEM_XPATH, RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(StaleRatesConstants.STALE_RATES_PAGE_TITLE_XPATH)

    def open_unbalanced_rates_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.UNBALANCED_RATES_ITEM_XPATH, RootConstants.PRICE_CLEANSING_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(UnbalancedRatesConstants.UNBALANCED_RATES_PAGE_TITLE_XPATH)

    def open_instrument_symbols_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTRUMENT_SYMBOLS_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(InstrumentSymbolsConstants.INSTRUMENT_SYMBOLS_PAGE_TITLE_XPATH)

    def open_instrument_groups_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTRUMENT_GROUPS_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(InstrumentGroupsConstants.INSTRUMENT_GROUP_PAGE_TITLE_XPATH)

    def open_instrument_list_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTRUMENT_LIST_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(InstrumentListsConstants.INSTRUMENT_LIST_PAGE_TITLE_XPATH)

    def open_listing_groups_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.LISTING_GROUPS_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ListingGroupsConstants.LISTING_GROUPS_PAGE_TITLE_XPATH)

    def open_listings_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.LISTINGS_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ListingsConstants.LISTINGS_PAGE_TITLE_XPATH)

    def open_venue_list_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.VENUE_LISTS_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(VenueListsConstants.MainPage.TITLE_XPATH)

    def open_recover_historical_volume_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.RECOVER_HISTORICAL_VOLUME_ITEM_XPATH,
                       RootConstants.MARKETS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(RecoverHistoricalVolumeConstants.RECOVER_HISTORICAL_VOLUME_PAGE_TITLE_XPATH)

    def open_subvenues_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.SUBVENUES_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(SubVenuesConstants.SUBVENUES_PAGE_TITLE_XPATH)

    def open_venues_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.VENUES_ITEM_XPATH, RootConstants.MARKETS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(VenuesConstants.VENUES_PAGE_TITLE_XPATH)

    def open_cum_trading_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CUM_TRADING_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(CumTradingLimitsConstants.CUM_TRADING_LIMITS_PAGE_TITLE_XPATH)

    def open_cum_trading_limit_counters_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CUM_TRADING_LIMIT_COUNTER_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(CumTradingLimitCountersConstants.CUM_TRADING_LIMIT_COUNTERS_PAGE_TITLE_XPATH)

    def open_external_check_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.EXTERNAL_CHECKS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(ExternalChecksConstants.EXTERNAL_CHECKS_PAGE_TITLE_XPATH)

    def open_fx_position_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.FX_POSITION_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(FxPositionsLimitsConstants.FX_POSITIONS_LIMITS_PAGE_TITLE_XPATH)

    def open_listing_cum_trading_limit_counters_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.LISTING_CUM_TRADING_LIMIT_COUNTERS_ITEM_XPATH,
                       RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ListingCumTradingLimitCountersConstants.LISTING_CUM_TRADING_LIMIT_COUNTERS_PAGE_TITLE_XPATH)

    def open_positions_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.POSITION_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(PositionsLimitsConstants.POSITIONS_LIMITS_PAGE_TITLE_XPATH)

    def open_risk_limit_dimension_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.RISK_LIMIT_DIMENSIONS_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(RiskLimitDimensionsConstants.MainPage.TITLE)

    def open_order_tolerance_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ORDER_TOLERANCE_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(OrderToleranceLimitsConstants.ORDER_TOLERANCE_LIMITS_PAGE_TITLE_XPATH)

    def open_trading_limits_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.TRADING_LIMITS_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(TradingLimitsConstants.TRADING_LIMITS_PAGE_TITLE_XPATH)

    def open_buying_power_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.BUYING_POWER_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(BuyingPower.MainPage.PAGE_TITLE)

    def open_institutions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.INSTITUTIONS_ITEM_XPATH, RootConstants.SITE_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(InstitutionsConstants.INSTITUTIONS_PAGE_TITLE_XPATH)

    def open_zones_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ZONES_ITEM_XPATH, RootConstants.SITE_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(ZonesConstants.ZONES_PAGE_TITLE_XPATH)

    def click_on_zones_when_site_tab_is_open(self):
        self.click_menu_item(RootConstants.ZONES_ITEM_XPATH)

    def open_locations_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.LOCATIONS_ITEM_XPATH, RootConstants.SITE_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(LocationsConstants.LOCATIONS_PAGE_TITLE_XPATH)

    def click_on_locations_when_site_tab_is_open(self):
        self.click_menu_item(RootConstants.LOCATIONS_ITEM_XPATH)

    def open_desks_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.DESKS_ITEM_XPATH, RootConstants.SITE_TOGGLE_CSS_SELECTOR, container_expected_state)
        self.check_is_page_opened(DesksConstants.DESKS_PAGE_TITLE_XPATH)

    def click_on_desks_when_site_tab_is_open(self):
        self.click_menu_item(RootConstants.DESKS_ITEM_XPATH)

    def open_user_sessions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.USER_SESSIONS_ITEM_XPATH, RootConstants.USERS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(UserSessionsConstants.USER_SESSIONS_PAGE_TITLE_XPATH)

    def open_users_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.USERS_ITEM_XPATH, RootConstants.USERS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(UsersConstants.USERS_PAGE_TITLE_XPATH)

    def open_order_velocity_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.ORDER_VELOCITY_LIMIT_ITEM_XPATH, RootConstants.RISK_LIMITS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(OrderVelocityLimitConstants.ORDER_VELOCITY_LIMIT_PAGE_TITLE_XPATH)

    def open_cash_positions_page(self, container_expected_state: ToggleStateEnum = ToggleStateEnum.CLOSED):
        self.open_page(RootConstants.CASH_POSITIONS_XPATH, RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR,
                       container_expected_state)
        self.check_is_page_opened(CashPositionsConstants.CASH_POSITIONS_PAGE_TITLE_XPATH)

    def wait_for_button_to_become_active(self):
        i = 0
        while i < 30:
            if not self.is_field_enabled(ExecutionStrategiesConstants.NEW_BUTTON_AT_MAIN_MENU_XPATH):
                i += 1
                time.sleep(0.5)
            else:
                break

    def is_site_page_tab_displayed(self):
        return self.is_element_present(RootConstants.SITE_TAB_XPATH)

    def is_institutions_page_tab_displayed(self):
        if 'expanded' not in self.find_by_xpath(RootConstants.SITE_COLLAPSE_XPATH).get_attribute('class'):
            self.find_by_css_selector(RootConstants.SITE_TOGGLE_CSS_SELECTOR).click()
        return self.is_element_present(RootConstants.INSTITUTIONS_ITEM_XPATH)

    def is_zones_page_tab_displayed(self):
        if 'expanded' not in self.find_by_xpath(RootConstants.SITE_COLLAPSE_XPATH).get_attribute('class'):
            self.find_by_css_selector(RootConstants.SITE_TOGGLE_CSS_SELECTOR).click()
        return self.is_element_present(RootConstants.ZONES_ITEM_XPATH)

    def is_locations_page_tab_displayed(self):
        if 'expanded' not in self.find_by_xpath(RootConstants.SITE_COLLAPSE_XPATH).get_attribute('class'):
            self.find_by_css_selector(RootConstants.SITE_TOGGLE_CSS_SELECTOR).click()
        return self.is_element_present(RootConstants.LOCATIONS_ITEM_XPATH)

    def is_desks_page_tab_displayed(self):
        if 'expanded' not in self.find_by_xpath(RootConstants.SITE_COLLAPSE_XPATH).get_attribute('class'):
            self.find_by_css_selector(RootConstants.SITE_TOGGLE_CSS_SELECTOR).click()
        return self.is_element_present(RootConstants.DESKS_ITEM_XPATH)

    def is_washbook_page_tab_displayed(self):
        self.find_by_css_selector(RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR).click()
        time.sleep(1)
        return self.is_element_present(RootConstants.WASHBOOK_ITEM_XPATH)

    def is_washbook_rule_page_tab_displayed(self):
        self.find_by_css_selector(RootConstants.POSITIONS_TOGGLE_CSS_SELECTOR).click()
        time.sleep(1)
        return self.is_element_present(RootConstants.WASHBOOK_RULES_ITEM_XPATH)

