import os
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule, \
    TemplateNoPartyIDs
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager


def execute(report_id):
    rule_manager = RuleManager()
    trade_rule = rule_manager.add_SingleExec(
        [
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        200,
        {0: 200},
        {40: 40},
        {"XPAR": "3503"},
        "fix-bs-310-columbia",
        "fix-fh-310-columbia"
    )

    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager_qtwquod5 = FixManager('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_bs = FixVerifier('fix-bs-310-columbia', case_id)
    fix_manager_fh_paris = FixManager('fix-fh-310-columbia', case_id)
    fix_manager_fh_trqx = FixManager('fix-fh-310-columbia', case_id)

    symbol_paris = "924"
    symbol_trqx = "3464"

    mdfr_params = {
        'MDReportID': "1",
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '10',
                'MDEntrySize': '650',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '12',
                'MDEntrySize': '500',
                'MDEntryPositionNo': '1'
            }
        ]}
    fix_message_md_update = FixMessage(mdfr_params)
    fix_manager_fh_paris.Send_MarketDataFullSnapshotRefresh_FixMessage(fix_message_md_update, symbol_paris)
    fix_manager_fh_trqx.Send_MarketDataFullSnapshotRefresh_FixMessage(fix_message_md_update, symbol_trqx)
    # Send NewOrderSingle
    multilisting_params = {
        'Account': "CLIENT2",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "200",
        'TimeInForce': "4",
        'ExpireDate': '20210305',
        'Price': "40",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'FR0010307819_EUR',
            'SecurityID': 'FR0010307819',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1008",
        'NoStrategyParameters': [
            {
                'StrategyParameterName': 'AvailableVenues',
                'StrategyParameterType': '13',
                'StrategyParameterValue': 'true'
            },
            {
                'StrategyParameterName': 'AllowMissingPrimary',
                'StrategyParameterType': '13',
                'StrategyParameterValue': 'true'
            },
            {
                'StrategyParameterName': 'AllowedPassiveVenues',
                'StrategyParameterType': '14',
                'StrategyParameterValue': 'TRQX'
            }
        ]
    }

    fix_message_multilisting = FixMessage(multilisting_params)
    fix_message_multilisting.add_random_ClOrdID()
    responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_multilisting)

    #Check on ss
    er_params_new ={
        'ExecID': '*',
        'OrderQty': multilisting_params['OrderQty'],
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': multilisting_params['Side'],
        'AvgPx': '0',
        'OrdStatus': '0',
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'ExecType': "0",
        'HandlInst': multilisting_params['HandlInst'],
        'LeavesQty': multilisting_params['OrderQty'],
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(), 
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '0',
        'Price': multilisting_params['Price'],
        'TargetStrategy': multilisting_params['TargetStrategy'],
        'Instrument': multilisting_params['Instrument']
    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce)
    #Check on bs
    new_order_single_bs = {
        'NoParty': '*',
        'Account': multilisting_params['Account'],       
        'OrderQty': multilisting_params['OrderQty'],
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'TransactTime': '*',
        'ChildOrderID': '*',
        'Side': multilisting_params['Side'],
        'Price': multilisting_params['Price'],
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'Instrument': '*',
        'HandlInst': '1',
        'ExDestination': multilisting_params['Instrument']['SecurityExchange']
    }
    fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce)

    trade_er_params = {
        "OrdStatus": "2",
        'ExecType': "F",
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value
    }
    fix_verifier_ss.CheckExecutionReport(trade_er_params, responce )
    rule_manager.remove_rule(trade_rule)
