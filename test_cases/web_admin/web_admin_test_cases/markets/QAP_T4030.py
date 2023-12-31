import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_description_sub_wizard import \
    ListingGroupsDescriptionSubWizard
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_details_sub_wizard import \
    ListingGroupsDetailsSubWizard
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_page import ListingGroupsPage
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_wizard import \
    ListingGroupsWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_page import SubVenuesPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_wizard import SubVenuesWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_price_limit_profile_sub_wizard \
    import SubVenuesPriceLimitProfilesSubWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4030(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.sub_venue = self.data_set.get_sub_venue("sub_venue_1")
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.trading_status = self.data_set.get_trading_status("trading_status_1")
        self.trading_phase = self.data_set.get_trading_phase("trading_phase_1")
        self.price_limit_profile = self.data_set.get_price_limit_profile("price_limit_profile_1")
        self.tick_size_profile = self.data_set.get_tick_size_profile("tick_size_profile_1")
        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile_1")

        self.trading_reference_price_type = 'LastTradedPrice'
        self.price_limit_type = 'Price'
        self.limit_price = '1'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_subvenues_page()
        page = SubVenuesPage(self.web_driver_container)
        page.set_name_filter(self.data_set.get_sub_venue("sub_venue_1"))
        time.sleep(1)
        if not page.is_searched_subvenue_found(self.data_set.get_sub_venue("sub_venue_1")):
            page.click_on_new()
            description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
            description_sub_wizard.set_name(self.data_set.get_sub_venue("sub_venue_1"))
            description_sub_wizard.set_venue(self.data_set.get_venue_by_name("venue_2"))
            wizard = SubVenuesWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(1)

        side_menu.open_listing_groups_page()
        page = ListingGroupsPage(self.web_driver_container)

        description_sub_wizard = ListingGroupsDescriptionSubWizard(self.web_driver_container)
        details_sub_wizard = ListingGroupsDetailsSubWizard(self.web_driver_container)

        page.click_on_new()
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_sub_venue(self.sub_venue)
        description_sub_wizard.set_ext_id_venue(self.ext_id_client)
        description_sub_wizard.click_on_news_checkbox()
        details_sub_wizard.set_trading_status(self.trading_status)
        details_sub_wizard.set_trading_phase(self.trading_phase)
        if not details_sub_wizard.is_price_limit_profile_contains_filled_value(self.price_limit_profile):
            details_sub_wizard.click_on_manage_price_limit_profile_button()
            price_limit_profile = SubVenuesPriceLimitProfilesSubWizard(self.web_driver_container)
            price_limit_profile.click_on_plus_at_profiles()
            price_limit_profile.set_external_id(self.price_limit_profile)
            price_limit_profile.set_trading_reference_price_type(self.trading_reference_price_type)
            price_limit_profile.set_price_limit_type(self.price_limit_type)
            price_limit_profile.click_on_plus_at_points()
            price_limit_profile.set_limit_price(self.limit_price)
            price_limit_profile.click_on_checkmark_at_points()
            price_limit_profile.click_on_checkmark_at_profiles()
            price_limit_profile.click_on_go_back_button()
            time.sleep(1)
        details_sub_wizard.set_price_limit_profile(self.price_limit_profile)
        details_sub_wizard.set_tick_size_profile(self.tick_size_profile)
        details_sub_wizard.set_trading_phase_profile(self.trading_phase_profile)
        time.sleep(1)

    def test_context(self):
        self.precondition()
        page = ListingGroupsPage(self.web_driver_container)
        wizard = ListingGroupsWizard(self.web_driver_container)
        expected_pdf_values = [self.name,
                               self.sub_venue,
                               self.ext_id_client,
                               self.trading_status,
                               self.trading_phase,
                               self.price_limit_profile,
                               self.tick_size_profile,
                               self.trading_phase_profile]

        self.verify("Is pdf contains values", True,
                    wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_values))

        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(2)
        self.verify("Is entity saved correctly and displayed in main page", self.name, page.get_name())
