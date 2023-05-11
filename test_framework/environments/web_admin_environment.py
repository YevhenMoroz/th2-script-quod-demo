from test_framework.data_sets.constants import Connectivity
from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import WebAdminURL, WebBrowser
from test_framework.data_sets.environment_type import EnvironmentType


class WebAdminEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, web_browser: str = None, site_url: str = None):
        self.environment_type = environment_type
        self.web_browser = web_browser
        self.site_url = site_url

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod306_web_admin_saturn_chrome.value:
            if EnvironmentType.quod306_web_admin_saturn_chrome.value not in WebAdminEnvironment.environment_instances.keys():
                web_admin_environment = WebAdminEnvironment(
                    environment_type=EnvironmentType.quod306_web_admin_saturn_chrome.value,
                    web_browser=WebBrowser.chrome.value,
                    site_url=WebAdminURL.saturn_306.value
                )
                WebAdminEnvironment.environment_instances.update(
                    {EnvironmentType.quod306_web_admin_saturn_chrome.value: web_admin_environment})
            return WebAdminEnvironment.environment_instances[EnvironmentType.quod306_web_admin_saturn_chrome.value]
        elif env.value == EnvironmentType.quod310_web_admin_columbia_chrome.value:
            if EnvironmentType.quod310_web_admin_columbia_chrome.value not in WebAdminEnvironment.environment_instances.keys():
                web_admin_environment = WebAdminEnvironment(
                    environment_type=EnvironmentType.quod310_web_admin_columbia_chrome.value,
                    web_browser=WebBrowser.chrome.value,
                    site_url=WebAdminURL.columbia_310.value
                )
                WebAdminEnvironment.environment_instances.update(
                    {EnvironmentType.quod310_web_admin_columbia_chrome.value: web_admin_environment})
            return WebAdminEnvironment.environment_instances[EnvironmentType.quod310_web_admin_columbia_chrome.value]
        elif env.value == EnvironmentType.quod324_web_admin_venus_chrome.value:
            if EnvironmentType.quod324_web_admin_venus_chrome.value not in WebAdminEnvironment.environment_instances.keys():
                web_admin_environment = WebAdminEnvironment(
                    environment_type=EnvironmentType.quod324_web_admin_venus_chrome.value,
                    web_browser=WebBrowser.chrome.value,
                    site_url=WebAdminURL.venus_324.value
                )
                WebAdminEnvironment.environment_instances.update(
                    {EnvironmentType.quod324_web_admin_venus_chrome.value: web_admin_environment})
            return WebAdminEnvironment.environment_instances[EnvironmentType.quod324_web_admin_venus_chrome.value]
        elif env.value == EnvironmentType.quod306_web_admin_saturn_firefox.value:
            if EnvironmentType.quod306_web_admin_saturn_firefox.value not in WebAdminEnvironment.environment_instances.keys():
                web_admin_environment = WebAdminEnvironment(
                    environment_type=EnvironmentType.quod306_web_admin_saturn_firefox.value,
                    web_browser=WebBrowser.firefox.value,
                    site_url=WebAdminURL.saturn_306.value
                )
                WebAdminEnvironment.environment_instances.update(
                    {EnvironmentType.quod306_web_admin_saturn_chrome.value: web_admin_environment})
            return WebAdminEnvironment.environment_instances[EnvironmentType.quod306_web_admin_saturn_chrome.value]
        elif env.value == EnvironmentType.test_site_web_admin_chrome.value:
            if EnvironmentType.test_site_web_admin_chrome.value not in WebAdminEnvironment.environment_instances.keys():
                web_admin_environment = WebAdminEnvironment(
                    environment_type=EnvironmentType.test_site_web_admin_chrome.value,
                    web_browser=WebBrowser.chrome.value,
                    site_url=WebAdminURL.test_site.value
                )
                WebAdminEnvironment.environment_instances.update(
                    {EnvironmentType.test_site_web_admin_chrome.value: web_admin_environment})
            return WebAdminEnvironment.environment_instances[EnvironmentType.test_site_web_admin_chrome.value]
        else:
            raise Exception('Environment not found')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
