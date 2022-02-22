from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.web_admin_data_set.web_admin_const_enum import WebAdminUsers, \
    WebAdminPasswords, WebAdminComponentId, WebAdminAdminCommands, WebAdminDesks, WebAdminLocation


class WebAdminDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    user = WebAdminUsers
    password = WebAdminPasswords
    component_id = WebAdminComponentId
    admin_command = WebAdminAdminCommands
    desk = WebAdminDesks
    location = WebAdminLocation
