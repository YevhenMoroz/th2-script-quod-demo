from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType


class WebAdminRestApiEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, session_alias_wa: str = None):
        self.environment_type = environment_type
        self.session_alias_wa = session_alias_wa

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod314_luna_web_admin.value:
            if EnvironmentType.quod314_luna_web_admin.value not in WebAdminRestApiEnvironment.environment_instances.keys():
                site_environment = WebAdminRestApiEnvironment(
                    environment_type=EnvironmentType.quod314_luna_web_admin.value,
                    session_alias_wa=Connectivity.Luna_314_wa.value
                )
                WebAdminRestApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod314_luna_web_admin.value: site_environment})
            return WebAdminRestApiEnvironment.environment_instances[EnvironmentType.quod314_luna_web_admin.value]
        elif env.value == EnvironmentType.quod315_luna_web_admin.value:
            if EnvironmentType.quod315_luna_web_admin.value not in WebAdminRestApiEnvironment.environment_instances.keys():
                site_environment = WebAdminRestApiEnvironment(
                    environment_type=EnvironmentType.quod315_luna_web_admin.value,
                    session_alias_wa=Connectivity.Luna_315_web_admin.value
                )
                WebAdminRestApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod315_luna_web_admin.value: site_environment})
            return WebAdminRestApiEnvironment.environment_instances[EnvironmentType.quod315_luna_web_admin.value]
        elif env.value == EnvironmentType.quod317_ganymede_web_admin.value:
            if EnvironmentType.quod317_ganymede_web_admin.value not in WebAdminRestApiEnvironment.environment_instances.keys():
                site_environment = WebAdminRestApiEnvironment(
                    environment_type=EnvironmentType.quod317_ganymede_web_admin.value,
                    session_alias_wa=Connectivity.Ganymede_317_wa.value
                )
                WebAdminRestApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod317_ganymede_web_admin.value: site_environment})
            return WebAdminRestApiEnvironment.environment_instances[EnvironmentType.quod317_ganymede_web_admin.value]
        elif env.value == EnvironmentType.quod320_kuiper_web_admin.value:
            if EnvironmentType.quod320_kuiper_web_admin.value not in WebAdminRestApiEnvironment.environment_instances.keys():
                site_environment = WebAdminRestApiEnvironment(
                    environment_type=EnvironmentType.quod320_kuiper_web_admin.value,
                    session_alias_wa=Connectivity.Kuiper_320_web_admin.value
                )
                WebAdminRestApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod320_kuiper_web_admin.value: site_environment})
            return WebAdminRestApiEnvironment.environment_instances[EnvironmentType.quod320_kuiper_web_admin.value]
        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
