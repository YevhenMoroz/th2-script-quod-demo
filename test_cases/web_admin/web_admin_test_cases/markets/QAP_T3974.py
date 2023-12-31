import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listings.listings_attachment_sub_wizard import \
    ListingsAttachmentSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_currency_sub_wizard import \
    ListingsCurrencySubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.markets.listings.listings_values_sub_wizard import \
    ListingsValuesSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_wizard import ListingsWizard
from test_framework.web_admin_core.pages.markets.listings.listings_translation_sub_wizard\
    import TranslationTab
from test_framework.web_admin_core.pages.markets.listings.listings_dark_algo_comission_sub_wizard\
    import ListingsDarkAlgoCommissionSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_market_data_sub_wizard\
    import ListingsMarketDataSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_format_sub_wizard\
    import ListingsFormatSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_feature_sub_wizard\
    import ListingsFeatureSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_market_identifies_sub_wizard\
    import ListingsMarketIdentifiersSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_validations_sub_wizard\
    import ListingsValidationsSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_status_sub_wizard\
    import ListingsStatusSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_short_shell_sub_wizard\
    import ListingsShortShellSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_misc_sub_wizard\
    import ListingsMiscSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_counterpart_sub_wizard\
    import ListingsCounterpartSubWizard
from test_framework.web_admin_core.pages.markets.listings.listings_fee_type_exemption_sub_wizard\
    import ListingsFeeTypeExemptionSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3974(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.lookup_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.instr_symbol = 'ASC'
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.security_exchange = 'CHIX'
        self.settle_type = 'Future'
        self.strike_price = str(random.randint(1, 11))
        self.language = 'German'
        self.language_description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name("venue_3")
        self.sub_venue = ''
        self.currency = self.data_set.get_currency_by_name("currency_1")
        self.instr_currency = 'AED'
        self.per_unit_comm_amt = str(random.randint(1, 11))
        self.quote_book_symbol = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.security_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.security_id_source = 'Belgian'
        self.tick_denominator = str(random.randint(1, 11))
        self.contract_multiplier = str(random.randint(1, 11))
        self.min_trade_vol = str(random.randint(1, 11))
        self.trading_phase = "210"
        self.misk_0 = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.counterpart = 'TCOther'
        self.security_exchange = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_listings_page()
        main_page = ListingsPage(self.web_driver_container)
        main_page.click_on_new()
        values_tab = ListingsValuesSubWizard(self.web_driver_container)
        values_tab.set_symbol(self.symbol)
        values_tab.set_lookup_symbol(self.lookup_symbol)
        values_tab.set_instr_symbol(self.instr_symbol)
        values_tab.set_instr_type(self.instr_type)
        values_tab.set_security_exchange(self.security_exchange)

        attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
        attachment_tab.set_venue(self.venue)

        currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
        currency_tab.set_currency(self.currency)

        wizard = ListingsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        main_page.load_listing_from_global_filter(self.lookup_symbol)
        time.sleep(2)

        main_page.click_on_more_actions()
        main_page.click_on_edit()

    def test_context(self):

        self.precondition()

        values_tab = ListingsValuesSubWizard(self.web_driver_container)
        values_tab.set_symbol(self.new_symbol)
        values_tab.set_settl_type(self.settle_type)
        values_tab.set_strike_price(self.strike_price)

        translation_tab_listing = TranslationTab.ListingTable(self.web_driver_container)
        translation_tab_listing.click_on_plus()
        translation_tab_listing.set_language(self.language)
        translation_tab_listing.set_description(self.language_description)
        translation_tab_listing.click_on_checkmark()

        attachment_tab = ListingsAttachmentSubWizard(self.web_driver_container)
        self.sub_venue = random.choice(attachment_tab.get_all_sub_venue_from_drop_menu())
        attachment_tab.set_sub_venue(self.sub_venue)

        currency_tab = ListingsCurrencySubWizard(self.web_driver_container)
        currency_tab.set_instr_currency(self.instr_currency)

        dark_algo_commission_tab = ListingsDarkAlgoCommissionSubWizard(self.web_driver_container)
        dark_algo_commission_tab.set_per_unit_comm_amt(self.per_unit_comm_amt)

        market_data_tab = ListingsMarketDataSubWizard(self.web_driver_container)
        market_data_tab.set_quote_book_symbol(self.quote_book_symbol)

        market_identifiers_tab = ListingsMarketIdentifiersSubWizard(self.web_driver_container)
        market_identifiers_tab.set_security_id(self.security_id)
        market_identifiers_tab.set_security_id_source(self.security_id_source)

        format_tab = ListingsFormatSubWizard(self.web_driver_container)
        format_tab.set_tick_denominator(self.tick_denominator)

        feature_tab = ListingsFeatureSubWizard(self.web_driver_container)
        feature_tab.set_contract_multiplier(self.contract_multiplier)
        feature_tab.click_on_async_indicator()
        feature_tab.click_on_cross_through_eur()

        validations_tab = ListingsValidationsSubWizard(self.web_driver_container)
        validations_tab.set_min_trade_vol(self.min_trade_vol)

        status_tab = ListingsStatusSubWizard(self.web_driver_container)
        status_tab.set_trading_phase(self.trading_phase)

        short_sell_tab = ListingsShortShellSubWizard(self.web_driver_container)
        short_sell_tab.click_on_allow_short_sell()

        misc_tab = ListingsMiscSubWizard(self.web_driver_container)
        misc_tab.set_misc_0(self.misk_0)

        counterpart_tab = ListingsCounterpartSubWizard(self.web_driver_container)
        counterpart_tab.set_counterpart(self.counterpart)

        fee_type_exemption = ListingsFeeTypeExemptionSubWizard(self.web_driver_container)
        fee_type_exemption.click_on_levy_fee_exemption()

        wizard = ListingsWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)

        main_page = ListingsPage(self.web_driver_container)
        main_page.set_listing_in_global_filter(self.lookup_symbol)
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(1)
        main_page.click_on_edit()
        time.sleep(2)

        translation_tab_listing.click_on_edit()

        actual_result = [values_tab.get_symbol(), values_tab.get_settl_type(),
                         values_tab.get_strike_price(), translation_tab_listing.get_language(),
                         translation_tab_listing.get_description(), attachment_tab.get_sub_venue(),
                         currency_tab.get_instr_currency(), dark_algo_commission_tab.get_per_unit_comm_amt(),
                         market_data_tab.get_quote_book_symbol(), market_identifiers_tab.get_security_id(),
                         market_identifiers_tab.get_security_id_source(), format_tab.get_tick_denominator(),
                         feature_tab.get_contract_multiplier(), feature_tab.is_async_indicator_checked(),
                         feature_tab.is_cross_through_eur_checked(), validations_tab.get_min_trade_vol(),
                         status_tab.get_trading_phase(), short_sell_tab.is_allow_short_sell_checked(),
                         misc_tab.get_misc_0(), counterpart_tab.get_counterpart(),
                         fee_type_exemption.is_levy_fee_exemption()]

        excepted_result = [self.new_symbol, self.settle_type, self.strike_price, self.language,
                           self.language_description, self.sub_venue, self.instr_currency,
                           self.per_unit_comm_amt, self.quote_book_symbol, self.security_id,
                           self.security_id_source, self.tick_denominator, self.contract_multiplier,
                           True, True, self.min_trade_vol, self.trading_phase, False, self.misk_0,
                           self.counterpart, True]

        self.verify("Edit data is correct", actual_result, excepted_result)
