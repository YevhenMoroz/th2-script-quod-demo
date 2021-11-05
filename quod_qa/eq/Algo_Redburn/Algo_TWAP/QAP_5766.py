import os
import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#text
text_pn = 'Pending New status'
text_n = 'New status'
text_f = 'Fill'

#order param
qty = 300000
side = 1
price = 110
price_nav = 100
tif_day = 0
order_type = 2

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

#connectivity
case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-316-gnmd-rb"
connectivity_fh = 'fix-feed-handler-316-ganymede'

instrument = {
            'Symbol': 'FR0000062788_EUR',
            'SecurityID': 'FR0000062788',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_nav, price_nav, qty, qty, 0)

    return [nos_trade_rule1]


def rule_destroyer(list_rules):
    if list_rules is not None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def send_market_data(symbol: str, case_id: str, market_data):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntries': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', md_params, connectivity_fh)
    ))


def send_market_dataT(symbol: str, case_id: str, market_data):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntriesIR': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataIncrementalRefresh', md_params, connectivity_fh)
    ))


def execute(report_id):
    try:
        rule_list = rule_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager_316 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '100',
                'MDEntrySize': '100000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '105',
                'MDEntrySize': '100000',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data1)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        new_order_single_params = {
            'Account': client,
            'ClOrdID': 'TWAP_NAV_05_01' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif_day,
            'Price': price,
            'OrdType': order_type,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': currency,
            'TargetStrategy': 1005,
            'ExDestination': ex_destination_1,
            'QuodFlatParameters': {
                'NavigatorPercentage': '100',
                'NavigatorExecution': '1',
                'NavigatorInitialSweepTime': '10',
                'NavGuard': '0',
                'NavigatorLimitPrice': '100',
            }
        }

        fix_message_new_order_single = FixMessage(new_order_single_params)
        fix_message_new_order_single.add_random_ClOrdID()
        responce_new_order_single = fix_manager_316.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)

        time.sleep(1)

        nos_1 = dict(
            fix_message_new_order_single.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))

        fix_verifier_ss.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL7 receive 35=D')

        #region NavSlice with NavigatorInitialSweepTime
        #Check that FIXQUODSELL7 sent 35=8 pending new
        case_id_2 = bca.create_event("Nav child", case_id)
        er_1 = {
            'Account': client,
            'ExecID': '*',
            'OrderQty': qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Currency': currency,
            'TimeInForce': tif_day,
            'ExecType': "A",
            'HandlInst': new_order_single_params['HandlInst'],
            'LeavesQty': qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'Price': price_nav,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument

        }
        fix_verifier_ss.CheckExecutionReport(er_1, responce_new_order_single, case=case_id_2,   message_name='FIXQUODSELL7 sent 35=8 Pending New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        # Check that FIXQUODSELL7 sent 35=8 new
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            SettlType='*',
            ExecRestatementReason='*',
        )
        er_2.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_2, message_name='FIXQUODSELL7 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        er_3 = {
            'Account': account,
            'CumQty': qty,
            'LastPx': price_nav,
            'ExecID': '*',
            'OrderQty': qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'LastQty': qty,
            'Text': text_f,
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '*',
            'OrdStatus': '2',
            'Price': price_nav,
            'Currency': currency,
            'TimeInForce': tif_day,
            'Instrument': '*',
            'ExecType': "F",
            'ExDestination': ex_destination_1,
            'LeavesQty': '0'
        }
        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='BS FIXBUYTH2 sent 35=8 Nav Fill',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        #endregion

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_destroyer(rule_list)
