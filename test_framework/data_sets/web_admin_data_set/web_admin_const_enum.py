from enum import Enum


class WebAdminUsers(Enum):
    user_1 = "adm03"
    user_2 = "adm_loca"
    user_3 = "adm_desk"
    user_4 = "adm01"
    user_5 = "adm02"
    user_6 = "acameron"
    user_7 = "gbarett"


class WebAdminPasswords(Enum):
    password_1 = "adm03"
    password_2 = "adm02"


# region WaGeneral
class WebAdminComponentId(Enum):
    component_id_1 = "SATS"


class WebAdminAdminCommands(Enum):
    admin_command_1 = "ChangeLogLevel"
# endregion

# region WaSite
class WebAdminInstitutions(Enum):
    institution_1 = "QUOD FINANCIAL"
    institution_2 = "LOAD"

class WebAdminDesks(Enum):
    desk_1 = "DESK A"
    desk_2 = "DESK-C"
    desk_3 = "Quod Desk"


class WebAdminLocations(Enum):
    location_1 = "EAST-LOCATION-B"
    location_2 = "WEST-LOCATION-B"
    location_3 = "EAST-LOCATION-A"

class WebAdminZones(Enum):
    zone_1 = "WEST-ZONE"
    zone_2 = "EAST-ZONE"

#endregion

#region WaUsers
class WebAdminClients(Enum):
    client_1 = "CLIENT1"

class WebAdminClientType(Enum):
    client_type_1 = "Holder"

class WebAdminVenues(Enum):
    venue_1 = "AMEX"

class WebAdminEmail(Enum):
    email_1 = "test"

class WebAdminPermRole(Enum):
    perm_role_1 = "Permissions for FIX Clients"

class WebAdminFirstUserName(Enum):
    first_user_name_1 = "George"
#endregion