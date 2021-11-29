from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersRoleSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_group(self, value):
        self.set_combobox_value(UsersConstants.GROUP_AT_ROLE_SUB_WIZARD, value)

    def get_group(self):
        return self.get_text_by_xpath(UsersConstants.GROUP_AT_ROLE_SUB_WIZARD)

    def set_perm_role(self, value):
        self.set_combobox_value(UsersConstants.PERM_ROLE_AT_ROLE_SUB_WIZARD, value)

    def get_perm_role(self):
        return self.get_text_by_xpath(UsersConstants.PERM_ROLE_AT_ROLE_SUB_WIZARD)

    def set_perm_op(self, value):
        self.set_combobox_value(UsersConstants.PERM_OP_AT_ROLE_SUB_WIZARD, value)

    def get_perm_op(self):
        return self.get_text_by_xpath(UsersConstants.PERM_OP_AT_ROLE_SUB_WIZARD)

    def is_role_id_field_visible(self):
        return self.find_by_xpath(UsersConstants.ROLE_ID_AT_ROLE_SUB_WIZARD).is_displayed()

    def is_perm_role_field_visible(self):
        return self.find_by_xpath(UsersConstants.PERM_ROLE_AT_ROLE_SUB_WIZARD).is_displayed()

    def is_perm_op_field_visible(self):
        return self.find_by_xpath(UsersConstants.PERM_OP_AT_ROLE_SUB_WIZARD).is_displayed()

    def is_group_field_visible(self):
        return self.find_by_xpath(UsersConstants.GROUP_AT_ROLE_SUB_WIZARD).is_displayed()
