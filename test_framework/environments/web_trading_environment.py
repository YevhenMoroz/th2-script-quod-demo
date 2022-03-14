from test_framework.data_sets.constants import WebTradingURL
from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import WebBrowser
from test_framework.data_sets.environment_type import EnvironmentType


class WebTradingEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, web_browser: str = None, site_url: str = None):
        self.environment_type = environment_type
        self.web_browser = web_browser
        self.site_url = site_url

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod315_web_trading_luna_chrome.value:
            if EnvironmentType.quod315_web_trading_luna_chrome.value not in WebTradingEnvironment.environment_instances.keys():
                web_admin_environment = WebTradingEnvironment(
                    environment_type=EnvironmentType.quod315_web_trading_luna_chrome.value,
                    web_browser=WebBrowser.chrome.value,
                    site_url=WebTradingURL.luna_315.value
                )
                WebTradingEnvironment.environment_instances.update(
                    {EnvironmentType.quod315_web_trading_luna_chrome.value: web_admin_environment})
            return WebTradingEnvironment.environment_instances[EnvironmentType.quod315_web_trading_luna_chrome.value]
        else:
            raise Exception('Environment not found')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
