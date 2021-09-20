from copy import deepcopy
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request
from rule_management import RuleManager
from stubs import Stubs
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs
from th2_grpc_common.common_pb2 import ConnectionID, Direction


def execute():
    act = Stubs.fix_act
    verifier = Stubs.verifier
    sim = Stubs.simulator
    seoconds, nanos = bca.timestamps()
    sell_side_conn = "gtwquod3"
    buy_side_conn = "fix-bs-eq-paris"
    mask_conn = "fix-fh-eq-paris"
    rule_manager = RuleManager()

    case_name = "Test trade execution"
    case_id = bca.create_event(case_name)
    symbol = "1042"

    instrument_1 = {
        'Symbol': 'FR0010380626_EUR',
        'SecurityID': 'FR0010380626',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }
    new_order_params = {
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '2',
        'OrderQty': '200',
        'TimeInForce': '0',
        'Price': '10',
        'OrdType': '2',
        'ClOrdID': client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument_1,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
        'TargetStrategy': "1011"
    }

    mdr_params = {
        'MDReportID': '1',
        'MDReqID': rule_manager.get_MDReqID(symbol, mask_conn),
        'Instrument': {'Symbol': symbol},
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '15',
                'MDEntrySize': '200',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '20',
                'MDEntrySize': '200',
                'MDEntryPositionNo': '1'
            }
        ]
    }
    no_party_ids = [
        TemplateNoPartyIDs(party_id='KEPLER', party_id_source='D', party_role='1'),
        TemplateNoPartyIDs(party_id='1', party_id_source='D', party_role='2'),
        TemplateNoPartyIDs(party_id='2', party_id_source='D', party_role='3')
    ]
    cum_qty = 200
    entry_size = {200: 200}
    entry_price = {20: 15}

    trade_rule = rule_manager.add_SingleExec(party_id=no_party_ids,
                                             cum_qty=cum_qty,
                                             md_entry_size=entry_size,
                                             md_entry_px=entry_price,
                                             symbol={'XPAR': symbol},
                                             session=buy_side_conn,
                                             mask_as_connectivity=mask_conn)

    act.sendMessage(
        request=convert_to_request("Send Market Data", mask_conn, case_id,
                                   wrap_message(mdr_params, "MarketDataSnapshotFullRefresh", mask_conn))
    )

    new_order = act.placeOrderFIX(
        request=convert_to_request("Send new order", sell_side_conn, case_id,
                                   wrap_message(new_order_params, "NewOrderSingle", sell_side_conn))
    )

    checkpoint_1 = new_order.checkpoint_id

    pending_er_params = {
        'Account': new_order_params['Account'],
        'HandlInst': new_order_params['HandlInst'],
        'Side': new_order_params['Side'],
        'TimeInForce': new_order_params['TimeInForce'],
        'OrdType': new_order_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': new_order_params['TargetStrategy'],
        'ClOrdID': new_order_params['ClOrdID'],
        'OrderID': "*",
        'ExecID': "*",
        'TransactTime': '*',
        'Price': new_order_params['Price'],
        'OrderQty': new_order_params['OrderQty'],
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_params['OrderQty'],
        'Instrument': new_order_params['Instrument'],
        'NoParty': [{
            'PartyID': sell_side_conn,
            'PartyIDSource': 'D',
            'PartyRole': '36'
        }]
    }

    new_er_params = deepcopy(pending_er_params)
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = new_order_params['ClientAlgoPolicyID']
    new_er_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    new_er_params['ExecRestatementReason'] = '4'
    new_er_params['Account'] = "#"

    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL")
        }
    }
    pre_filter_sim = bca.prefilter_to_grpc(pre_filter_sim_params)

    message_filters_sell = [
        bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
        bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus'])
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_sell,
            checkpoint=checkpoint_1,
            connectivity=sell_side_conn,
            event_id=case_id,
        )
    )

    buy_side_instrument = {
        'SecurityType': 'CS',
        'Symbol': 'PROL',
        'SecurityID': 'FR0010380626',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    # new order single params for buy side
    order_params_buys_side = deepcopy(new_order_params)
    order_params_buys_side.pop("ClientAlgoPolicyID")
    order_params_buys_side.pop("ComplianceID")
    order_params_buys_side.pop("TargetStrategy")
    order_params_buys_side["ClOrdID"] = "*"
    order_params_buys_side["TransactTime"] = "*"
    order_params_buys_side["ChildOrderID"] = "*"
    order_params_buys_side["SettlDate"] = "*"
    order_params_buys_side["Instrument"] = buy_side_instrument
    order_params_buys_side["HandlInst"] = "1"
    order_params_buys_side["ExDestination"] = "XPAR"
    message_filters_nos_bs = [bca.filter_to_grpc("NewOrderSingle", order_params_buys_side, ["SecurityID"])]

    # request for module check1, which compares NOS message from the buy side
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_nos_bs,
            checkpoint=checkpoint_1,
            connectivity=buy_side_conn,
            event_id=case_id
        )
    )

    # Execution report params for buy side
    er_params_buy_side = {
        "Account": new_order_params['Account'],
        "OrderID": "*",
        "ExecID": "*",
        "ExecType": "F",
        "OrdStatus": "0",
        "CumQty": cum_qty,
        "LastPx": "10",
        "LastQty": "200",
        "OrderCapacity": "A",
        "AvgPx": "10",
        "OrdStatus": "2",
        "Currency": new_order_params['Currency'],
        "TimeInForce": new_order_params['TimeInForce'],
        "Instrument": buy_side_instrument,
        "Text": "Hello sim",
        "LeavesQty": "0",
        "TransactTime": "*",
        "OrderQty": new_order_params["OrderQty"],
        "OrdType": new_order_params["OrdType"],
        "ClOrdID": "*",
        "Side": new_order_params["Side"],
        "Price": new_order_params["Price"],
        "NoParty": [
            {
                'PartyID': 'KEPLER',
                'PartyIDSource': 'D',
                'PartyRole': '1'
            },
            {
                'PartyID': '1',
                'PartyIDSource': 'D',
                'PartyRole': '2'
            },
            {
                'PartyID': '2',
                'PartyIDSource': 'D',
                'PartyRole': '3'
            }
        ]
    }
    message_filters_er_bs = [bca.filter_to_grpc("ExecutionReport", er_params_buy_side)]

    # request for module check1, which compares the NOS message from the buy side
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_er_bs,
            checkpoint=checkpoint_1,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.Value("SECOND")
        )
    )
    rule_manager.remove_rule(trade_rule)


if __name__ == '__main__':
    execute()
    Stubs.factory.close()
