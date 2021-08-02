from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstitutionsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)


    def click_on_save_changes(self):
        self.find_by_xpath(InstitutionsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(InstitutionsConstants.REVERT_CHANGES_BUTTON_XPATH).click()

    def set_institution_name(self, value):
        self.set_text_by_xpath(InstitutionsConstants.INSTITUTION_NAME_XPATH, value)

    def get_institution_name(self):
        return self.get_text_by_xpath(InstitutionsConstants.INSTITUTION_NAME_XPATH)

    def set_lei(self, value):
        self.set_text_by_xpath(InstitutionsConstants.LEI_XPATH, value)

    def get_lei(self):
        return self.get_text_by_xpath(InstitutionsConstants.LEI_XPATH)

    def set_ctm_bic(self, value):
        self.set_text_by_xpath(InstitutionsConstants.CTM_BIC_XPATH, value)

    def get_ctm_bic(self):
        return self.get_text_by_xpath(InstitutionsConstants.CTM_BIC_XPATH)

    def set_counterpart(self, value):
        self.set_combobox_value(InstitutionsConstants.COUNTERPART_XPATH, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(InstitutionsConstants.COUNTERPART_XPATH)
