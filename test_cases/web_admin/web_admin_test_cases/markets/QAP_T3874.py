import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_description_sub_wizard import \
    SubVenuesDescriptionSubWizard

from test_framework.web_admin_core.pages.markets.subvenues.subvenues_page import SubVenuesPage
from test_framework.web_admin_core.pages.markets.subvenues.subvenues_wizard import SubVenuesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3874(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.feed_source = self.data_set.get_feed_source("feed_source_5")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_subvenues_page()
        page = SubVenuesPage(self.web_driver_container)
        page.click_on_new()
        description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
        description_sub_wizard.set_name(self.name)
        description_sub_wizard.set_venue(self.venue)
        wizard = SubVenuesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        page.set_name_filter(self.name)
        time.sleep(1)
        page.click_on_more_actions()
        page.click_on_edit()

    def test_context(self):
        description_sub_wizard = SubVenuesDescriptionSubWizard(self.web_driver_container)
        self.precondition()

        description_sub_wizard.set_market_data_source(self.feed_source)
        try:
            self.verify("Feed Source contains value", self.feed_source, description_sub_wizard.get_feed_source())
        except Exception as e:
            self.verify("Feed Source not contains value", True, e.__class__.__name__)
        time.sleep(2)
        try:
            self.verify("Feed Source field is not editable", False, description_sub_wizard.is_feed_source_editable())
        except Exception as e:
            self.verify("Feed Source field can be changed", True, e.__class__.__name__)
