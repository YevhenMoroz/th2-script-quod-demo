import os
import logging
import time
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#order param
qty = 100000
price = 30
price_nav = 20
tif_day = 0
order_type = 2
nav_init_sweep = 10

#Key parameters
key_params_cl = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
key_params=['OrdStatus', 'ExecType', 'OrderQty', 'Price']

#Gateway Side
gateway_side_buy = DataSet.GatewaySide.Buy
gateway_side_sell = DataSet.GatewaySide.Sell

#Status
status_pending = DataSet.Status.Pending
status_new = DataSet.Status.New
status_fill = DataSet.Status.Fill

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

#connectivity
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.BUI
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value

def rules_creation():
    rule_manager = RuleManager(Simulators.algo)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_nav)
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_nav, price_nav, qty, qty, 0)

    return [nos_rule, nos_trade_rule1]

def execute(report_id):
    try:
        rules_list = rules_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)

        # Send_MarkerData
        fix_manager_fh.set_case_id(bca.create_event("Send Market Data", case_id))
        market_data_snapshot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        fix_manager_fh.send_message(market_data_snapshot)

        time.sleep(3)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        twap_nav_order = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator_params()
        twap_nav_order.add_ClordId((os.path.basename(__file__)[:-3]))
        twap_nav_order.change_parameters(dict(Account= client, OrderQty = qty))
        twap_nav_order.update_fields_in_component('QuodFlatParameters', dict(NavigatorInitialSweepTime= nav_init_sweep, NavigatorLimitPrice= price_nav))

        fix_manager.send_message_and_receive_response(twap_nav_order, case_id_1)
        #endregion

        time.sleep(3)

        #region Check Sell side
        fix_verifier_ss.check_fix_message(twap_nav_order, direction=ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_pending)
        fix_verifier_ss.check_fix_message(pending_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_new)
        fix_verifier_ss.check_fix_message(new_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport New')
        #endregion

        #region Check Buy side
        fix_verifier_bs.set_case_id(bca.create_event("First TWAP slice", case_id))

        nav_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_child.change_parameter('OrderQty', qty)
        fix_verifier_bs.check_fix_message(nav_child, key_parameters=key_params, message_name='Buy side NewOrderSingle Navigator')

        pending_nav_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_nav_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew Navigator')

        new_nav_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_nav_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New Navigator')

        fill_nav_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child, gateway_side_buy, status_fill)
        fix_verifier_bs.check_fix_message(fill_nav_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Fill Navigator')
        #endregion

        #region Check Parent order fill
        fix_verifier_ss.set_case_id(bca.create_event("Check parent order Fill", case_id))

        fill_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_fill)
        fix_verifier_ss.check_fix_message(fill_twap_nav_order_params, key_parameters=key_params, message_name='Sell side ExecReport Fill')
        #endregion
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(rules_list)