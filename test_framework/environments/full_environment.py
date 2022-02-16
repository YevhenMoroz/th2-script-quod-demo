from test_framework.environments.fix_environment import FixEnvironment
from test_framework.data_sets.environment_type import EnvironmentType
from test_framework.environments.fe_environment import FEEnvironment


class FullEnvironment:

    def __init__(self, component_environment):
        self.__list_fix_environment = list()
        self.__list_fe_environment = list()
        self.__list_web_admin_environment = list()
        self.__list_web_trading_environment = list()

        for session_environment in component_environment:
            environment = session_environment.getchildren()
            for instance in environment:
                if instance.tag == "fix_environment":
                    self.__list_fix_environment.append(FixEnvironment.get_instance(EnvironmentType[instance.text]))
                if instance.tag == "fe_environment":
                    self.__list_fe_environment.append(FEEnvironment.get_instance(EnvironmentType[instance.text]))

    # region getters
    def get_list_fix_environment(self):
        return self.__list_fix_environment

    def get_list_fe_environment(self):
        return self.__list_fe_environment

    def get_list_web_admin_environment(self):
        return self.__list_web_admin_environment

    def get_list_web_trading_environment(self):
        return self.__list_web_trading_environment
    # endregion
