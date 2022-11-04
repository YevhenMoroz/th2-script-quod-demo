import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_description_sub_wizard import \
    ListingGroupsDescriptionSubWizard
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_page import ListingGroupsPage
from test_framework.web_admin_core.pages.markets.listing_groups.listing_groups_wizard import \
    ListingGroupsWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_page import SubVenuesPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_wizard import SubVenuesWizard
from test_framework.web_admin_core.pages.markets.venues.venues_market_data_sub_wizard import \
    VenuesMarketDataSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3873(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.venue_name = self.data_set.get_venue_by_name("venue_5")
        self.feed_source = self.data_set.get_feed_source("feed_source_8")
        self.sub_venue_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.venue_name
        self.listing_group_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.listing_group_sub_venue = self.sub_venue_name

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()
        venues_page = VenuesPage(self.web_driver_container)
        venues_page.set_name_filter(self.venue_name)
        time.sleep(1)
        venues_page.click_on_more_actions()
        venues_page.click_on_edit()
        venues_market_data_sub_wizard = VenuesMarketDataSubWizard(self.web_driver_container)
        venues_market_data_sub_wizard.set_feed_source(self.feed_source)
        venues_wizard = VenuesWizard(self.web_driver_container)
        venues_wizard.click_on_save_changes()

        time.sleep(2)
        side_menu.open_subvenues_page()

        sub_venue_page = SubVenuesPage(self.web_driver_container)
        sub_venue_page.click_on_new()
        sub_venue_description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
        sub_venue_description_sub_wizard.set_name(self.sub_venue_name)
        sub_venue_description_sub_wizard.set_venue(self.venue)
        sub_venue_wizard = SubVenuesWizard(self.web_driver_container)
        sub_venue_wizard.click_on_save_changes()

        time.sleep(2)
        side_menu.open_listing_groups_page()

        listing_groups_page = ListingGroupsPage(self.web_driver_container)
        time.sleep(2)
        listing_groups_page.click_on_new()
        listing_groups_sub_wizard = ListingGroupsDescriptionSubWizard(self.web_driver_container)
        listing_groups_sub_wizard.set_name(self.listing_group_name)
        listing_groups_sub_wizard.set_sub_venue(self.sub_venue_name)
        listing_groups_wizard = ListingGroupsWizard(self.web_driver_container)
        listing_groups_wizard.click_on_save_changes()
        listing_groups_page.set_name(self.listing_group_name)
        time.sleep(1)
        listing_groups_page.click_on_more_actions()
        listing_groups_page.click_on_edit()

    def test_context(self):
        listing_groups_page = ListingGroupsPage(self.web_driver_container)
        try:
            self.precondition()
            time.sleep(2)
            try:
                self.verify("Feed Source contains value", self.feed_source,
                            listing_groups_page.get_feed_source())
            except Exception as e:
                self.verify("Feed Source not contains value", True, e.__class__.__name__)
            time.sleep(2)
            try:
                self.verify("Feed Source field is not editable", False,
                            listing_groups_page.is_feed_source_field_editable())
            except Exception as e:
                self.verify("Feed Source field can be changed", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
