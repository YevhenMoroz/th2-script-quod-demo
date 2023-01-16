from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType


class JavaApiEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, java_api_conn: str = None):
        self.environment_type = environment_type
        self.java_api_conn = java_api_conn

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod317_java_api.value:
            if EnvironmentType.quod317_java_api.value not in JavaApiEnvironment.environment_instances.keys():
                java_api_environment = JavaApiEnvironment(
                    environment_type=EnvironmentType.quod317_java_api.value,
                    java_api_conn=Connectivity.Ganymede_317_ja.value
                )
                JavaApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod317_java_api.value: java_api_environment})
            return JavaApiEnvironment.environment_instances[EnvironmentType.quod317_java_api.value]
        elif env.value == EnvironmentType.quod314_java_api.value:
            if EnvironmentType.quod314_java_api.value not in JavaApiEnvironment.environment_instances.keys():
                java_api_environment = JavaApiEnvironment(
                    environment_type=EnvironmentType.quod314_java_api.value,
                    java_api_conn=Connectivity.Luna_314_ja.value
                )
                JavaApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod314_java_api.value: java_api_environment})
            return JavaApiEnvironment.environment_instances[EnvironmentType.quod314_java_api.value]
        elif env.value == EnvironmentType.quod309_java_api.value:
            if EnvironmentType.quod309_java_api.value not in JavaApiEnvironment.environment_instances.keys():
                java_api_environment = JavaApiEnvironment(
                    environment_type=EnvironmentType.quod309_java_api.value,
                    java_api_conn=Connectivity.Kratos_309_ja.value
                )
                JavaApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod309_java_api.value: java_api_environment})
            return JavaApiEnvironment.environment_instances[EnvironmentType.quod309_java_api.value]
        else:
            raise Exception('Environment not found')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
