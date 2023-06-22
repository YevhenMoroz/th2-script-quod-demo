import time

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from test_framework.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from test_framework.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_framework.web_admin_core.pages.site.locations.locations_wizard import LocationsWizard
from test_framework.web_admin_core.pages.site.desks.desks_wizard import DesksWizard
from test_framework.web_admin_core.pages.site.locations.locations_page import LocationsPage
from test_framework.web_admin_core.pages.site.zones.zones_page import ZonesPage
from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3566(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def step_check_only_click_at_full_screen_btn(self, page):
        common_page = CommonPage(self.web_driver_container)
        common_page.click_on_full_screen_button()
        time.sleep(1)
        self.verify(f"{page} page became Full Screen", False, common_page.is_header_displayed())

        common_page.click_on_exit_full_screen_button()
        time.sleep(1)
        self.verify(f"{page} page back to Normal screen", True, common_page.is_header_displayed())

    def step_check_full_screen_after_click_on_new_btn(self, page):
        common_page = CommonPage(self.web_driver_container)
        institution_page = InstitutionsPage(self.web_driver_container)
        zones_page = ZonesPage(self.web_driver_container)
        locations_page = LocationsPage(self.web_driver_container)
        desks_page = DesksPage(self.web_driver_container)
        institution_wizard = InstitutionsWizard(self.web_driver_container)
        zones_wizard = ZonesWizard(self.web_driver_container)
        locations_wizard = LocationsWizard(self.web_driver_container)
        desks_wizard = DesksWizard(self.web_driver_container)

        common_page.click_on_full_screen_button()
        time.sleep(1)
        self.verify(f"{page} page became Full Screen", False, common_page.is_header_displayed())

        if page == "Institutions":
            institution_page.click_on_new()
        elif page == "Zones":
            zones_page.click_on_new()
        elif page == "Locations":
            locations_page.click_on_new()
        elif page == "Desks":
            desks_page.click_on_new()

        time.sleep(1)
        self.verify(f"{page} page back to Normal screen after click on [NEW] btn", True,
                    common_page.is_header_displayed())

        if page == "Institutions":
            institution_wizard.click_on_close()
            if institution_wizard.is_leave_page_confirmation_pop_up_displayed():
                institution_wizard.click_on_no_button()
        elif page == "Zones":
            zones_wizard.click_on_close()
            if zones_wizard.is_leave_page_confirmation_pop_up_displayed():
                zones_wizard.click_on_no_button()
        elif page == "Locations":
            locations_wizard.click_on_close()
            if locations_wizard.is_leave_page_confirmation_pop_up_displayed():
                locations_wizard.click_on_no_button()
        elif page == "Desks":
            desks_wizard.click_on_close_wizard()
            if desks_wizard.is_leave_page_confirmation_pop_up_displayed():
                desks_wizard.click_on_no_button()

    def step_check_full_screen_after_edit_btn(self, page):
        common_page = CommonPage(self.web_driver_container)
        institution_page = InstitutionsPage(self.web_driver_container)
        zones_page = ZonesPage(self.web_driver_container)
        locations_page = LocationsPage(self.web_driver_container)
        desks_page = DesksPage(self.web_driver_container)
        institution_wizard = InstitutionsWizard(self.web_driver_container)
        zones_wizard = ZonesWizard(self.web_driver_container)
        locations_wizard = LocationsWizard(self.web_driver_container)
        desks_wizard = DesksWizard(self.web_driver_container)

        common_page.click_on_full_screen_button()
        time.sleep(1)
        self.verify(f"{page} page became Full Screen", False, common_page.is_header_displayed())

        time.sleep(1)
        if page == "Institutions":
            institution_page.click_on_more_actions()
            institution_page.click_on_edit()
        elif page == "Zones":
            zones_page.click_on_more_actions()
            zones_page.click_on_edit()
        elif page == "Locations":
            locations_page.click_on_more_actions()
            locations_page.click_on_edit()
        elif page == "Desks":
            desks_page.click_on_more_actions()
            desks_page.click_on_edit()

        self.verify(f"{page} page back to Normal screen after click on [EDIT] btn", True,
                    common_page.is_header_displayed())

        if page == "Institutions":
            institution_wizard.click_on_close()
            if institution_wizard.is_leave_page_confirmation_pop_up_displayed():
                institution_wizard.click_on_ok_button()
        elif page == "Zones":
            zones_wizard.click_on_close()
            if zones_wizard.is_leave_page_confirmation_pop_up_displayed():
                zones_wizard.click_on_ok_button()
        elif page == "Locations":
            locations_wizard.click_on_close()
            if locations_wizard.is_leave_page_confirmation_pop_up_displayed():
                locations_wizard.click_on_ok_button()
        elif page == "Desks":
            desks_wizard.click_on_close_wizard()
            if desks_wizard.is_leave_page_confirmation_pop_up_displayed():
                desks_wizard.click_on_ok_button()

    def step_check_full_screen_after_clone_btn(self, page):
        common_page = CommonPage(self.web_driver_container)
        institution_page = InstitutionsPage(self.web_driver_container)
        zones_page = ZonesPage(self.web_driver_container)
        locations_page = LocationsPage(self.web_driver_container)
        desks_page = DesksPage(self.web_driver_container)
        institution_wizard = InstitutionsWizard(self.web_driver_container)
        zones_wizard = ZonesWizard(self.web_driver_container)
        locations_wizard = LocationsWizard(self.web_driver_container)
        desks_wizard = DesksWizard(self.web_driver_container)

        common_page.click_on_full_screen_button()
        time.sleep(1)
        self.verify(f"{page} page became Full Screen", False, common_page.is_header_displayed())

        if page == "Institutions":
            institution_page.click_on_more_actions()
            time.sleep(1)
            institution_page.click_on_clone()
            time.sleep(2)
        elif page == "Zones":
            zones_page.click_on_more_actions()
            time.sleep(1)
            zones_page.click_on_clone()
            time.sleep(2)
        elif page == "Locations":
            locations_page.click_on_more_actions()
            time.sleep(1)
            locations_page.click_on_clone()
            time.sleep(2)
        elif page == "Desks":
            desks_page.click_on_more_actions()
            time.sleep(1)
            desks_page.click_on_clone()
            time.sleep(2)

        self.verify(f"{page} page back to Normal screen after click on [CLONE] btn", True,
                    common_page.is_header_displayed())

        if page == "Institutions":
            institution_wizard.click_on_close()
            institution_wizard.click_on_no_button()
        elif page == "Zones":
            zones_wizard.click_on_close()
            zones_wizard.click_on_no_button()
        elif page == "Locations":
            locations_wizard.click_on_close()
            locations_wizard.click_on_no_button()
        elif page == "Desks":
            desks_wizard.click_on_close_wizard()
            desks_wizard.click_on_no_button()

    def step_check_full_screen_after_click_esc_btn(self, page):
        common_page = CommonPage(self.web_driver_container)
        common_page.click_on_full_screen_button()
        time.sleep(1)
        self.verify(f"{page} page became Full Screen", False, common_page.is_header_displayed())

        common_page.click_on_esc_keyboard_button()
        time.sleep(1)
        self.verify(f"{page} page back to Normal screen after click on Esc", True, common_page.is_header_displayed())

    def test_context(self):
        side_menu = SideMenu(self.web_driver_container)

        self.precondition()

        side_menu.open_institutions_page()
        time.sleep(1)
        self.step_check_only_click_at_full_screen_btn("Institutions")
        self.step_check_full_screen_after_click_on_new_btn("Institutions")
        self.step_check_full_screen_after_edit_btn("Institutions")
        self.step_check_full_screen_after_clone_btn("Institutions")
        self.step_check_full_screen_after_click_esc_btn("Institutions")

        side_menu.click_on_zones_tab()
        time.sleep(1)
        self.step_check_only_click_at_full_screen_btn("Zones")
        self.step_check_full_screen_after_click_on_new_btn("Zones")
        self.step_check_full_screen_after_edit_btn("Zones")
        self.step_check_full_screen_after_clone_btn("Zones")
        self.step_check_full_screen_after_click_esc_btn("Zones")

        side_menu.click_on_locations_tab()
        time.sleep(1)
        self.step_check_only_click_at_full_screen_btn("Locations")
        self.step_check_full_screen_after_click_on_new_btn("Locations")
        self.step_check_full_screen_after_edit_btn("Locations")
        self.step_check_full_screen_after_clone_btn("Locations")
        self.step_check_full_screen_after_click_esc_btn("Locations")

        side_menu.click_on_desks_tab()
        time.sleep(1)
        self.step_check_only_click_at_full_screen_btn("Desks")
        self.step_check_full_screen_after_click_on_new_btn("Desks")
        self.step_check_full_screen_after_edit_btn("Desks")
        self.step_check_full_screen_after_clone_btn("Desks")
        self.step_check_full_screen_after_click_esc_btn("Desks")

