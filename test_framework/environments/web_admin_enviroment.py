from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType
from test_framework.environments.base_environment import BaseEnvironment


class WebAdminEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, wa_alias: str = None):
        self.environment_type = environment_type
        self.wa_alias = wa_alias

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod314_luna_web_admin.value:
            if EnvironmentType.quod314_luna_web_admin.value not in WebAdminEnvironment.environment_instances.keys():
                site_environment = WebAdminEnvironment(
                    environment_type=EnvironmentType.quod314_luna_web_admin.value,
                    wa_alias=Connectivity.Luna_314_wa.value
                )
                WebAdminEnvironment.environment_instances.update(
                    {EnvironmentType.quod314_luna_web_admin.value: site_environment})
            return WebAdminEnvironment.environment_instances[EnvironmentType.quod314_luna_web_admin.value]
        else:
            raise Exception('No such environment')
