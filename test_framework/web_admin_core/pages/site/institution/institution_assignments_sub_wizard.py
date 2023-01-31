from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstitutionAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_zones(self, desk_name):
        self.find_by_xpath(InstitutionsConstants.ASSIGNMENTS_TAB_ZONES_LINK_XPATH.format(desk_name)).click()
        if self.is_element_present(InstitutionsConstants.CONFIRMATION_POP_UP):
            self.find_by_xpath(InstitutionsConstants.OK_BUTTON_XPATH).click()

    def click_on_user(self, user_name):
        self.find_by_xpath(InstitutionsConstants.ASSIGNMENTS_TAB_USERS_LINK_XPATH.format(user_name)).click()
        if self.is_element_present(InstitutionsConstants.CONFIRMATION_POP_UP):
            self.find_by_xpath(InstitutionsConstants.OK_BUTTON_XPATH).click()
