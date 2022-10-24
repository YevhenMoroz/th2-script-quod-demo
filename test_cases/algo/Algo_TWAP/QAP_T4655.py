import os
import logging
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.algo_formulas_manager import AlgoFormulasManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#order param
tick = 0.005
qty = 2000
price_parent = 22
price_ask = 21
price_bid = 19.98
price_trigger = price_ask + tick
would_price_reference = 'MAN'
would_price_offset = 1
price_would = AlgoFormulasManager.calc_ticks_offset_minus(price_trigger, would_price_offset, tick)
tif_ioc = 3

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
s_par = '1015'

#connectivity
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.PAR.value
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value


def rules_creation():
    rule_manager = RuleManager(Simulators.algo)
    nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, True, qty, price_ask)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [nos_ioc_rule, ocr_rule]

def execute(report_id):
    try:
        rules_list = rules_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        now = datetime.today() - timedelta(hours=3)

        # Send_MarkerData
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)

        # Send_MarkerData
        fix_manager_fh.set_case_id(bca.create_event("Send Market Data", case_id))
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=price_bid, MDEntrySize=qty)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=qty)
        fix_manager_fh.send_message(market_data_snap_shot)

        time.sleep(3)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        twap_would_order = FixMessageNewOrderSingleAlgo().set_TWAP_params()
        twap_would_order.add_ClordId((os.path.basename(__file__)[:-3]))
        twap_would_order.change_parameters(dict(Account= client, OrderQty = qty, Price=price_parent))
        twap_would_order.update_fields_in_component('QuodFlatParameters', dict(StartDate2=now.strftime("%Y%m%d-%H:%M:%S"), EndDate2=(now + timedelta(minutes=4)).strftime("%Y%m%d-%H:%M:%S"), WouldPriceReference=would_price_reference, WouldPriceOffset=would_price_offset, TriggerPriceRed=price_trigger))

        fix_manager.send_message_and_receive_response(twap_would_order, case_id_1)

        time.sleep(3)
        
        #region Check Sell side
        fix_verifier_ss.check_fix_message(twap_would_order, direction=ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_would_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_would_order, gateway_side_sell, status_pending)
        fix_verifier_ss.check_fix_message(pending_twap_would_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_would_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_would_order, gateway_side_sell, status_new)
        fix_verifier_ss.check_fix_message(new_twap_would_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport New')
        #endregion

        #Check First TWAP child
        fix_verifier_bs.set_case_id(bca.create_event("First TWAP slice", case_id))

        twap_1_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_1_child.change_parameters(dict(OrderQty=qty, Price=price_would, TimeInForce=tif_ioc, Instrument=instrument))
        fix_verifier_bs.check_fix_message(twap_1_child, key_parameters=key_params, message_name='Buy side NewOrderSingle TWAP child')

        pending_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_twap_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew TWAP child')

        new_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_twap_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New TWAP child')

        fill_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, gateway_side_buy, status_fill)
        fix_verifier_bs.check_fix_message(fill_twap_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Fill TWAP child')
        #endregion

        time.sleep(3)

        # region Fill Algo Order
        case_id_4 = bca.create_event("Fill Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_4)
        # Fill Order
        fill_twap_would_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_would_order, gateway_side_sell, status_fill)
        fix_verifier_ss.check_fix_message(fill_twap_would_order, key_parameters=key_params_cl, message_name='Sell side ExecReport Fill')
        #endregion

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(rules_list)

