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


class WebAdminDesks(Enum):
    desk_1 = "DESK A"


class WebAdminLocation(Enum):
    location_1 = "EAST-LOCATION-B"
# endregion
