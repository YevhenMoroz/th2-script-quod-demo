import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, StrategyParameterType
from test_framework.fix_wrappers.algo.FixMessageNewOrderMultiLegAlgo import FixMessageNewOrderMultiLegAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRequestAlgo import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T4249(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region order parameters
        self.order_type = constants.OrderType.Market.value
        self.qty = 1000
        self.tif_day = constants.TimeInForce.Day.value
        self.spread_devi_type = "Currency"
        self.string_type = StrategyParameterType.String.value
        self.spread_devi_val = "5"
        self.spread_devi_val_mod = "6"
        self.float_type = StrategyParameterType.Float.value
        # endregion

        # region Gateway Side
        self.gateway_side_sell = GatewaySide.Sell
        self.gateway_side_buy = GatewaySide.Buy
        # endregion

        # region Status
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_pending = Status.Pending
        self.status_new = Status.New
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_pt")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_2")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send NewOrderSingle (35=D) for PairTrad order
        case_id_1 = bca.create_event("Create PairTrad Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.PairTrad_order = FixMessageNewOrderMultiLegAlgo(data_set=self.data_set).set_PairTrading_params()
        self.PairTrad_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.PairTrad_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, OrdType=self.order_type, Instrument=self.instrument))
        self.PairTrad_order.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='SpreadDeviationNumber', StrategyParameterType=self.float_type, StrategyParameterValue=self.spread_devi_val), 
                                                                            dict(StrategyParameterName='SpreadDeviationType', StrategyParameterType=self.string_type, StrategyParameterValue=self.spread_devi_type)])
        self.fix_manager_sell.send_message_and_receive_response(self.PairTrad_order, case_id_1)
        # endregion


        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.PairTrad_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_PairTrad_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.PairTrad_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_PairTrad_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_PairTrad_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.PairTrad_order, self.gateway_side_sell, self.status_new)
        
        self.fix_verifier_sell.check_fix_message(new_PairTrad_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        time.sleep(2)
        
        # region Send OCRR (35=G) for PairTrad order
        case_id_1 = bca.create_event("Modify PairTrad Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.PairTrad_order_mod = FixMessageOrderCancelReplaceRequestAlgo(self.PairTrad_order)
        self.PairTrad_order_mod.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='SpreadDeviationNumber', StrategyParameterType=self.float_type, StrategyParameterValue=self.spread_devi_val_mod)])\

        self.fix_manager_sell.send_message_and_receive_response(self.PairTrad_order_mod, case_id_1)
        
        er_replaced_PairTrad_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.PairTrad_order_mod, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(er_replaced_PairTrad_order_params, key_parameters=self.key_params_cl, message_name='Sell Side ExecReport Replace Request')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):        
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)

        cancel_request_PairTrad_order = FixMessageOrderCancelRequest(self.PairTrad_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_PairTrad_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_PairTrad_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        cancel_PairTrad_order = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.PairTrad_order_mod, self.gateway_side_sell, self.status_cancel)
        
        self.fix_verifier_sell.check_fix_message(cancel_PairTrad_order, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport Canceled')
        # endregion
