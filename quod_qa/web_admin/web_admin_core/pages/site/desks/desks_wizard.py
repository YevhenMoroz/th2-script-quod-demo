from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class DesksWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_save_changes(self):
        self.find_by_xpath(DesksConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(DesksConstants.REVERT_CHANGES_BUTTON_XPATH).click()
