import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Direction
from custom import tenor_settlement_date as tsd

from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    rule_man = RuleManager()

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2684"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    NOS1 = rule_man.add_NOS('fix-bs-eq-paris')
    OCR1 = rule_man.add_OCR('fix-bs-eq-paris')
    logger.info(f"Start rules with id's: \n {NOS1}, {OCR1}")

    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-paris',
        'TraderConnectivity3': 'fix-bs-eq-trqx',
        'TraderConnectivity4': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'Account2': 'TRQX_KEPLER',
        'HandlInst': '2',
        'Side': '1',
        'OrderQty': 1000,
        'OrdType': '2',
        'Price': 20,
        'TimeInForce': '0',
        'TargetStrategy': 1011,
        'Instrument': {
            'Symbol': 'FR0010542647_EUR',
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
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
        'TargetStrategy': case_params['TargetStrategy'],
        'NoParty': [{
            'PartyID': 'TestCLIENTACCOUNT',
            'PartyIDSource': 'D',
            'PartyRole': '24'
        }],
        'Text': case_name
    }

    try:
        # print(bca.message_to_grpc('NewOrderSingle', sor_order_params))
        new_sor_order = act.placeOrderFIX(
            bca.convert_to_request(
                'Send NewSingleOrder',
                case_params['TraderConnectivity'],
                case_id,
                bca.message_to_grpc('NewOrderSingle', sor_order_params, case_params['TraderConnectivity'])
            ))

        checkpoint_1 = new_sor_order.checkpoint_id

        pending_er_params = {
            **reusable_order_params,
            'ClOrdID': sor_order_params['ClOrdID'],
            'ExecID': '*',
            'OrderID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
            'OrderQty': case_params['OrderQty'],
            'Price': case_params['Price'],
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': 'A',
            'ExecType': 'A',
            'NoParty': [{
                'PartyID': 'TestCLIENTACCOUNT',
                'PartyIDSource': 'D',
                'PartyRole': '24'
            },
            {
                'PartyID': 'gtwquod3',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }
            ],
            'LeavesQty': sor_order_params['OrderQty'],
            'Instrument': case_params['Instrument']
        }
        # print(bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus']))
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER Pending NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )
        del pending_er_params['Account']
        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['ExecID'] = '*'
        new_er_params['ExecRestatementReason'] = '4'
        new_er_params['SecondaryAlgoPolicyID'] = 'QA_SORPING'
        new_er_params['Instrument'] = case_params['Instrument']
        new_er_params['SettlDate'] = "*"
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER New NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )
        time.sleep(60)
        readlog_nos_params = {
            "AuthenticationBlock": {
                "UserID": case_params['TraderConnectivity'],
                "RoleID": "FIXClient",
                "SessionKey": "*"
            },
            "NewOrderSingleBlock": {
                "InstrumentBlock": {
                    "InstrSymbol": case_params['Instrument']['Symbol'],
                    "SecurityID": case_params['Instrument']['SecurityID'],
                    "SecurityIDSource": "ISIN",
                    "SecurityExchange": "XPAR"
                },
                "PartiesList": {
                    "PartiesBlock": [
                        {
                            "PartyID": sor_order_params['NoParty'][0]['PartyID'],
                            "PartyIDSource": "Proprietary",
                            "PartyRole": "CustomerAccount"
                        }
                    ]
                },
                "DisplayInstructionBlock": "*",
                "AlgoParametersBlock": {
                    "AlgoType": "LitDark"
                },
                "OrdrMiscBlock": {
                    "OrdrMisc0": sor_order_params['NoParty'][0]['PartyID']
                },
                "ClOrdID": sor_order_params['ClOrdID'],
                "Side": "Buy",
                "Price": '{:.9f}'.format(int(case_params['Price'])),
                "OrdType": "Limit",
                "Currency": sor_order_params['Currency'],
                "TimeInForce": "Day",
                "OrdCapacity": "Agency",
                "TransactTime": datetime.fromisoformat(sor_order_params['TransactTime']).strftime("%Y-%b-%d %H:%M:%S"),
                "ComplianceID": sor_order_params['ComplianceID'],
                "ClientAccountGroupID": "KEPLER",
                "ClientAlgoPolicyID": sor_order_params['ClientAlgoPolicyID'],
                "OrdQty": '{:.9f}'.format(int(case_params['OrderQty'])),
                "ExecutionPolicy": "Synthetic",
            },
            "CDOrdAssignInstructionsBlock": {
                "CDOrdFreeNotes": sor_order_params['Text']
            }
        }

        # print(bca.filter_to_grpc("NewOrderSingle", readlog_nos_params))
        verifier.submitCheckRule(
            bca.create_check_rule(
                "Readlog NewOrderSingle Received",
                bca.filter_to_grpc("NewOrderSingle", readlog_nos_params, keys=['ClOrdID', 'CDOrdFreeNotes'],
                                   ignored_fields=['Header']),
                checkpoint_1, 'QUOD.FIXSELLQUODKepler.log', case_id
            )
        )

        instrument_2 = {
            'Symbol': 'RSC',
            'SecurityID': 'FR0010542647',
            'SecurityType': 'CS',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

        newordersingle_params = {
            'Account': case_params['Account'],
            'HandlInst': '1',
            'Side': case_params['Side'],
            'OrderQty': sor_order_params['OrderQty'],
            'TimeInForce': case_params['TimeInForce'],
            'Price': case_params['Price'],
            'OrdType': case_params['OrdType'],
            'OrderCapacity': 'A',
            'SettlDate': "*",
            'Currency': 'EUR',
            'ClOrdID': '*',
            'ChildOrderID': '*',
            'TransactTime': '*',
            'Instrument': instrument_2,
            'NoParty': sor_order_params['NoParty'],
            'AlgoCst03': sor_order_params['NoParty'][0]['PartyID'],
            'ExDestination': 'XPAR'
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                'NewOrderSingle transmitted >> PARIS',
                bca.filter_to_grpc('NewOrderSingle', newordersingle_params, ["ClOrdID"]),
                checkpoint_1,
                case_params['TraderConnectivity2'],
                case_id
            )
        )

        er_sim_params = {
            'ClOrdID': '*',
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': '0',
            'OrderQty': sor_order_params['OrderQty'],
            'OrdType': case_params['OrdType'],
            'Side': case_params['Side'],
            'Price': case_params['Price'],
            'AvgPx': '0',
            'OrdStatus': '0',
            'ExecType': '0',
            'LeavesQty': '0',
            'Text': '*'
        }

        logger.debug("Verify received Execution Report (OrdStatus = New)")
        verifier.submitCheckRule(
            bca.create_check_rule(
                'ER NewOrderSingle transmitted << PARIS',
                bca.filter_to_grpc('ExecutionReport', er_sim_params, ["ClOrdID", "OrdStatus"]),
                checkpoint_1,
                case_params['TraderConnectivity2'],
                case_id,
                Direction.Value("SECOND")
            )
        )

        cancel_order_params = {
            'OrigClOrdID': sor_order_params['ClOrdID'],
            'ClOrdID': (sor_order_params['ClOrdID']),
            'Instrument': sor_order_params['Instrument'],
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
                bca.message_to_grpc('OrderCancelRequest', cancel_order_params, case_params['TraderConnectivity']),
            ))
        del new_er_params['Instrument']
        cancellation_er_params = {
            **new_er_params,
            'Instrument': sor_order_params['Instrument'],
            'ClOrdID': cancel_order_params['ClOrdID'],
            'OrigClOrdID': pending_er_params['ClOrdID'],
            'Text': cancel_order_params['Text'],
            'ExecID': '*',
            'NoParty': '*',
            'OrdStatus': '4',
            'ExecType': '4',
            'LeavesQty': '0'
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


    except Exception:
        logger.error("Error execution", exc_info=True)

    if timeouts:
        time.sleep(5)

    rule_man.remove_rule(NOS1)
    rule_man.remove_rule(OCR1)
    rule_man.print_active_rules()
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
