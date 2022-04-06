from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType


class TradingRestApiEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, session_alias_http: str = None, session_alias_web_socket: str = None):
        self.environment_type = environment_type
        self.session_alias_http = session_alias_http
        self.session_alias_web_socket = session_alias_web_socket

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod315_luna_trading_desktop.value:
            if EnvironmentType.quod315_luna_trading_desktop not in TradingRestApiEnvironment.environment_instances.keys():
                site_environment = TradingRestApiEnvironment(
                    environment_type=EnvironmentType.quod315_luna_trading_desktop.value,
                    session_alias_http=Connectivity.Luna_315_desktop_trading_http.value,
                    session_alias_web_socket=Connectivity.Luna_315_desktop_trading_web_socket.value
                )
                TradingRestApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod315_luna_trading_desktop.value: site_environment})
            return TradingRestApiEnvironment.environment_instances[EnvironmentType.quod315_luna_trading_desktop.value]
        elif env.value == EnvironmentType.quod320_kuiper_web_trading.value:
            if EnvironmentType.quod320_kuiper_web_trading not in TradingRestApiEnvironment.environment_instances.keys():
                site_environment = TradingRestApiEnvironment(
                    environment_type=EnvironmentType.quod320_kuiper_web_trading.value,
                    session_alias_http=Connectivity.Kuiper_320_web_trading_http.value,
                    session_alias_web_socket=Connectivity.Kuiper_320_web_trading_web_socket.value
                )
                TradingRestApiEnvironment.environment_instances.update(
                    {EnvironmentType.quod320_kuiper_web_trading.value: site_environment})
            return TradingRestApiEnvironment.environment_instances[EnvironmentType.quod320_kuiper_web_trading.value]
        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result