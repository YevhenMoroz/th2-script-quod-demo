from stubs import Stubs
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request, \
    filter_to_grpc, create_check_sequence_rule, prefilter_to_grpc
from datetime import datetime, timedelta
from copy import deepcopy
from rule_management import RuleManager
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs, RequestMDRefID

def run_test_case():
    seconds, nanos = timestamps()
    case_name = "panyushkin_trade"
    sell_side_conn = "gtwquod3"
    buy_side_conn_1 = "fix-bs-eq-paris"
    buy_side_conn_2 = "fix-bs-eq-paris"
    rule_manager = RuleManager()
    
    instrument_1 = {
        'Symbol': 'FR0000065435_EUR',
        'SecurityID': 'FR0000065435',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }
    new_order_params = {
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '2',
        'OrderQty': 150,
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
        'TargetStrategy': '1011'
    }
    
    symbol_1 = "1411"
    
    params_1 = {
        'MDReportID': '1',
        'MDReqID': rule_manager.get_RequestMDRefID(symbol_1, buy_side_conn_2),
        'Instrument': {
            'Symbol': symbol_1 },
        'NoMDEntries': {
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPX': '12',
                    'MDEntrySize': '50',
                    'MDEntryPositionNo': '1' 
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPX': '14',
                    'MDEntrySize': '60',
                    'MDEntryPositionNo': '1'
                }
            ]
        }
    }
    
    
    Stubs.fix_act.sendMessage(request=convert_to_request( "Send MarketDataSnapshotFullRefresh", buy_side_conn_2, case_id,
                                                         wrap_message(params_1, "MarketDataSnapshotFullRefresh", buy_side_conn_2)))
    
    trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
            connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
            no_party_ids=[
                TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
                TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
                TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
            ],
            cum_qty=100,
            mask_as_connectivity="fix-fh-eq-paris",))

    entry_size = {20:50}
    entry_price = {14:12}
    
    new_order = Stubs.fix_act.placeOrderFIX(
        request=convert_to_request("Send new order", sell_side_conn, case_id,
                                   wrap_message(new_order_params, "NewOrderSingle", sell_side_conn)))
    
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
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'Price': new_order_params['Price'],
        'OrderQty': new_order_params['OrderQty'],
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'NoParty': [{
            'PartyID': f'{sell_side_conn}',
            'PartyIDSource': 'D',
            'PartyRole': '36'}],
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_params['OrderQty'],
        'Instrument': new_order_params['Instrument']
    }
        
    new_er_params = deepcopy(pending_er_params)
    new_er_params['Account'] = '#'
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = new_order_params['ClientAlgoPolicyID']
    new_er_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    new_er_params['ExecRestatementReason'] = '4'
    
    pre_filter_params = {'header': {'MsgType': ('0', "NOT_EQUAL")}}
    pre_filter = prefilter_to_grpc(pre_filter_params)
    message_filters_sell_side = [
        filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
        filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus'])]
    
    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side",
            prefilter=pre_filter,
            msg_filters=message_filters_sell_side,
            checkpoint=checkpoint_1,
            connectivity=sell_side_conn,
            event_id=case_id,
            timeout=2000

        )
    )
        
    rule_manager.remove_rule(trade_rule_1)
    print(f"Case {case_name} was executed")        
                
if __name__ == '__main__':
    run_test_case()
    Stubs.factory.close()                
    
