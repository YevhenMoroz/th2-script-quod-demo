import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_description_sub_wizard import \
    ListingGroupsDescriptionSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_page import ListingGroupsPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_wizard import \
    ListingGroupsWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_page import SubVenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_wizard import SubVenuesWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_market_data_sub_wizard import \
    VenuesMarketDataSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_wizard import VenuesWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2940(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.venue_name = "BATS"
        self.feed_source = "ADX"
        self.sub_venue_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.venue_name
        self.listing_group_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.listing_group_sub_venue = self.sub_venue_name

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        venues_page = VenuesPage(self.web_driver_container)
        venues_page.set_name_filter(self.venue_name)
        time.sleep(2)
        venues_page.click_on_more_actions()
        time.sleep(2)
        venues_page.click_on_edit()
        time.sleep(2)
        venues_market_data_sub_wizard = VenuesMarketDataSubWizard(self.web_driver_container)
        venues_market_data_sub_wizard.set_feed_source(self.feed_source)
        time.sleep(2)
        venues_wizard = VenuesWizard(self.web_driver_container)
        venues_wizard.click_on_save_changes()

        time.sleep(3)
        side_menu.open_subvenues_page()
        time.sleep(2)

        sub_venue_page = SubVenuesPage(self.web_driver_container)
        sub_venue_page.click_on_new()
        time.sleep(2)
        sub_venue_description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
        sub_venue_description_sub_wizard.set_name(self.sub_venue_name)
        time.sleep(2)
        sub_venue_description_sub_wizard.set_venue(self.venue)
        time.sleep(2)
        sub_venue_wizard = SubVenuesWizard(self.web_driver_container)
        sub_venue_wizard.click_on_save_changes()

        time.sleep(3)
        side_menu.open_listing_groups_page()
        time.sleep(2)

        listing_groups_page = ListingGroupsPage(self.web_driver_container)
        listing_groups_page.click_on_new()
        time.sleep(2)
        listing_groups_sub_wizard = ListingGroupsDescriptionSubWizard(self.web_driver_container)
        listing_groups_sub_wizard.set_name(self.listing_group_name)
        time.sleep(2)
        listing_groups_sub_wizard.set_sub_venue(self.sub_venue_name)
        time.sleep(2)
        listing_groups_wizard = ListingGroupsWizard(self.web_driver_container)
        listing_groups_wizard.click_on_save_changes()
        time.sleep(2)
        listing_groups_page.set_name(self.listing_group_name)
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            listing_groups_page = ListingGroupsPage(self.web_driver_container)
            self.verify("Is sub venue saved correctly in listing group", self.feed_source,
                        listing_groups_page.get_feed_source())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
