import typing

from test_framework.data_sets.environment_type import EnvironmentType
from test_framework.environments.fe_environment import FEEnvironment
from test_framework.environments.fix_environment import FixEnvironment
from test_framework.environments.java_api_environment import JavaApiEnvironment
from test_framework.environments.read_log_envirenment import ReadLogEnvironment
from test_framework.environments.ssh_client_environment import SshClientEnvironment
from test_framework.environments.web_admin_environment import WebAdminEnvironment
from test_framework.environments.web_admin_rest_api_environment import WebAdminRestApiEnvironment
from test_framework.environments.trading_rest_api_environment import TradingRestApiEnvironment
from test_framework.environments.web_trading_environment import WebTradingEnvironment
from test_framework.environments.mobile_android_environment import MobileEnvironment

class FullEnvironment:

    def __init__(self, component_environment):
        self.__list_fix_environment = list()
        self.__list_fe_environment = list()
        self.__list_web_admin_environment = list()
        self.__list_web_admin_rest_api_environment = list()
        self.__list_trading_rest_api_environment = list()
        self.__list_web_trading_environment = list()
        self.__list_mobile_environment = list()
        self.__list_java_api_environment = list()
        self.__list_read_log_environment = list()
        self.__list_ssh_client_environment = list()

        for session_environment in component_environment:
            environment = list(session_environment)
            for instance in environment:
                if instance.tag == "fix_environment":
                    self.__list_fix_environment.append(FixEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "web_admin_environment":
                    self.__list_web_admin_environment.append(
                        WebAdminEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "fe_environment":
                    self.__list_fe_environment.append(FEEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "web_admin_rest_api_environment":
                    self.__list_web_admin_rest_api_environment.append(
                        WebAdminRestApiEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "trading_rest_api_environment":
                    self.__list_trading_rest_api_environment.append(
                        TradingRestApiEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "web_trading_environment":
                    self.__list_web_trading_environment.append(
                        WebTradingEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "mobile_environment":
                    self.__list_mobile_environment.append(
                        MobileEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "java_api_environment":
                    self.__list_java_api_environment.append(
                        JavaApiEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "read_log_environment":
                    self.__list_read_log_environment.append(
                        ReadLogEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "ssh_client_environment":
                    self.__list_ssh_client_environment.append(
                        SshClientEnvironment.get_instance(EnvironmentType[instance.text]))

    # region getters
    def get_list_fix_environment(self) -> typing.List[FixEnvironment]:
        return self.__list_fix_environment

    def get_list_fe_environment(self) -> typing.List[FEEnvironment]:
        return self.__list_fe_environment

    def get_list_web_admin_environment(self) -> typing.List[WebAdminEnvironment]:
        return self.__list_web_admin_environment

    def get_list_web_admin_rest_api_environment(self) -> typing.List[WebAdminRestApiEnvironment]:
        return self.__list_web_admin_rest_api_environment

    def get_list_trading_rest_api_environment(self) -> typing.List[TradingRestApiEnvironment]:
        return self.__list_trading_rest_api_environment

    def get_list_web_trading_environment(self) -> typing.List[WebTradingEnvironment]:
        return self.__list_web_trading_environment

    def get_list_mobile_environment(self) -> typing.List[MobileEnvironment]:
        return self.__list_mobile_environment

    def get_list_java_api_environment(self) -> typing.List[JavaApiEnvironment]:
        return self.__list_java_api_environment

    def get_list_read_log_environment(self) -> typing.List[ReadLogEnvironment]:
        return self.__list_read_log_environment

    def get_list_ssh_client_environment(self) -> typing.List[SshClientEnvironment]:
        return self.__list_ssh_client_environment
    # endregion
