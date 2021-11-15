import os
import logging
import time
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from rule_management import RuleManager
from quod_qa.wrapper_test.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from quod_qa.wrapper_test.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test import DataSet
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#order param
qty = 100000
side = 1
price = 30
price_nav = 20
tif_day = 0
order_type = 2
nav_exec = 1
nav_init_sweep = 10

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

#connectivity
case_name = os.path.basename(__file__)
FIRST = DataSet.DirectionEnum.FIRST.value
SECOND = DataSet.DirectionEnum.SECOND.value
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value
instrument = DataSet.Instrument.BUI.value

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_nav)
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_nav, price_nav, qty, qty, 0)

    return [nos_rule, nos_trade_rule1]


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
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
        fix_manager = FixManager(connectivity_sell_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '100000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
                'MDEntrySize': '100000',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data1)

        time.sleep(3)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        fix_message = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator()
        fix_message.add_ClordId((os.path.basename(__file__)[:-3]))
        fix_message.change_parameters(dict(Account= client,  OrderQty = qty))
        fix_message.update_fields_in_component('QuodFlatParameters', dict(NavigatorExecution= nav_exec, NavigatorInitialSweepTime= nav_init_sweep, NavigatorLimitPrice= price_nav))

        fix_manager.send_message_and_receive_response(fix_message, case_id_1)
        #endregion

        time.sleep(3)

        #region Check Sell side
        fix_verifier_ss.check_fix_message(fix_message, direction=SECOND, message_name='Sell side 35=D')

        exec_report = FixMessageExecutionReportAlgo().execution_report(fix_message)
        fix_verifier_ss.check_fix_message(exec_report, message_name='Sell side Pending new')

        exec_report_2 = FixMessageExecutionReportAlgo().execution_report(fix_message).change_from_pending_new_to_new()
        fix_verifier_ss.check_fix_message(exec_report_2, message_name='Sell side New')
        #endregion

        #region Check Buy side
        case_id_2 = bca.create_event("First TWAP slice", case_id)
        fix_verifier_bs.set_case_id(case_id_2)

        navigator_child = FixMessageNewOrderSingleAlgo().set_DMA()
        navigator_child.change_parameter('OrderQty', qty)
        fix_verifier_bs.check_fix_message(navigator_child, key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'], message_name='Buy side 35=D')

        exec_report_3 = FixMessageExecutionReportAlgo().execution_report_buy(navigator_child)
        fix_verifier_bs.check_fix_message(exec_report_3, direction=SECOND, message_name='Buy side Pending new')

        exec_report_4 = FixMessageExecutionReportAlgo().execution_report_buy(navigator_child).change_buy_from_new_to_pendingnew()
        fix_verifier_bs.check_fix_message(exec_report_4, direction=SECOND, message_name='Buy side New')

        exec_report_5 = FixMessageExecutionReportAlgo().execution_report_fill_buy(navigator_child)
        fix_verifier_bs.check_fix_message(exec_report_5, direction=SECOND, message_name='Buy side Navigator Fill')
        #endregion
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rule_list)