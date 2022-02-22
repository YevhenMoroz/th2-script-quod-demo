from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import FrontEnd
from test_framework.data_sets.environment_type import EnvironmentType


class FEEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, users: list = None, passwords: list = None, folder: str = None,
                 desks: list = None):
        self.environment_type = environment_type
        self.user_1 = users[0]
        self.user_2 = users[1]
        self.user_3 = users[2]
        self.password_1 = passwords[0]
        self.password_2 = passwords[1]
        self.password_3 = passwords[2]
        self.folder = folder
        self.desk_1 = desks[0]
        self.desk_2 = desks[1]

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod317_fe.value:
            if EnvironmentType.quod317_fe.value not in FEEnvironment.environment_instances.keys():
                site_environment = FEEnvironment(
                    environment_type=EnvironmentType.quod317_fe.value,
                    users=FrontEnd.USERS_317.value,
                    passwords=FrontEnd.PASSWORDS_317.value,
                    folder=FrontEnd.FOLDER_317.value,
                    desks=FrontEnd.DESKS_317.value
                )
                FEEnvironment.environment_instances.update({EnvironmentType.quod317_fe.value: site_environment})
            return FEEnvironment.environment_instances[EnvironmentType.quod317_fe.value]

        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
