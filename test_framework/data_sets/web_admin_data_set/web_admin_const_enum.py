from enum import Enum


class WebAdminUsers(Enum):
    user_1 = "adm03"
    user_2 = "adm_loca"


class WebAdminPasswords(Enum):
    password_1 = "adm03"


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


class WebAdminLocations(Enum):
    location_1 = "EAST-LOCATION-B"
    location_2 = "WEST-LOCATION-B"
    location_3 = "EAST-LOCATION-A"

class WebAdminZones(Enum):
    zone_1 = "WEST-ZONE"
    zone_2 = "EAST-ZONE"

#endregion