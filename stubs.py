from th2_common.schema.factory.common_factory import CommonFactory
from th2_grpc_act_gui_quod.act_ui_win_service import ActUIWinService
from th2_grpc_act_gui_quod.order_book_service import OrderBookServiceService
from th2_grpc_act_gui_quod.order_ticket_service import OrderTicketServiceService
from th2_grpc_act_quod.act_fix_service import ActFixService
from th2_grpc_check1.check1_service import Check1Service
from th2_grpc_sim_quod.sim_service import TemplateSimulatorServiceService
from th2_grpc_sim.sim_service import SimService
from th2_grpc_act_gui_quod.rfq_operations_service import RFQOperationsService


class Stubs:
    factory = CommonFactory(
        grpc_router_config_filepath="./configs/grpc.json",
        rabbit_mq_config_filepath="./configs/rabbit.json",
        mq_router_config_filepath="./configs/mq.json",
        custom_config_filepath="./configs/script-params.json"
    )
    fix_act = factory.grpc_router.get_service(ActFixService)
    event_store = factory.event_batch_router
    verifier = factory.grpc_router.get_service(Check1Service)
    simulator = factory.grpc_router.get_service(TemplateSimulatorServiceService)
    core = factory.grpc_router.get_service(SimService)
    win_act = factory.grpc_router.get_service(ActUIWinService)
    win_act_order_book = factory.grpc_router.get_service(OrderBookServiceService)
    win_act_order_ticket = factory.grpc_router.get_service(OrderTicketServiceService)
    win_act_rfq_service = factory.grpc_router.get_service(RFQOperationsService)

    custom_config = factory.create_custom_configuration()
    session_id = None
    frontend_is_open = False
