from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType


class ReadLogEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, read_log_conn: str = None, read_log_conn_ors: str = None):
        self.environment_type = environment_type
        self.read_log_conn = read_log_conn
        self.read_log_conn_ors = read_log_conn_ors

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod317_read_log.value:
            if EnvironmentType.quod317_read_log.value not in ReadLogEnvironment.environment_instances.keys():
                site_environment = ReadLogEnvironment(
                    environment_type=EnvironmentType.quod317_read_log.value,
                    read_log_conn=Connectivity.Ganymede_317_als_email_report.value,
                    read_log_conn_ors=Connectivity.Ganymede_317_ors_report.value
                )
                ReadLogEnvironment.environment_instances.update(
                    {EnvironmentType.quod317_read_log.value: site_environment})
            return ReadLogEnvironment.environment_instances[EnvironmentType.quod317_read_log.value]
        else:
            raise Exception('Environment not found')
