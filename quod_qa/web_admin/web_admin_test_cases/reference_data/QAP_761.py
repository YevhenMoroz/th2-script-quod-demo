import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_description_sub_wizard import \
    ListingGroupsDescriptionSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_details_sub_wizard import \
    ListingGroupsDetailsSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_page import ListingGroupsPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listing_groups.listing_groups_wizard import \
    ListingGroupsWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_page import SubVenuesPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.subvenues.subvenues_wizard import SubVenuesWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_761(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.sub_venue = 'Forward'
        self.ext_id_client = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.trading_status = "Suspended"
        self.trading_phase = "201"
        self.price_limit_profile = "test"
        self.tick_size_profile = "0.000000010"
        self.trading_phase_profile = "JSE"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_subvenues_page()
        time.sleep(2)
        page = SubVenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
        description_sub_wizard.set_name("Forward")
        time.sleep(2)
        description_sub_wizard.set_venue("ASE")
        time.sleep(2)
        wizard = SubVenuesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        side_menu.open_listing_groups_page()
        time.sleep(2)
        page = ListingGroupsPage(self.web_driver_container)

        description_sub_wizard = ListingGroupsDescriptionSubWizard(self.web_driver_container)
        details_sub_wizard = ListingGroupsDetailsSubWizard(self.web_driver_container)

        page.click_on_new()
        time.sleep(1)
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_sub_venue(self.sub_venue)
        description_sub_wizard.set_ext_id_venue(self.ext_id_client)
        description_sub_wizard.click_on_news_checkbox()
        time.sleep(1)
        details_sub_wizard.set_trading_status(self.trading_status)
        details_sub_wizard.set_trading_phase(self.trading_phase)
        details_sub_wizard.set_price_limit_profile(self.price_limit_profile)
        details_sub_wizard.set_tick_size_profile(self.tick_size_profile)
        details_sub_wizard.set_trading_phase_profile(self.trading_phase_profile)
        time.sleep(1)

    def test_context(self):

        try:
            self.precondition()
            page = ListingGroupsPage(self.web_driver_container)
            wizard = ListingGroupsWizard(self.web_driver_container)
            expected_pdf_values = ["test",
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

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
