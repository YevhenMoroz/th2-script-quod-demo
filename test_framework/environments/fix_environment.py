from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType


class FixEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, sell_side: str = None, sell_side2: str = None, buy_side: str = None, buy_side2: str = None, feed_handler: str = None, back_office: str = None):
        self.environment_type = environment_type
        self.sell_side = sell_side
        self.sell_side2 = sell_side2
        self.buy_side = buy_side
        self.buy_side2 = buy_side2
        self.feed_handler = feed_handler
        self.back_office = back_office

    @staticmethod
    def get_instance(env: EnvironmentType):
        if env.value == EnvironmentType.quod316_ganymede_standard.value:
            if EnvironmentType.quod316_ganymede_standard.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod316_ganymede_standard.value,
                    sell_side=Connectivity.Ganymede_316_Sell_Side.value,
                    buy_side=Connectivity.Ganymede_316_Buy_Side.value,
                    feed_handler=Connectivity.Ganymede_316_Feed_Handler.value
                )
                FixEnvironment.environment_instances.update({EnvironmentType.quod316_ganymede_standard.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod316_ganymede_standard.value]
        elif env.value == EnvironmentType.quod316_ganymede_redburn.value:
            if EnvironmentType.quod316_ganymede_redburn.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod316_ganymede_redburn.value,
                    sell_side=Connectivity.Ganymede_316_Redburn.value,
                    buy_side=Connectivity.Ganymede_316_Buy_Side.value,
                    feed_handler=Connectivity.Ganymede_316_Feed_Handler.value
                )
                FixEnvironment.environment_instances.update({EnvironmentType.quod316_ganymede_redburn.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod316_ganymede_redburn.value]
        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
