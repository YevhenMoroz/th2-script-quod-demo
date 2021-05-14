from os.path import abspath, dirname, join
from th2_common.schema.factory.common_factory import CommonFactory
from th2_grpc_act_gui_quod.act_ui_win_service import ActUIWinService
from th2_grpc_act_gui_quod.ar_operations_service import AggregatedRatesOperationsService
from th2_grpc_act_gui_quod.middle_office_service import MiddleOfficeOperationsService
from th2_grpc_act_gui_quod.order_book_service import OrderBookServiceService
from th2_grpc_act_gui_quod.order_ticket_service import OrderTicketServiceService
from th2_grpc_act_quod.act_fix_service import ActFixService
from th2_grpc_check1.check1_service import Check1Service
from th2_grpc_sim.sim_service import SimService
from th2_grpc_sim_quod.sim_service import TemplateSimulatorServiceService
from th2_grpc_act_gui_quod.cp_operations_service import ClientPricingOperationsService
from th2_grpc_sim_http.sim_template_service import SimTemplateService


class Stubs:
    configs_dir = join(dirname(abspath(__file__)), 'configs')
    factory = CommonFactory(
        grpc_router_config_filepath=join(configs_dir, "grpc.json"),
        rabbit_mq_config_filepath=join(configs_dir, "rabbit.json"),
        mq_router_config_filepath=join(configs_dir, "mq.json"),
        custom_config_filepath=join(configs_dir, "script-params.json")
    )
    fix_act = factory.grpc_router.get_service(ActFixService)
    event_store = factory.event_batch_router
    verifier = factory.grpc_router.get_service(Check1Service)
    simulator = factory.grpc_router.get_service(TemplateSimulatorServiceService)
    # simulator_http = factory.grpc_router.get_service(SimTemplateService)
    core = factory.grpc_router.get_service(SimService)
    win_act = factory.grpc_router.get_service(ActUIWinService)
    win_act_order_book = factory.grpc_router.get_service(OrderBookServiceService)
    win_act_order_ticket = factory.grpc_router.get_service(OrderTicketServiceService)
    win_act_aggregated_rates_service = factory.grpc_router.get_service(AggregatedRatesOperationsService)
    win_act_middle_office_service = factory.grpc_router.get_service(MiddleOfficeOperationsService)
    win_act_cp_service = factory.grpc_router.get_service(ClientPricingOperationsService)

    custom_config = factory.create_custom_configuration()
    session_id = None
    frontend_is_open = False
