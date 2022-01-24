import os
import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.algo_formulas_manager import AlgoFormulasManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#order param
ats = 10000
price_twap_child = 29.995
price_would = 31
price_bid = 30
price_ask = 40
qty_bid = qty_ask = 1000000
qty = 75000
qty_would = 10000
waves = 5
qty_twap_child = AlgoFormulasManager.get_next_twap_slice(qty, waves)
qty_nav_child1 = AlgoFormulasManager.get_twap_nav_child_qty(qty, waves, ats)
qty_nav_rebalance = AlgoFormulasManager.get_nav_reserve(qty, waves, ats)
nav_rebalance_time = 15

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
status_partial_fill = DataSet.Status.PartialFill
status_cancel = DataSet.Status.Cancel

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
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_twap_child)
    nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_would)
    nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, False, 0, price_would)
    trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_would, price_would, qty_nav_child1, qty_nav_child1, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    
    return [nos_rule, nos_rule2, nos_ioc_rule, trade, ocr_rule]


def execute(report_id):
    try:
        rules_list = rules_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)
        
        # Send_MarketData
        fix_manager_fh.set_case_id(bca.create_event("Send Market Data", case_id))
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=price_bid, MDEntrySize=qty_bid)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=qty_ask)
        fix_manager_fh.send_message(market_data_snap_shot)
        
        time.sleep(3)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)
        
        twap_nav_order = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator_params().add_ClordId((os.path.basename(__file__)[:-3]))
        twap_nav_order.change_parameters(dict(OrderQty=qty, Account=client, Price=price_would))
        twap_nav_order.update_fields_in_component("QuodFlatParameters", dict(TriggerPriceRed=price_would, NavigatorRebalanceTime=nav_rebalance_time, Waves=waves))

        fix_manager.send_message_and_receive_response(twap_nav_order, case_id_1)

        time.sleep(1)

        # region Check Sell side
        fix_verifier_ss.check_fix_message(twap_nav_order, direction=ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_pending)
        fix_verifier_ss.check_fix_message(pending_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_new)
        fix_verifier_ss.check_fix_message(new_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check First TWAP slice
        # First TWAP child order
        fix_verifier_bs.set_case_id(bca.create_event("First TWAP slice", case_id))

        twap_1_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_1_child.change_parameters(dict(OrderQty=qty_twap_child, Price=price_twap_child))
        fix_verifier_bs.check_fix_message(twap_1_child, key_parameters=key_params, message_name='Buy side NewOrderSingle First TWAP')

        pending_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_twap_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew First TWAP')

        new_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_twap_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New First TWAP')

        #First Navigator child order
        nav_1_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_1_child.change_parameters(dict(OrderQty=qty_nav_child1, Price=price_would))
        fix_verifier_bs.check_fix_message(nav_1_child, key_parameters=key_params, message_name='Buy side NewOrderSingle First TWAP')

        pending_nav_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_1_child, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_nav_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew First Navigator')

        new_nav_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_1_child, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_nav_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New First Navigator')

        time.sleep(1)

        fill_nav_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_1_child, gateway_side_buy, status_fill)
        fix_verifier_bs.check_fix_message(fill_nav_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Fill First Navigator')
        # endregion

        # region Rebalance navigator child
        # endregion

        time.sleep(5)
        market_data_snap_shot_2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot_2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=price_bid, MDEntrySize=qty_bid)
        market_data_snap_shot_2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_would, MDEntrySize=qty_would)
        fix_manager_fh.send_message(market_data_snap_shot_2)

        time.sleep(5)
        market_data_snap_shot_3 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot_3.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=price_bid, MDEntrySize=qty_bid)
        market_data_snap_shot_3.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=qty_ask)
        fix_manager_fh.send_message(market_data_snap_shot_3)

        time.sleep(10)
        order_cancel = FixMessageOrderCancelRequest(twap_nav_order)
        fix_manager.send_message_and_receive_response(order_cancel)
        
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rules_list)
