from test_framework.web_admin_core.pages.positions.wash_books.wash_books_constants import WashBookConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_institution(self, value):
        self.set_combobox_value(WashBookConstants.INSTITUTION_AT_ASSIGNMENT_TAB, value)

    def get_institution(self):
        return self.get_text_by_xpath(WashBookConstants.INSTITUTION_AT_ASSIGNMENT_TAB)

    def click_at_institution_link_by_name(self, name):
        self.find_by_xpath(WashBookConstants.INSTITUTION_LINK_NAME_AT_ASSIGNMENTS_TAB.format(name)).click()
