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

    # new order params
    instrument_1 = {
        'Symbol': 'FR0000032658_EUR',
        'SecurityID': 'FR0000032658',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }
    new_order_params = {
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '2',
        'OrderQty': 200,
        'TimeInForce': '0',
        'Price': 20,
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

    symbol = '1141'
    mdr_params = {
        'MDReportID': 1,
        'MDReqID': rule_manager.get_MDReqID(symbol, mask_conn),
        'Instrument': {'Symbol': symbol},
        'NoMDEntries':[
            {
                'MDEntryType': 0,
                'MDEntryPX': 15,
                'MDEntrySize': 200,
                'MDEntryPositionNo': 1
            },
            {
                'MDEntryType': 1,
                'MDEntryPX': 20,
                'MDEntrySize': 200,
                'MDEntryPositionNo': 1
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
                                             symbol={'XPAR':symbol},
                                             session=buy_side_conn,
                                             mask_as_connectivity=mask_conn)
    act.sendMessage(
        request=convert_to_request("Send Market Data", mask_conn, case_id,
                                   wrap_message(mdr_params, "MarketDataSnapShot", mask_conn))
    )
    new_order = Stubs.fix_act.placeOrderFIX(
        request=convert_to_request("Send new order", sell_side_conn, case_id,
                                   wrap_message(new_order_params, "NewOrderSingle", sell_side_conn))
    )
    rule_manager.remove_rule(trade_rule)


if __name__ == '__main__':
    execute()
    Stubs.factory.close()