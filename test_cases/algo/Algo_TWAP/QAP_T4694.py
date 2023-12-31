import os
import logging
import time
from datetime import datetime, timedelta

from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager, Simulators
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 500
traded_qty = 350
traded_qty_2 = 150
side = 1
price = 20
price_2 = 19.995
tif_day = 0
tif_ioc = 3
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = 2
account = 'XPAR_CLIENT2'
currency = 'EUR'
waves = 2

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-316-ganymede"
connectivity_fh = 'fix-feed-handler-316-ganymede'

instrument = {
            'Symbol': 'FR0010263202_EUR',
            'SecurityID': 'FR0010263202',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
symbol = "1015"


def rule_creation():
    rule_manager = RuleManager(Simulators.algo)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(connectivity_buy_side, account, ex_destination_1, price, 150, 5000)
    ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, True, traded_qty, price_2)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [ioc_rule, ocr_rule, trade_rule, nos_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager(Simulators.algo)
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

def send_incremental(symbol: str, case_id: str, market_data):
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
        now = datetime.today() - timedelta(hours=3)


        rule_list = rule_creation();
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # region Send_MarkerData
        fix_manager_310 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = [
            {
                'MDEntryType': '1',
                'MDEntryPx': '19.995',
                'MDEntrySize': '350',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(symbol, case_id_0, market_data1)

        mdir_params_incremental = [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': price,
                    'MDEntrySize': '120',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]

        send_incremental(symbol, case_id_0, mdir_params_incremental)
        # endregion
        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        new_order_single_params = {
            'Account': client,
            'ClOrdID': 'QAP_4403_' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif_day,
            'OrdType': order_type,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Price': price,
            'Currency': currency,
            'TargetStrategy': 1005,
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'StartDate',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': now.strftime("%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'EndDate',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': (now + timedelta(minutes=5)).strftime("%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'WouldPriceReference',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LTP'
                },
                {
                    'StrategyParameterName': 'WouldPriceOffset',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '-1'
                },
                {
                    'StrategyParameterName': 'Waves',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '3'
                },
                {
                    'StrategyParameterName': 'MaxWouldShares',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '350'
                },

            ]
        }
        fix_message_new_order_single = FixMessage(new_order_single_params)
        responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single,
                                                                                   case=case_id_1)

        # Check that FIXQUODSELL5 receive 35=D
        nos_1 = dict(
            fix_message_new_order_single.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))

        fix_verifier_ss.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1,
                                            message_name='FIXQUODSELL5 receive 35=D')

        # Check that FIXQUODSELL5 sent 35=8 pending new
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
            'Price': price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument

        }
        fix_verifier_ss.CheckExecutionReport(er_1, responce_new_order_single, case=case_id_1,
                                             message_name='FIXQUODSELL5 sent 35=8 Pending New',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            ExecRestatementReason='*',
            SettlType= '*'
        )
        er_2.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1,
                                             message_name='FIXQUODSELL5 sent 35=8 New',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        # endregion
        # region Check Buy Side(1st slice)
        case_id_2 = bca.create_event("Check Buy Side(1st slice)", case_id)
        # Check bs (Quod sent 35=D)
        new_order_single_bs = {
            'NoParty': '*',
            'Account': account,
            'OrderQty': traded_qty,
            'OrdType': new_order_single_params['OrdType'],
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price_2,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce_new_order_single, case=case_id_2,
                                            message_name='BS FIXBUYTH2 sent 35=D New Order')

        # Check that Sim sent 35=8 pending new
        er_3 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': traded_qty,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price_2,
            'TimeInForce': tif_ioc,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'Text': '*',
            'LeavesQty': traded_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2,
                                             message_name='Sim sent 35=8 Pending New',
                                             key_parameters=['ExecType', 'OrdStatus'])

        # Check that Sim sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0",
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2,
                                             message_name='Sim   sent 35=8 New',
                                             key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])

        # Check that Sim sent 35=8 trade
        er_5 = dict(
            er_3,
            OrdStatus='2',
            ExecType="F",
            CumQty=traded_qty,
            LastPx=price_2,
            LastQty=traded_qty,
            OrderCapacity='A',
            AvgPx=price_2,
            Currency=currency,
            Instrument='*',
            LeavesQty=0
        )
        fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_2,
                                             message_name='Sim sent 35=8 Trade',
                                             key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])

        # endregion
        # region Check Buy Side (2nd slice)
        time.sleep(10)

        case_id_2 = bca.create_event("Check Buy Side(2nd slice)", case_id)
        # Check bs (Quod sent 35=D)
        new_order_single_bs = {
            'NoParty': '*',
            'Account': account,
            'OrderQty': qty - traded_qty,
            'OrdType': new_order_single_params['OrdType'],
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_day,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce_new_order_single, case=case_id_2,
                                            message_name='BS FIXBUYTH2 sent 35=D New Order', key_parameters=['Price', 'TimeInForce', 'OrderQty'])

        # Check that Sim sent 35=8 pending new
        er_3 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': qty - traded_qty,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price,
            'TimeInForce': tif_day,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'Text': '*',
            'LeavesQty': qty - traded_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2,
                                             message_name='Sim sent 35=8 Pending New',
                                             key_parameters=['ExecType', 'OrdStatus', 'OrderQty', 'TimeInForce','Price'])

        # Check that Sim sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0",
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2,
                                             message_name='Sim sent 35=8 New',
                                             key_parameters=['ExecType', 'OrdStatus', 'OrderQty', 'TimeInForce','Price'])

        # Check that Sim sent 35=8 trade
        er_5 = dict(
            er_3,
            OrdStatus='2',
            ExecType="F",
            CumQty=qty - traded_qty,
            LastPx=price,
            LastQty=qty - traded_qty,
            OrderCapacity='A',
            AvgPx=price,
            Currency=currency,
            Instrument='*',
            LeavesQty=0,
        )
        er_5.pop('ExDestination')
        fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_2,
                                             message_name='Sim sent 35=8 Trade',
                                             key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])

        # endregion
        # region Check sell-side
        time.sleep(1)
        case_id_3 = bca.create_event("Check sell-side", case_id)

        execution_report_fill = {
            'Account': '*',
            'LastQty': traded_qty_2,
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': '*',
            'AvgPx': '*',
            'OrdStatus': 2,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_day,
            'ExecType': 'F',
            'HandlInst': 2,
            'LeavesQty': 0,
            'CumQty': qty,
            'LastPx': price,
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': 'A',
            'QtyType': 0,
            'SettlType': '*',
            'Price': price,
            'TargetStrategy': 1005,
            'Instrument': '*',
            'NoParty': '*',
            'NoStrategyParameters': '*',
            'ExecID': '*',
            'OrderQty': qty,
            'LastExecutionPolicy': '*',
            'TradeDate': '*',
            'SecondaryOrderID': '*',
            'LastMkt': ex_destination_1,
            'Text': '*',
            'ExDestination': '*',
            'GrossTradeAmt': '*',
            'SecondaryExecID': '*'
        }
        fix_verifier_ss.CheckExecutionReport(execution_report_fill, responce_new_order_single, direction='FIRST', case=case_id_3,
                                                message_name='Quod sent 35=8 Fill', key_parameters=['OrderID', 'ExecType', 'OrdStatus'])
        # endregion
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_destroyer(rule_list)
