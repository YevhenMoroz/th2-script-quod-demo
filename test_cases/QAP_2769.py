import logging
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
# from grpc_modules.infra_pb2 import ConnectionID
from grpc_modules.quod_simulator_pb2 import RequestMDRefID
from stubs import Stubs
from th2_grpc_act_template.act_template_pb2 import PlaceMessageRequest
from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs
from win_gui_modules.utils import set_session_id, get_base_request
from win_gui_modules.utils import prepare_fe, close_fe, call
from grpc_modules.win_act_pb2_grpc import HandWinActStub
from grpc_modules.order_book_pb2_grpc import OrderBookServiceStub
from channels import Channels
from win_gui_modules.wrappers import *
from win_gui_modules.order_book_wrappers import ExtractionInfo, OrdersDetails, ExtractionDetail
from th2_grpc_common.common_pb2 import ConnectionID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    # simulator = Stubs.simulator
    # sim = Stubs.sim

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2769"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-paris',
        'TraderConnectivity3': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '2',
        'OrderQty': 1000,
        'OrdType': '2',
        'Price': 25,
        'TimeInForce': '0',
        'TargetStrategy': 1011,
        'Instrument': {
            # 'Symbol': 'FR0000125460_EUR',
            'Symbol': 'FR0010542647_EUR',
            # 'SecurityID': 'FR0000125460',
            'SecurityID': 'FR0010542647',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
    }
    reusable_order_params = {  # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': case_params['TargetStrategy']
    }
    # symbol_1 = "596"
    # symbol_2 = "3390"
    # symbol_1 = "1062"
    # symbol_2 = "3503"
    # trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
    #     connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
    #     no_party_ids=[
    #         TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
    #         TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
    #         TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
    #     ],
    #     cum_qty=int(case_params['OrderQty'] / 2),
    #     mask_as_connectivity="fix-fh-eq-paris",
    #     md_entry_size={500: 0},
    #     md_entry_px={30: 25},
    #     symbol=symbol_1
    # ))
    # trade_rule_2 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
    #     connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
    #     no_party_ids=[
    #         TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
    #         TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
    #         TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
    #     ],
    #     cum_qty=int(case_params['OrderQty'] / 2),
    #     mask_as_connectivity="fix-fh-eq-trqx",
    #     md_entry_size={500: 0},
    #     md_entry_px={30: 25},
    #     symbol=symbol_2
    # ))
    try:
    #     # Send MarketDataSnapshotFullRefresh messages
    #
    #     MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
    #         symbol=symbol_1,
    #         connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
    #     )).MDRefID
    #     MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
    #         symbol=symbol_2,
    #         connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
    #     )).MDRefID
    #     mdfr_params_1 = {
    #         'MDReportID': "1",
    #         'MDReqID': MDRefID_1,
    #         'Instrument': {
    #             'Symbol': symbol_1
    #         },
    #         'NoMDEntries': [
    #             {
    #                 'MDEntryType': '0',
    #                 'MDEntryPx': '25',
    #                 'MDEntrySize': '500',
    #                 'MDEntryPositionNo': '1'
    #             },
    #             {
    #                 'MDEntryType': '1',
    #                 'MDEntryPx': '30',
    #                 'MDEntrySize': '500',
    #                 'MDEntryPositionNo': '1'
    #             }
    #         ]
    #     }
    #     mdfr_params_2 = deepcopy(mdfr_params_1)
    #     mdfr_params_2['MDReqID'] = MDRefID_2
    #     mdfr_params_2['Instrument'] = {
    #             'Symbol': symbol_2
    #     }
    #     act.sendMessage(request=bca.convert_to_request(
    #         'Send MarketDataSnapshotFullRefresh', "fix-fh-eq-paris", case_id,
    #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1)
    #     ))
    #     act.sendMessage(request=bca.convert_to_request(
    #         'Send MarketDataSnapshotFullRefresh', "fix-fh-eq-trqx", case_id,
    #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_2)
    #     ))

        # Send sorping order

        sor_order_params = {
            'Account': case_params['Account'],
            'HandlInst': case_params['HandlInst'],
            'Side': case_params['Side'],
            'OrderQty': case_params['OrderQty'],
            'TimeInForce': case_params['TimeInForce'],
            'Price': case_params['Price'],
            'OrdType': case_params['OrdType'],
            'ClOrdID': bca.client_orderid(9),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': case_params['Instrument'],
            'OrderCapacity': 'A',
            # 'OrdSubStatus': 'SORPING',
            'Currency': 'EUR',
            'ComplianceID': 'FX5',
            'ClientAlgoPolicyID': 'QA_SORPING',
            'TargetStrategy': case_params['TargetStrategy'],
            'Text': 'QAP-2769'
        }
        new_sor_order = act.placeOrderFIX(
            PlaceMessageRequest(
                description="Send new sorping order",
                connection_id=ConnectionID(session_alias="gtwquod3"),
                parent_event_id=case_id,
                message=bca.message_to_grpc('NewOrderSingle', sor_order_params, "gtwquod3")
            )
        )
    #     new_sor_order = act.placeOrderFIX(
    #         bca.convert_to_request(
    #             'Send NewSingleOrder',
    #             case_params['TraderConnectivity'],
    #             case_id,
    #             bca.message_to_grpc('NewOrderSingle', sor_order_params)
    #         ))
        checkpoint_1 = new_sor_order.checkpoint_id
        pending_er_params = {
            **reusable_order_params,
            'ClOrdID': sor_order_params['ClOrdID'],
            'OrderID': '*',
            # 'OrderID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            # 'TradingParty': sor_order_params['TradingParty'],
            'NoParty': [{
                'PartyID': 'gtwquod3',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'LeavesQty': sor_order_params['OrderQty'],
            'Instrument': case_params['Instrument']
        }
        verifier.submitCheckRule(
            request=bca.create_check_rule(
                "ER Pending NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            ),
            timeout=3000
        )
    #     verifier.submitCheckRule(
    #         bca.create_check_rule(
    #             "ER Pending NewOrderSingle Received",
    #             bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
    #             checkpoint_1, case_params['TraderConnectivity'], case_id
    #         )
    #     )
    #
    #     new_er_params = deepcopy(pending_er_params)
    #     new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    #     new_er_params['Instrument'] = {
    #         'Symbol': case_params['Instrument']['Symbol'],
    #         'SecurityExchange': case_params['Instrument']['SecurityExchange']
    #     }
    #     verifier.submitCheckRule(
    #         bca.create_check_rule(
    #             "ER New NewOrderSingle Received",
    #             bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
    #             checkpoint_1, case_params['TraderConnectivity'], case_id
    #         )
    #     )
    except Exception as e:
        logging.error("Error execution", exc_info=True)
    # sim.removeRule(trade_rule_1)
    # sim.removeRule(trade_rule_2)

    # if BaseParams.session_id is None:
    #     BaseParams.session_id = set_session_id()
    # session_id = BaseParams.session_id
    # BaseParams.event_id = case_id
    # prepare_fe(case_id, session_id)

    # Do some actions in the frontend
    # common_act = HandWinActStub(Channels.ui_act_channel)
    # act2 = OrderBookServiceStub(Channels.ui_act_channel)

    # order_info_extraction = "getOrderInfo"
    #
    # data = call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.id", "Order ID"]))
    # order_id = data['order.id']
    # logger.info(order_id)

    # check child orders

    extraction_id = "get order id"

    # sub_lv2_1_qty = ExtractionDetail("subOrder_1_lv2.qty", "Qty")
    #
    # sub_lv2_details = OrdersDetails()
    # sub_lv2_details.add_single_extraction_info(ExtractionInfo.create(detail=sub_lv2_1_qty))
    # length_name = "subOrders_lv2.length"
    # sub_lv2_details.extract_length(length_name)
    #
    # sub_lv1_info = ExtractionInfo()
    # sub_lv1_qty = ExtractionDetail("subOrder_lv1.qty", "Qty")
    # sub_lv1_info.add_order_details(sub_lv1_qty)
    # sub_lv1_info.set_sub_orders_details(sub_lv2_details)
    #
    # main_order_info = ExtractionInfo.create(sub_order_details=OrdersDetails.create(info=sub_lv1_info))
    # main_order_info = ExtractionInfo()
    # main_order_info.add_order_details(ExtractionDetail("order.id", "Order ID"))
    #
    # main_order_details = OrdersDetails()
    # main_order_details.set_default_params(get_base_request(session_id, case_id))
    # main_order_details.set_extraction_id(extraction_id)
    # main_order_details.set_filter(["Lookup", "FR0010542647_EUR"])
    # main_order_details.add_single_extraction_info(main_order_info)
    #
    # result = call(act2.getOrdersDetails, main_order_details.request())
    # logger.info(result)

    # close_fe(case_id, session_id)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
