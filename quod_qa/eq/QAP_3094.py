import logging
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodSingleExecRule, TemplateNoPartyIDs
from th2_grpc_common.common_pb2 import ConnectionID, Direction
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-3094"
    case_params = {
        'TraderConnectivity': 'gtwquod5',
        'TraderConnectivity2': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'Account2': 'TRQX_KEPLER',
        'HandlInst': '2',
        'Side': '1',
        'OrderQty': 1100,
        'OrdType': '2',
        'Price': 45,
        'TimeInForce': '0',
        'Instrument': {
            'Symbol': 'IT0000076189_EUR',
            'SecurityID': 'IT0000076189',
            'SecurityIDSource': '4',
            'SecurityExchange': 'MTAA'
        }
    }

    TraderConnectivity = "gtwquod5"
    TraderConnectivity2 = 'fix-bs-eq-trqx'

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)


    symbol = "2320"




    try:

        MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
        )).MDRefID

        mdfr_params = {
            'MDReportID': "1",
            'MDReqID': MDRefID_2,
            'Instrument': {
                'Symbol': symbol
            },
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '10',
                    'MDEntrySize': '650',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '11',
                    'MDEntrySize': '500',
                    'MDEntryPositionNo': '1'
                }
        ]}

        mdfr_params_2 = {
            'MDReportID': "1",
            'MDReqID': MDRefID_2,
            'Instrument': {
                'Symbol': symbol
            },
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '10.7',
                    'MDEntrySize': '650',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '11',
                    'MDEntrySize': '500',
                    'MDEntryPositionNo': '1'
                }
        ]}

        # send MD
        act.sendMessage(
            request=bca.convert_to_request(
                'Send MarketDataSnapshotFullRefresh',
                "fix-fh-eq-trqx",
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params, "fix-fh-eq-trqx")
            ))

        sor_order_params = {
            'Account': "CLIENT1",
            'HandlInst': "2",
            'Side': "1",
            'OrderQty': "200",
            'TimeInForce': "0",
            'Price': "10.6",
            'OrdType': "2",
            'ClOrdID': bca.client_orderid(9),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'IT0000076189_EUR',
                'SecurityID': 'IT0000076189',
                'SecurityIDSource': '4',
                'SecurityExchange': 'MTAA'
            },
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': "1009",
            "PegOffsetType": "2",
            "PegOffsetValue": "0",
            "PegPriceType": "5"
        }

        #Send new order
        new_peg_order = act.placeOrderFIX(
            bca.convert_to_request(
                'Send Peg order via Fix',
                TraderConnectivity,
                case_id,
                bca.message_to_grpc('NewOrderSingle', sor_order_params, TraderConnectivity)
            ))
        checkpoint_1 = new_peg_order.checkpoint_id


        # send MD
        act.sendMessage(
            request=bca.convert_to_request(
                'Send MDSFR with BBID 10 ',
                "fix-fh-eq-trqx",
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params, "fix-fh-eq-trqx")
            ))




        execution_report1_params = {
            'ClOrdID': sor_order_params['ClOrdID'],
            'OrderID': new_peg_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'LeavesQty': sor_order_params['OrderQty'],
            'Instrument': sor_order_params['Instrument']
        }

        verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report Pending",
                bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1,
                TraderConnectivity,
                case_id
            )
        )

        execution_report2_params = deepcopy(execution_report1_params)
        execution_report2_params['OrdStatus'] = execution_report2_params['ExecType'] = '0'


        verifier.submitCheckRule(
            bca.create_check_rule(
                "Receive Execution Report New",
                bca.filter_to_grpc("ExecutionReport", execution_report2_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1,
                TraderConnectivity,
                case_id
            )
        )

        dma_order_params = {
            'HandlInst': '1',
            'Side': sor_order_params['Side'],
            'OrderQty': sor_order_params['OrderQty'],
            'TimeInForce': '0',
            'Price': '10',
            'OrdType': sor_order_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'ClOrdID': '*',
            'ChildOrderID': '*',
            'TransactTime': '*',
            'Instrument': {
                'SecurityID': sor_order_params['Instrument']['SecurityID'],
                'SecurityIDSource': sor_order_params['Instrument']['SecurityIDSource']
            }
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                'Transmitted NewOrderSingle  with price 10',
                bca.filter_to_grpc('NewOrderSingle', dma_order_params),
                checkpoint_1,
                TraderConnectivity2,
                case_id
            )
        )


        # send MD#2
        act.sendMessage(
            request=bca.convert_to_request(
                'Send MDSFR with BBID 10.7',
                "fix-fh-eq-trqx",
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_2, "fix-fh-eq-trqx")
            ))
        dma_order_params2 = deepcopy(dma_order_params)
        dma_order_params2['Price'] = '10.6'


        verifier.submitCheckRule(
            bca.create_check_rule(
                'Transmitted Amend with price 10.6',
                bca.filter_to_grpc('OrderCancelReplaceRequest', dma_order_params2),
                checkpoint_1,
                TraderConnectivity2,
                case_id
            )
        )
        amend_executionReport = { 'HandlInst': '1',
            'Side': sor_order_params['Side'],
            'OrderQty': sor_order_params['OrderQty'],
            'TimeInForce': '0',
            'Price': '10.6',
            'OrdType': sor_order_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'ClOrdID': '*',
            'ChildOrderID': '*',
            'TransactTime': '*',
            'Instrument': {
                'SecurityID': sor_order_params['Instrument']['SecurityID'],
                'SecurityIDSource': sor_order_params['Instrument']['SecurityIDSource']
            }
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                'Send ER with price 10.6',
                bca.filter_to_grpc('ExecutionReport', amend_executionReport),
                checkpoint_1,
                TraderConnectivity2,
                case_id,
                Direction.Value("SECOND")
            )
        )
    except Exception:
        logger.error("Error execution", exc_info=True)


    logger.info(f"Case {case_name} was executed in {round(datetime.now().timestamp() - seconds)} sec.")