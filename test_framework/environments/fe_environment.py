from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import FrontEnd
from test_framework.data_sets.environment_type import EnvironmentType


class FEEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, user: str = None, password: str = None, path: str = None):
        self.environment_type = environment_type
        self.user = user
        self.password = password
        self.path = path

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod317_fe.value:
            if EnvironmentType.quod317_fe.value not in FEEnvironment.environment_instances.keys():
                site_environment = FEEnvironment(
                    environment_type=EnvironmentType.quod317_fe.value,
                    user=FrontEnd.USER_317.value,
                    password=FrontEnd.PASSWORD_317.value,
                    path=FrontEnd.FOLDER_317.value
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
