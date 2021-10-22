from quod_qa.web_admin.web_admin_core.pages.client_accounts.clients.clients_constants import ClientsConstants
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsExternalSourcesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_bic_venue_act_grp_name(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BIC_VENUE_ACT_GRP_NAME, value)

    def get_bic_venue_act_grp_name(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BIC_VENUE_ACT_GRP_NAME)

    def set_dtcc_venue_act_grp_name(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_DTCC_VENUE_ACT_GRP_NAME, value)

    def get_dtcc_venue_act_grp_name(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_DTCC_VENUE_ACT_GRP_NAME)

    def set_omgeo_venue_act_grp_name(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_OMGEO_VENUE_ACT_GRP_NAME, value)

    def get_omgeo_venue_act_grp_name(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_OMGEO_VENUE_ACT_GRP_NAME)

    def set_other_venue_act_grp_name(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_OTHER_VENUE_ACT_GRP_NAME, value)

    def get_other_venue_act_grp_name(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_OTHER_VENUE_ACT_GRP_NAME)

    def set_sid_venue_act_grp_name(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_SID_VENUE_ACT_GRP_NAME, value)

    def get_sid_venue_act_grp_name(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_SID_VENUE_ACT_GRP_NAME)

    def set_tfm_venue_act_grp_name(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_TFM_VENUE_ACT_GRP_NAME, value)

    def get_tfm_venue_act_grp_name(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_TFM_VENUE_ACT_GRP_NAME)

    def set_bo_field_1(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD1, value)

    def get_bo_field_1(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD1)

    def set_bo_field_2(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD2, value)

    def get_bo_field_2(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD2)

    def set_bo_field_3(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD3, value)

    def get_bo_field_3(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD3)

    def set_bo_field_4(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD4, value)

    def get_bo_field_4(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD4)

    def set_bo_field_5(self, value):
        self.set_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD5, value)

    def get_bo_field_5(self):
        return self.get_text_by_xpath(ClientsConstants.EXTERNAL_SOURCES_TAB_BO_FIELD5)
