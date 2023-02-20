from test_framework.data_sets.constants import DataBaseEnv
from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.environment_type import EnvironmentType


class DataBaseEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, db_host: str = None, db_name: str = None, db_user: str = None,
                 db_pass: str = None, db_type: str = None, db_port: str = None):
        self.environment_type = environment_type
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_type = db_type
        self.db_port = db_port

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod317_data_base.value:
            if EnvironmentType.quod317_data_base.value not in DataBaseEnvironment.environment_instances.keys():
                site_environment = DataBaseEnvironment(
                    environment_type=EnvironmentType.quod317_fe.value,
                    db_host=DataBaseEnv.HOST_317.value,
                    db_name=DataBaseEnv.NAME_317.value,
                    db_user=DataBaseEnv.USER_317.value,
                    db_pass=DataBaseEnv.PASS_317.value,
                    db_type=DataBaseEnv.DB_TYPE_317.value
                )
                DataBaseEnvironment.environment_instances.update({EnvironmentType.quod317_data_base.value: site_environment})
            return DataBaseEnvironment.environment_instances[EnvironmentType.quod317_data_base.value]
        elif env.value == EnvironmentType.quod316_data_base_mongo.value:
            if EnvironmentType.quod316_data_base_mongo.value not in DataBaseEnvironment.environment_instances.keys():
                site_environment = DataBaseEnvironment(
                    environment_type=EnvironmentType.quod317_fe.value,
                    db_host=DataBaseEnv.HOST_316.value,
                    db_name=DataBaseEnv.NAME_316.value,
                    db_port=DataBaseEnv.PORT_316.value,
                    db_type=DataBaseEnv.DB_TYPE_316.value
                )
                DataBaseEnvironment.environment_instances.update({EnvironmentType.quod316_data_base_mongo.value: site_environment})
            return DataBaseEnvironment.environment_instances[EnvironmentType.quod316_data_base_mongo.value]
        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result