import sys
import time
import random
import string
import traceback
from pathlib import Path

from custom import basic_custom_actions
from test_framework.core.try_exept_decorator import try_except
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_page import CounterpartsPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_party_roles_subwizard import \
    CounterpartsPartyRolesSubWizard
from test_framework.web_admin_core.pages.others.counterparts.counterparts_wizard import CounterpartsWizard

from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3405(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.party_id_source = ["BIC", "Proprietary"]
        self.venue_counterpart_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in
                                     range(2)]
        self.party_role = ["DeskID", "Exchange"]
        self.ext_id_client = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_counterparts_page()
        time.sleep(2)
        page = CounterpartsPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        party_roles_tab_wizard = CounterpartsPartyRolesSubWizard(self.web_driver_container)
        counterparts_wizard = CounterpartsWizard(self.web_driver_container)

        self.precondition()
        try:
            counterparts_wizard.click_on_plus_party_roles()
            time.sleep(2)
            party_roles_tab_wizard.set_required_fields_in_party_role_tab(self.party_id_source[0],
                                                                         self.venue_counterpart_id[0],
                                                                         self.party_role[0],
                                                                         self.ext_id_client[0])
            time.sleep(2)
            counterparts_wizard.click_on_check_mark()
            self.verify("\"Party roles\" item is created", self.venue_counterpart_id[0],
                        party_roles_tab_wizard.get_venue_counterpart_id_value_at_party_roles_tab())
        except Exception as e:
            self.verify(f"\"Party roles\" item is not created", True, e.__class__.__name__)

            try:
                counterparts_wizard.click_on_plus_party_roles()
                time.sleep(2)
                party_roles_tab_wizard.set_required_fields_in_party_role_tab(self.party_id_source[1],
                                                                             self.venue_counterpart_id[1],
                                                                             self.party_role[1],
                                                                             self.ext_id_client[1])

                counterparts_wizard.click_on_check_mark()
                time.sleep(2)
                self.verify("\"Party roles\" item equal 2", "2",
                            len(party_roles_tab_wizard.get_number_of_items_at_party_roles_tab()))
            except Exception as e:
                self.verify(f"\"Party roles\" items more than 2", True, e.__class__.__name__)

            try:
                party_roles_tab_wizard.set_venue_counterpart_id_filter_at_party_roles_tab(self.venue_counterpart_id[0])
                time.sleep(2)
                actual_result = [self.party_id_source[0], self.venue_counterpart_id[0],
                                 self.party_role[0], self.ext_id_client[0]]
                expected_result = [party_roles_tab_wizard.get_party_id_source_value_at_party_roles_tab(),
                                   party_roles_tab_wizard.get_venue_counterpart_id_value_at_party_roles_tab(),
                                   party_roles_tab_wizard.get_party_role_value_at_party_roles_tab(),
                                   party_roles_tab_wizard.get_ext_id_client_value_at_party_roles_tab()]
                self.verify(f"{self.venue_counterpart_id[0]} - set and get data is equal",
                            expected_result, actual_result)

                time.sleep(2)
                party_roles_tab_wizard.set_venue_counterpart_id_filter_at_party_roles_tab(self.venue_counterpart_id[1])
                time.sleep(2)
                actual_result = [self.party_id_source[1], self.venue_counterpart_id[1],
                                 self.party_role[1], self.ext_id_client[1]]
                expected_result = [party_roles_tab_wizard.get_party_id_source_value_at_party_roles_tab(),
                                   party_roles_tab_wizard.get_venue_counterpart_id_value_at_party_roles_tab(),
                                   party_roles_tab_wizard.get_party_role_value_at_party_roles_tab(),
                                   party_roles_tab_wizard.get_ext_id_client_value_at_party_roles_tab()]
                self.verify(f"{self.venue_counterpart_id[1]} - set and get data is equal",
                            expected_result, actual_result)
            except Exception as e:
                self.verify(f"\"Party roles\" items set and get data different", True, e.__class__.__name__)

