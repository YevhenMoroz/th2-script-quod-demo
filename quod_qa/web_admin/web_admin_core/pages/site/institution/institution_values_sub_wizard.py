from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstitutionsValuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_institution_name(self, value):
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_INSTITUTION_NAME, value)

    def get_institution_name(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_INSTITUTION_NAME)

    def set_lei(self, value):
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_LEI_NAME, value)

    def get_lei(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_LEI_NAME)

    def set_ctm_bic(self, value):
        self.set_text_by_xpath(InstitutionsConstants.VALUES_TAB_CTM_BIC_NAME, value)

    def get_ctm_bic(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_CTM_BIC_NAME)

    def set_counterpart(self, value):
        self.set_combobox_value(InstitutionsConstants.VALUES_TAB_COUNTERPART_NAME, value)

    def get_counterpart(self):
        return self.get_text_by_xpath(InstitutionsConstants.VALUES_TAB_COUNTERPART_NAME)

    def click_on_manage_counterpart(self):
        self.find_by_xpath(InstitutionsConstants.VALUES_TAB_MANAGE_COUNTERPART_BUTTON_XPATH).click()
