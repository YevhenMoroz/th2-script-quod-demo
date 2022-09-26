from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import FrontEnd
from test_framework.data_sets.environment_type import EnvironmentType


class FEEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, users: list = None, passwords: list = None, folder: str = None,
                 desks: list = None, target_server_win: str = None, main_window: str = None, login_window: str = None,
                 exe_name: str = None, desk_ids: list = None):
        self.environment_type = environment_type
        self.user_1 = users[0]
        self.user_2 = users[1] if len(users) > 1 else None
        self.user_3 = users[2] if len(users) > 2 else None
        self.password_1 = passwords[0]
        self.password_2 = passwords[1] if len(passwords) > 1 else None
        self.password_3 = passwords[2] if len(passwords) > 2 else None
        self.folder = folder
        self.desk_1 = desks[0]
        self.desk_2 = desks[1] if len(desks) > 1 else None
        self.desk_3 = desks[2] if len(desks) > 2 else None
        self.target_server_win = target_server_win
        self.main_window = main_window
        self.login_window = login_window
        self.exe_name = exe_name
        self.desk_ids = desk_ids

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod317_fe.value:
            if EnvironmentType.quod317_fe.value not in FEEnvironment.environment_instances.keys():
                site_environment = FEEnvironment(
                    environment_type=EnvironmentType.quod317_fe.value,
                    users=FrontEnd.USERS_317.value,
                    passwords=FrontEnd.PASSWORDS_317.value,
                    folder=FrontEnd.FOLDER_317.value,
                    desks=FrontEnd.DESKS_317.value,
                    target_server_win=FrontEnd.TARGET_SERVER_WIN.value,
                    main_window=FrontEnd.MAIN_WIN_NAME_317.value,
                    login_window=FrontEnd.LOGIN_WIN_NAME_317.value,
                    exe_name=FrontEnd.EXE_NAME.value,
                    desk_ids=FrontEnd.DESKS_ID_317.value
                )
                FEEnvironment.environment_instances.update({EnvironmentType.quod317_fe.value: site_environment})
            return FEEnvironment.environment_instances[EnvironmentType.quod317_fe.value]
        elif env.value == EnvironmentType.quod314_luna_fe.value:
            if EnvironmentType.quod314_luna_fe.value not in FEEnvironment.environment_instances.keys():
                site_environment = FEEnvironment(
                    environment_type=EnvironmentType.quod314_luna_fe.value,
                    users=FrontEnd.USERS_314.value,
                    passwords=FrontEnd.PASSWORDS_314.value,
                    folder=FrontEnd.FOLDER_314.value,
                    desks=FrontEnd.DESKS_314.value
                )
                FEEnvironment.environment_instances.update({EnvironmentType.quod314_luna_fe.value: site_environment})
            return FEEnvironment.environment_instances[EnvironmentType.quod314_luna_fe.value]

        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
