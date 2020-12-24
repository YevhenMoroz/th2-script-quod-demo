import logging
from copy import deepcopy
from datetime import datetime
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.infra_pb2 import ConnectionID
from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs, RequestMDRefID
from grpc_modules.win_act_pb2_grpc import HandWinActStub
from grpc_modules.order_book_pb2_grpc import OrderBookServiceStub
from custom.basic_custom_actions import create_event_id
from custom.basic_custom_actions import create_store_event_request
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.utils import call, get_base_request, prepare_fe, set_session_id, close_fe
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionInfo
from channels import Channels
from win_gui_modules.wrappers import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False


def execute(report_id, session_id):
    global sor_order_params, pending_er_params, new_er_params
    event_store = EventStoreServiceStub(Channels.event_store_channel)
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    sim = Stubs.sim

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2740 [SORPING] Send SORPING algo order to check PriceCost criteria in Aggressive phase"
    case_id = bca.create_event(case_name, report_id)
    # case_id = create_event_id()
    event_store.StoreEvent(request=create_store_event_request(case_name, case_id, report_id))
    set_base(session_id, case_id)

    common_act = HandWinActStub(Channels.ui_act_channel)
    #
    act2 = OrderBookServiceStub(Channels.ui_act_channel)
    #
    order_info_extraction = "getOrderInfo"

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
        'OrderQty': 100,
        'OrdType': '2',
        'Price': 25,
        'TimeInForce': '0',
        'TargetStrategy': 1011,
        'Instrument': {
            'Symbol': 'FR0000125460_EUR',
            'SecurityID': 'FR0000125460',
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
    symbol_1 = "596"
    symbol_2 = "3390"
    trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=int(case_params['OrderQty'] / 2),
        mask_as_connectivity="fix-fh-eq-paris",
        md_entry_size={50: 0},
        md_entry_px={30: 25},
        symbol=symbol_1
    ))
    trade_rule_2 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=int(case_params['OrderQty'] / 2),
        mask_as_connectivity="fix-fh-eq-trqx",
        md_entry_size={50: 0},
        md_entry_px={30: 25},
        symbol=symbol_2
    ))
    try:
        # Send MarketDataSnapshotFullRefresh message

        MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_1,
            connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
        )).MDRefID
        MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_2,
            connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
        )).MDRefID
        mdfr_params_1 = {
            'MDReportID': "1",
            'MDReqID': MDRefID_1,
            'Instrument': {
                'Symbol': symbol_1
            },
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '30',
                    'MDEntrySize': '50',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '40',
                    'MDEntrySize': '50',
                    'MDEntryPositionNo': '1'
                }
            ]
        }
        mdfr_params_2 = deepcopy(mdfr_params_1)
        mdfr_params_2['MDReqID'] = MDRefID_2
        mdfr_params_2['Instrument'] = {
            'Symbol': symbol_2
        }
        act.sendMessage(request=bca.convert_to_request(
            'Send MarketDataSnapshotFullRefresh', "fix-fh-eq-paris", case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1)
        ))
        act.sendMessage(request=bca.convert_to_request(
            'Send MarketDataSnapshotFullRefresh', "fix-fh-eq-trqx", case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_2)
        ))

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
            'Text': 'QAP-2740'
        }
        # print(bca.message_to_grpc('NewOrderSingle', sor_order_params))
        new_sor_order = act.placeOrderFIX(
            bca.convert_to_request(
                'Send NewSingleOrder',
                case_params['TraderConnectivity'],
                case_id,
                bca.message_to_grpc('NewOrderSingle', sor_order_params)
            ))
        checkpoint_1 = new_sor_order.checkpoint_id
        pending_er_params = {
            **reusable_order_params,
            'ClOrdID': sor_order_params['ClOrdID'],
            'OrderID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
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
            bca.create_check_rule(
                "ER Pending NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )

        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['Instrument'] = {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER New NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )
        sim.removeRule(trade_rule_1)
        sim.removeRule(trade_rule_2)
    except Exception as e:
        logging.error("Error execution", exc_info=True)

    if BaseParams.session_id is None:
        BaseParams.session_id = set_session_id()
    session_id = BaseParams.session_id
    prepare_fe(case_id, session_id)

    call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.ExecPcy", "ExecPcy"]))
    call(common_act.verifyEntities, verification(
        order_info_extraction, "checking order", [
            verify_ent("Order ExecPcy", "order.ExecPcy", "Synth (Quod LitDark)")
        ])
         )

    # prepare_fe(report_id, session_id)
    # step 2

    call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.status", "Sts"]))
    call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                 [verify_ent("Order Status", "order.status", "Filled")]))

    sub_order1 = ExtractionInfo.from_data(["subOrder1.ExecPcy", "ExecPcy"])
    sub_order2 = ExtractionInfo.from_data(["subOrder2.ExecPcy", "ExecPcy"])
    main_order = ExtractionInfo.from_sub_order_details(OrdersDetails.from_info([sub_order1, sub_order2]))

    sub_order_details = OrdersDetails()
    sub_order_details.set_default_params(get_base_request(session_id, case_id))
    sub_order_details.set_extraction_id("order.subOrder")
    sub_order_details.set_one_extraction_info(main_order)

    call(act2.getOrdersDetails, sub_order_details.request())

    call(common_act.verifyEntities,
         verification("order.subOrder", "checking order",
                      [verify_ent("Order ExecPcy", "subOrder1.ExecPcy", "Synth (Quod MultiListing)")]))

    call(common_act.verifyEntities,
         verification("order.subOrder", "checking order",
                      [verify_ent("Order ExecPcy", "subOrder2.ExecPcy", "Synth (Quod DarkPool)")]))

    close_fe(case_id, session_id)

    cancel_order_params = {
        'OrigClOrdID': sor_order_params['ClOrdID'],
        'ClOrdID': (sor_order_params['ClOrdID']),
        'Instrument': sor_order_params['Instrument'],
        'ExDestination': 'QDL1',
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty'],
        'Text': 'Cancel order'
    }

    cancel_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params),
        ))

    cancellation_er_params = {
        **reusable_order_params,
        'Instrument': {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        },
        'ClOrdID': cancel_order_params['ClOrdID'],
        'OrderID': pending_er_params['OrderID'],
        'OrderQty': case_params['OrderQty'],
        'Price': case_params['Price'],
        'TransactTime': '*',
        'ExecID': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'ExecRestatementReason': '4',
        'NoParty': '*',
        'NoStrategyParameters': new_er_params['NoStrategyParameters'],
        'TargetStrategy': case_params['TargetStrategy'],
        'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID']
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Cancellation ER Received',
            bca.filter_to_grpc('ExecutionReport', cancellation_er_params, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
