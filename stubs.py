import os
from os.path import abspath, dirname, join
import grpc
from th2_common.schema.factory.common_factory import CommonFactory
from th2_grpc_act_gui_quod.act_ui_win_service import ActUIWinService
from th2_grpc_act_gui_quod.ar_operations_service import AggregatedRatesOperationsService
from th2_grpc_act_gui_quod.bag_mgt_service import BagManagementServiceService
from th2_grpc_act_gui_quod.basket_book_service import BasketBookServiceService
from th2_grpc_act_gui_quod.basket_ticket_service import BasketTicketServiceService
from th2_grpc_act_gui_quod.bookings_blotter_service import BookingsBlotterServiceService
from th2_grpc_act_gui_quod.care_orders_service import CareOrdersServiceService
from th2_grpc_act_gui_quod.child_order_book_service import ChildOrderBookServiceService
from th2_grpc_act_gui_quod.dealer_intervention_operations_service import DealerInterventionOperationsService
from th2_grpc_act_gui_quod.layout_panel_service import LayoutPanelServiceService
from th2_grpc_act_gui_quod.fx_dealing_positions_service import FxDealingPositionsServiceService
from th2_grpc_act_gui_quod.middle_office_service import MiddleOfficeOperationsService
from th2_grpc_act_gui_quod.order_book_archive_service import OrderBookArchiveServiceService
from th2_grpc_act_gui_quod.order_book_fx_service import OrderBookFXServiceService
from th2_grpc_act_gui_quod.order_book_service import OrderBookServiceService
from th2_grpc_act_gui_quod.order_ticket_fx_service import OrderTicketFxServiceService
from th2_grpc_act_gui_quod.order_ticket_service import OrderTicketServiceService
from th2_grpc_act_gui_quod.risk_management_service import RiskManagementServiceService
from th2_grpc_act_gui_quod.trade_book_archive_service import TradeBookArchiveServiceService
from th2_grpc_act_gui_quod.trades_service import TradesServiceService
from th2_grpc_act_fix_quod.act_fix_service import ActFixService
from th2_grpc_check1.check1_service import Check1Service
from th2_grpc_sim import sim_pb2_grpc
from th2_grpc_sim.sim_service import SimService
from th2_grpc_act_gui_quod.cp_operations_service import ClientPricingOperationsService
from th2_grpc_sim_http_quod.sim_template_service import SimTemplateService
from th2_grpc_act_rest_quod.rest_act_service import RestActService
from th2_grpc_act_java_api_quod.act_service import ActService

from th2_grpc_sim_fix_quod.template_simulator_service_service import TemplateSimulatorServiceService
from th2_grpc_sim_fix_quod.template_simulator_service_test_service import TemplateSimulatorServiceTestService
from th2_grpc_sim_fix_quod.template_simulator_service_equity_service import TemplateSimulatorServiceEquityService

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Stubs:
    configs_dir = join(dirname(abspath(__file__)), 'configs')
    factory = CommonFactory(
        grpc_config_filepath=join(configs_dir, "grpc.json"),
        rabbit_mq_config_filepath=join(configs_dir, "rabbit.json"),
        mq_router_config_filepath=join(configs_dir, "mq.json"),
        custom_config_filepath=join(configs_dir, "script-params.json"),
        prometheus_config_filepath=join(configs_dir, "prometheus.json"),
        logging_config_filepath="logging.txt"
    )
    fix_act = factory.grpc_router.get_service(ActFixService)
    event_store = factory.event_batch_router
    verifier = factory.grpc_router.get_service(Check1Service)
    simulator = factory.grpc_router.get_service(TemplateSimulatorServiceService)
    simulator_equity = factory.grpc_router.get_service(TemplateSimulatorServiceEquityService)
    test_sim = factory.grpc_router.get_service(TemplateSimulatorServiceTestService)
    simulator_http = factory.grpc_router.get_service(SimTemplateService)
    core = factory.grpc_router.get_service(SimService)
    core_equity = sim_pb2_grpc.SimStub(grpc.insecure_channel("10.0.22.22:32700"))
    core_algo = sim_pb2_grpc.SimStub(grpc.insecure_channel("10.0.22.22:32650"))
    win_act = factory.grpc_router.get_service(ActUIWinService)
    win_act_order_book = factory.grpc_router.get_service(OrderBookServiceService)
    win_act_order_book_fx = factory.grpc_router.get_service(OrderBookFXServiceService)
    win_act_trades = factory.grpc_router.get_service(TradesServiceService)
    win_act_order_ticket = factory.grpc_router.get_service(OrderTicketServiceService)
    win_act_order_ticket_fx = factory.grpc_router.get_service(OrderTicketFxServiceService)
    win_act_aggregated_rates_service = factory.grpc_router.get_service(AggregatedRatesOperationsService)
    win_act_middle_office_service = factory.grpc_router.get_service(MiddleOfficeOperationsService)
    win_act_cp_service = factory.grpc_router.get_service(ClientPricingOperationsService)
    win_act_options = factory.grpc_router.get_service(LayoutPanelServiceService)
    act_fx_dealing_positions = factory.grpc_router.get_service(FxDealingPositionsServiceService)
    win_act_dealer_intervention_service = factory.grpc_router.get_service(DealerInterventionOperationsService)
    api_service = factory.grpc_router.get_service(RestActService)
    care_orders_action = factory.grpc_router.get_service(CareOrdersServiceService)
    win_act_basket_order_book = factory.grpc_router.get_service(BasketBookServiceService)
    win_act_basket_ticket = factory.grpc_router.get_service(BasketTicketServiceService)
    win_act_bag_management_service = factory.grpc_router.get_service(BagManagementServiceService)
    win_act_booking_blotter_service = factory.grpc_router.get_service(BookingsBlotterServiceService)
    win_act_risk_management = factory.grpc_router.get_service(RiskManagementServiceService)
    win_act_child_order_book = factory.grpc_router.get_service(ChildOrderBookServiceService)
    win_act_order_book_archive = factory.grpc_router.get_service(OrderBookArchiveServiceService)
    win_act_trade_book_archive = factory.grpc_router.get_service(TradeBookArchiveServiceService)
    # TODO: rename java api act service name
    act_java_api = factory.grpc_router.get_service(ActService)

    custom_config = factory.create_custom_configuration()
    session_id = None
    frontend_is_open = True
