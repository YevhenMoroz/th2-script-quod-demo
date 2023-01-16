from test_framework.environments.base_environment import BaseEnvironment
from test_framework.data_sets.constants import Connectivity
from test_framework.data_sets.environment_type import EnvironmentType


class FixEnvironment(BaseEnvironment):
    environment_instances = {}

    def __init__(self, environment_type: str = None, sell_side: str = None, sell_side2: str = None,
                 buy_side: str = None, buy_side2: str = None, feed_handler: str = None, drop_copy: str = None,
                 sell_side_rfq: str = None, sell_side_esp: str = None, buy_side_esp: str = None,
                 feed_handler2: str = None, sell_side_cnx: str = None, buy_side_md: str = None,
                 external_validation: str = None):
        self.environment_type = environment_type
        self.sell_side = sell_side
        self.sell_side2 = sell_side2
        self.buy_side = buy_side
        self.buy_side2 = buy_side2
        self.feed_handler = feed_handler
        self.drop_copy = drop_copy
        self.sell_side_rfq = sell_side_rfq
        self.sell_side_esp = sell_side_esp
        self.buy_side_esp = buy_side_esp
        self.feed_handler2 = feed_handler2
        self.sell_side_cnx = sell_side_cnx
        self.buy_side_md = buy_side_md
        self.external_validation = external_validation

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
                FixEnvironment.environment_instances.update(
                    {EnvironmentType.quod316_ganymede_standard.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod316_ganymede_standard.value]
        elif env.value == EnvironmentType.quod316_ganymede_redburn.value:
            if EnvironmentType.quod316_ganymede_redburn.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod316_ganymede_redburn.value,
                    sell_side=Connectivity.Ganymede_316_Sell_Side_Redburn.value,
                    buy_side=Connectivity.Ganymede_316_Buy_Side_Redburn.value,
                    feed_handler=Connectivity.Ganymede_316_Feed_Handler.value
                )
                FixEnvironment.environment_instances.update(
                    {EnvironmentType.quod316_ganymede_redburn.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod316_ganymede_redburn.value]
        elif env.value == EnvironmentType.quod314_luna_standard.value:
            if EnvironmentType.quod314_luna_standard.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod314_luna_standard.value,
                    sell_side_esp=Connectivity.Luna_314_ss_esp.value,
                    sell_side_rfq=Connectivity.Luna_314_ss_rfq.value,
                    buy_side_esp=Connectivity.Luna_314_ss_esp_t.value,
                    feed_handler=Connectivity.Luna_314_Feed_Handler.value,
                    feed_handler2=Connectivity.Luna_314_Feed_Handler_Q.value,
                    drop_copy=Connectivity.Luna_314_dc.value,
                    buy_side_md=Connectivity.Luna_314_bs_md.value,
                    sell_side_cnx=Connectivity.Luna_314_cnx.value,
                    external_validation=Connectivity.Luna_314_ev.value
                )
                FixEnvironment.environment_instances.update(
                    {EnvironmentType.quod314_luna_standard.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod314_luna_standard.value]
        elif env.value == EnvironmentType.quod309_kratos_standard.value:
            if EnvironmentType.quod309_kratos_standard.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod309_kratos_standard.value,
                    sell_side_esp=Connectivity.Kratos_309_ss_esp.value,
                    sell_side_rfq=Connectivity.Kratos_309_ss_rfq.value,
                    buy_side_esp=Connectivity.Kratos_309_ss_esp_t.value,
                    feed_handler=Connectivity.Kratos_309_Feed_Handler.value,
                    feed_handler2=Connectivity.Kratos_309_Feed_Handler_Q.value,
                    drop_copy=Connectivity.Kratos_309_dc.value,
                    buy_side_md=Connectivity.Kratos_309_bs_md.value,
                    sell_side_cnx=Connectivity.Kratos_309_cnx.value,
                    external_validation=Connectivity.Kratos_309_ev.value
                )
                FixEnvironment.environment_instances.update(
                    {EnvironmentType.quod309_kratos_standard.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod309_kratos_standard.value]
        elif env.value == EnvironmentType.quod317_ganymede_standard_test.value:
            if EnvironmentType.quod317_ganymede_standard_test.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod317_ganymede_standard_test.value,
                    sell_side=Connectivity.Ganymede_317_ss.value,
                    buy_side=Connectivity.Ganymede_317_bs.value,
                    drop_copy=Connectivity.Ganymede_317_dc.value
                )
                FixEnvironment.environment_instances.update(
                    {EnvironmentType.quod317_ganymede_standard_test.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod317_ganymede_standard_test.value]
        elif env.value == EnvironmentType.quod310_columbia_standard.value:
            if EnvironmentType.quod310_columbia_standard.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod310_columbia_standard.value,
                    sell_side=Connectivity.Columbia_310_Sell_Side.value,
                    buy_side=Connectivity.Columbia_310_Buy_Side.value,
                    feed_handler=Connectivity.Columbia_310_Feed_Handler.value
                )
                FixEnvironment.environment_instances.update(
                    {EnvironmentType.quod310_columbia_standard.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod310_columbia_standard.value]
        elif env.value == EnvironmentType.quod319_kuiper_kepler.value:
            if EnvironmentType.quod319_kuiper_kepler.value not in FixEnvironment.environment_instances.keys():
                site_environment = FixEnvironment(
                    environment_type=EnvironmentType.quod319_kuiper_kepler.value,
                    sell_side=Connectivity.Kepler_319_Sell_Side.value,
                    buy_side=Connectivity.Kepler_319_Buy_Side.value,
                    feed_handler=Connectivity.Kuiper_319_Feed_Handler.value
                )
                FixEnvironment.environment_instances.update(
                    {EnvironmentType.quod319_kuiper_kepler.value: site_environment})
            return FixEnvironment.environment_instances[EnvironmentType.quod319_kuiper_kepler.value]
        else:
            raise Exception('No such environment')

    def __str__(self):
        result = f"Environment {self.environment_type} "
        for attr, value in self.__dict__.items():
            if value:
                result += f"{attr} - {value}; "
        return result
