from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType
from test_framework.environments.base_environment import BaseEnvironment


class RestEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, wa_alias: str = None, web_trading_alias: str = None):
        self.environment_type = environment_type
        self.wa_alias = wa_alias
        self.web_trading_alias = web_trading_alias

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod314_luna_rest.value:
            if EnvironmentType.quod314_luna_rest.value not in RestEnvironment.environment_instances.keys():
                site_environment = RestEnvironment(
                    environment_type=EnvironmentType.quod314_luna_rest.value,
                    wa_alias=Connectivity.Luna_314_wa.value
                )
                RestEnvironment.environment_instances.update(
                    {EnvironmentType.quod314_luna_rest.value: site_environment})
            return RestEnvironment.environment_instances[EnvironmentType.quod314_luna_rest.value]
        else:
            raise Exception('No such environment')
