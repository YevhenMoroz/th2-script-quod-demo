from test_framework.data_sets.constants import SshClientEnv
from test_framework.data_sets.environment_type import EnvironmentType
from test_framework.environments.base_environment import BaseEnvironment


class SshClientEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, host: str = None, port: str = None, user: str = None,
                 password: str = None, su_user: str = None, su_password: str = None):
        self.environment_type = environment_type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.su_user = su_user
        self.su_password = su_password

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod317_ssh_client.value:
            if EnvironmentType.quod317_ssh_client.value not in SshClientEnvironment.environment_instances.keys():
                site_environment = SshClientEnvironment(
                    environment_type=EnvironmentType.quod317_fe.value,
                    host=SshClientEnv.HOST_317.value,
                    port=SshClientEnv.PORT_317.value,
                    user=SshClientEnv.USER_317.value,
                    password=SshClientEnv.PASSWORD_317.value,
                    su_user=SshClientEnv.SU_USER_317.value,
                    su_password=SshClientEnv.SU_PASSWORD_317.value,
                )
                SshClientEnvironment.environment_instances.update({EnvironmentType.quod317_ssh_client.value: site_environment})
            return SshClientEnvironment.environment_instances[EnvironmentType.quod317_ssh_client.value]
        elif env.value == EnvironmentType.quod310_ssh_client.value:
            if EnvironmentType.quod310_ssh_client.value not in SshClientEnvironment.environment_instances.keys():
                site_environment = SshClientEnvironment(
                    environment_type=EnvironmentType.quod310_fe.value,
                    host=SshClientEnv.HOST_310.value,
                    port=SshClientEnv.PORT_310.value,
                    user=SshClientEnv.USER_310.value,
                    password=SshClientEnv.PASSWORD_310.value,
                    su_user=SshClientEnv.SU_USER_310.value,
                    su_password=SshClientEnv.SU_PASSWORD_310.value,
                )
                SshClientEnvironment.environment_instances.update({EnvironmentType.quod310_ssh_client.value: site_environment})
            return SshClientEnvironment.environment_instances[EnvironmentType.quod310_ssh_client.value]
        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
