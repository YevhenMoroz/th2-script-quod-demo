from test_framework.data_sets.constants import WebTradingURL
from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.environment_type import EnvironmentType

class MobileEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, site_url: str = None):
        self.environment_type = environment_type
        self.site_url = site_url

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod315_web_trading_luna_chrome.value:
            if EnvironmentType.quod315_web_trading_luna_chrome.value not in MobileEnvironment.environment_instances.keys():
                web_admin_environment = MobileEnvironment(
                    environment_type=EnvironmentType.quod315_web_trading_luna_chrome.value,
                    site_url=WebTradingURL.luna_315.value
                )
                MobileEnvironment.environment_instances.update(
                    {EnvironmentType.quod315_web_trading_luna_chrome.value: web_admin_environment})
            return MobileEnvironment.environment_instances[EnvironmentType.quod315_web_trading_luna_chrome.value]
        elif env.value == EnvironmentType.quod320_web_trading_kuiper_chrome.value:
            if EnvironmentType.quod320_web_trading_kuiper_chrome.value not in MobileEnvironment.environment_instances.keys():
                web_admin_environment = MobileEnvironment(
                    environment_type=EnvironmentType.quod320_web_trading_kuiper_chrome.value,
                    site_url=WebTradingURL.kuiper_320.value
                )
                MobileEnvironment.environment_instances.update(
                    {EnvironmentType.quod320_web_trading_kuiper_chrome.value: web_admin_environment})
            return MobileEnvironment.environment_instances[EnvironmentType.quod320_web_trading_kuiper_chrome.value]
        else:
            raise Exception('Environment not found')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
