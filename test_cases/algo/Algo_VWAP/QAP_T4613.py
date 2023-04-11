# import os
# import logging
# import time
# import math
# from datetime import datetime, timedelta
# from copy import deepcopy
# from custom import basic_custom_actions as bca
# from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
# from th2_grpc_common.common_pb2 import ConnectionID, Direction
# from test_framework.old_wrappers.fix_manager import FixManager
# from test_framework.old_wrappers.fix_message import FixMessage
# from test_framework.old_wrappers.fix_verifier import FixVerifier
# from rule_management import RuleManager, Simulators
# from stubs import Stubs
# from custom.basic_custom_actions import message_to_grpc, convert_to_request
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# timeouts = True
#
# # text
# text_pn = 'Pending New status'
# text_n = 'New status'
# text_c = 'order canceled'
# text_f = 'Fill'
# text_r = 'order replaced'
#
# # algo param
# waves = 4
# aggressivity = 1
#
# # order param
# self.qty = 40
# price = 20
# wld_price = 19.995
# child_day_qty = round(qty / waves)
# side = 1
# tif_day = 0
# tif_ioc = 3
# order_type = 2
#
# # venue param
# ex_destination_1 = "XPAR"
# client = "CLIENT2"
# account = 'XPAR_CLIENT2'
# currency = 'EUR'
# s_par = '704'
#
# case_name = os.path.basename(__file__)
# connectivity_buy_side = "fix-buy-side-316-ganymede"
# connectivity_sell_side = "fix-sell-side-316-ganymede"
# connectivity_fh = 'fix-feed-handler-316-ganymede'
#
# instrument = {
#     'Symbol': 'FR0010436584_EUR',
#     'SecurityID': 'FR0010436584',
#     'SecurityIDSource': '4',
#     'SecurityExchange': 'XPAR'
# }
#
#
# def rule_creation():
#     rule_manager = RuleManager(Simulators.algo)
#     nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, True, qty, wld_price)
#     ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
#     return [nos_ioc_rule, ocr_rule]
#
#
# def rule_destroyer(list_rules):
#     if list_rules != None:
#         rule_manager = RuleManager(Simulators.algo)
#         for rule in list_rules:
#             rule_manager.remove_rule(rule)
#
#
# def send_market_data(symbol: str, case_id :str, market_data ):
#     MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
#         symbol=symbol,
#         connection_id=ConnectionID(session_alias=connectivity_fh)
#     )).MDRefID
#     md_params = {
#         'MDReqID': MDRefID,
#         'NoMDEntries': market_data
#     }
#
#     Stubs.fix_act.sendMessage(request=convert_to_request(
#         'Send MarketDataSnapshotFullRefresh',
#         connectivity_fh,
#         case_id,
#         message_to_grpc('MarketDataSnapshotFullRefresh', md_params, connectivity_fh)
#     ))
#
#
# def send_market_dataT(symbol: str, case_id: str, market_data):
#     MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
#         symbol=symbol,
#         connection_id=ConnectionID(session_alias=connectivity_fh)
#     )).MDRefID
#     md_params = {
#         'MDReqID': MDRefID,
#         'NoMDEntriesIR': market_data
#     }
#
#     Stubs.fix_act.sendMessage(request=convert_to_request(
#         'Send MarketDataIncrementalRefresh',
#         connectivity_fh,
#         case_id,
#         message_to_grpc('MarketDataIncrementalRefresh', md_params, connectivity_fh)
#     ))
#
#
# def execute(report_id):
#     try:
#         now = datetime.today() - timedelta(hours=3)
#         waves = 4
#
#         rule_list = rule_creation()
#         case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
#         # Send_MarkerData
#         fix_manager_310 = FixManager(connectivity_sell_side, case_id)
#         fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
#         fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
#
#         case_id_0 = bca.create_event("Send Market Data", case_id)
#         market_data1 = [
#             {
#                 'MDEntryType': '0',
#                 'MDEntryPx': 19.99,
#                 'MDEntrySize': qty,
#                 'MDEntryPositionNo': '1'
#             },
#             {
#                 'MDEntryType': '1',
#                 'MDEntryPx': wld_price,
#                 'MDEntrySize': qty,
#                 'MDEntryPositionNo': '1'
#             }
#         ]
#         send_market_data(s_par, case_id_0, market_data1)
#
#         market_data2 = [
#             {
#                 'MDUpdateAction': '0',
#                 'MDEntryType': '2',
#                 'MDEntryPx': 20,
#                 'MDEntrySize': qty,
#                 'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
#                 'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
#             }
#         ]
#         send_market_dataT(s_par, case_id_0, market_data2)
#
#         time.sleep(3)
#
#         # region Send NewOrderSingle (35=D)
#         case_id_1 = bca.create_event("Create Algo Order", case_id)
#         new_order_single_params = {
#             'Account': client,
#             'ClOrdID': 'QAP_4733_' + bca.client_orderid(9),
#             'HandlInst': 2,
#             'Side': side,
#             'OrderQty': qty,
#             'TimeInForce': tif_day,
#             'OrdType': order_type,
#             'TransactTime': datetime.utcnow().isoformat(),
#             'Instrument': instrument,
#             'OrderCapacity': 'A',
#             'Price': price,
#             'Currency': currency,
#             'TargetStrategy': 1,
#             'ExDestination': ex_destination_1,
#             'NoStrategyParameters': [
#                 {
#                     'StrategyParameterName': 'StartDate',
#                     'StrategyParameterType': '19',
#                     'StrategyParameterValue': now.strftime("%Y%m%d-%H:%M:%S")
#                 },
#                 {
#                     'StrategyParameterName': 'EndDate',
#                     'StrategyParameterType': '19',
#                     'StrategyParameterValue': (now + timedelta(minutes=20)).strftime("%Y%m%d-%H:%M:%S")
#                 },
#                 {
#                     'StrategyParameterName': 'Aggressivity',
#                     'StrategyParameterType': '1',
#                     'StrategyParameterValue': aggressivity
#                 },
#                 {
#                     'StrategyParameterName': 'WouldPriceReference',
#                     'StrategyParameterType': '14',
#                     'StrategyParameterValue': 'PRM'
#                 },
#                 {
#                     'StrategyParameterName': 'WouldPriceOffset',
#                     'StrategyParameterType': '1',
#                     'StrategyParameterValue': '1'
#                 }
#             ]
#         }
#
#         fix_message_new_order_single = FixMessage(new_order_single_params)
#         responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)
#
#         time.sleep(1)
#
#         nos_1 = dict(
#             fix_message_new_order_single.get_parameters(),
#             TransactTime='*',
#             ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))
#
#         fix_verifier_ss.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL5 receive 35=D')
#
#         # Check that FIXQUODSELL5 sent 35=8 pending new
#         er_1 = {
#             'Account': client,
#             'ExecID': '*',
#             'OrderQty': qty,
#             'NoStrategyParameters': '*',
#             'LastQty': '0',
#             'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
#             'TransactTime': '*',
#             'Side': side,
#             'AvgPx': '0',
#             'OrdStatus': 'A',
#             'Currency': currency,
#             'TimeInForce': tif_day,
#             'ExecType': "A",
#             'HandlInst': new_order_single_params['HandlInst'],
#             'LeavesQty': qty,
#             'NoParty': '*',
#             'CumQty': '0',
#             'LastPx': '0',
#             'OrdType': order_type,
#             'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
#             'OrderCapacity': new_order_single_params['OrderCapacity'],
#             'QtyType': '0',
#             'Price': price,
#             'TargetStrategy': new_order_single_params['TargetStrategy'],
#             'Instrument': instrument
#
#         }
#         fix_verifier_ss.CheckExecutionReport(er_1, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 Pending New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
#
#         # Check that FIXQUODSELL5 sent 35=8 new
#         er_2 = dict(
#             er_1,
#             ExecType="0",
#             OrdStatus='0',
#             SettlDate='*',
#             SettlType='*',
#             ExecRestatementReason='*',
#         )
#         er_2.pop('Account')
#         fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
#
#         # region IOC
#         case_id_2 = bca.create_event("Check IOC Order", case_id)
#         # Check bs (FIXQUODSELL5 sent 35=D IOC)
#         ioc_order = {
#             'NoParty': '*',
#             'Account': account,
#             'OrderQty': qty,
#             'OrdType': order_type,
#             'ClOrdID': '*',
#             'OrderCapacity': new_order_single_params['OrderCapacity'],
#             'TransactTime': '*',
#             'Side': side,
#             'Price': wld_price,
#             'SettlDate': '*',
#             'Currency': currency,
#             'TimeInForce': tif_ioc,
#             'Instrument': '*',
#             'HandlInst': '1',
#             'ExDestination': instrument['SecurityExchange']
#         }
#         fix_verifier_bs.CheckNewOrderSingle(ioc_order, responce_new_order_single, case=case_id_2, message_name='BS FIXBUYTH2 sent 35=D IOC New order Slice 1', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])
#
#         # Check that FIXBUYQUOD5 sent 35=8 IOC pending new
#         er_3 = {
#             'Account': account,
#             'CumQty': '0',
#             'ExecID': '*',
#             'OrderQty': qty,
#             'Text': text_pn,
#             'OrdType': '2',
#             'ClOrdID': '*',
#             'OrderID': '*',
#             'TransactTime': '*',
#             'Side': side,
#             'AvgPx': '0',
#             'OrdStatus': 'A',
#             'Price': wld_price,
#             'TimeInForce': tif_ioc,
#             'ExecType': "A",
#             'ExDestination': ex_destination_1,
#             'LeavesQty': qty
#         }
#
#         fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 IOC Pending New Slice 1', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])
#
#         # Check that FIXBUYQUOD5 sent 35=8 new
#         er_4 = dict(
#             er_3,
#             OrdStatus='0',
#             ExecType="0",
#             Text=text_n,
#         )
#         fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 IOC New Slice 1', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])
#
#         er_5 = {
#             'Account': account,
#             'CumQty': qty,
#             'LastPx': wld_price,
#             'ExecID': '*',
#             'OrderQty': qty,
#             'OrdType': order_type,
#             'ClOrdID': '*',
#             'LastQty': qty,
#             'Text': text_f,
#             'OrderCapacity': new_order_single_params['OrderCapacity'],
#             'OrderID': '*',
#             'TransactTime': '*',
#             'Side': side,
#             'AvgPx': '*',
#             'OrdStatus': '2',
#             'Price': wld_price,
#             'Currency': currency,
#             'TimeInForce': tif_ioc,
#             'Instrument': '*',
#             'ExecType': "F",
#             'ExDestination': ex_destination_1,
#             'LeavesQty': '0'
#         }
#         fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='BS FIXBUYTH2 sent 35=8 IOC Fill', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
#         # endregion
#
#         time.sleep(2)
#
#         # region Cancel Algo Order
#         case_id_5 = bca.create_event("Fill Algo Order", case_id)
#         # Check ss (on FIXQUODSELL5 sent 35=8 on cancel)
#         er_12 = {
#             'Account': '*',
#             'ExecID': '*',
#             'OrderQty': qty,
#             'NoStrategyParameters': '*',
#             'LastQty': qty,
#             'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
#             'TransactTime': '*',
#             'Side': side,
#             'AvgPx': '*',
#             "OrdStatus": "2",
#             'SettlDate': '*',
#             'LastExecutionPolicy': '*',
#             'Currency': currency,
#             'TimeInForce': tif_day,
#             'TradeDate': '*',
#             'ExecType': 'F',
#             'HandlInst': new_order_single_params['HandlInst'],
#             'LeavesQty': '0',
#             'NoParty': '*',
#             'CumQty': qty,
#             'LastPx': wld_price,
#             'OrdType': order_type,
#             'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
#             'SecondaryOrderID': '*',
#             'LastMkt': ex_destination_1,
#             'Text': text_f,
#             'OrderCapacity': new_order_single_params['OrderCapacity'],
#             'QtyType': '0',
#             'SettlType': '*',
#             'Price': price,
#             'TargetStrategy': new_order_single_params['TargetStrategy'],
#             'Instrument': '*',
#             'SecondaryExecID': '*',
#             'ExDestination': ex_destination_1,
#             'GrossTradeAmt': '*'
#         }
#
#         fix_verifier_ss.CheckExecutionReport(er_12, responce_new_order_single, case=case_id_5, message_name='SS FIXSELLQUOD5 sent 35=8 Fill', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID'])
#         # endregion
#     except:
#         logging.error("Error execution", exc_info=True)
#     finally:
#         rule_destroyer(rule_list)

import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets import constants
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.data_sets.constants import TradingPhases, Reference
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.algo_mongo_manager import AlgoMongoManager as AMM
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import \
    FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from datetime import datetime, timedelta
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager

from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T4613(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        self.restapi_env1 = self.environment.get_list_web_admin_rest_api_environment()[0]
        # endregion

        # region Market data params
        self.price_ask = 19.995
        self.qty_ask = 2000

        self.price_bid = 19.99
        self.qty_bid = 2000
        # endregion

        self.last_trade_price = 20
        self.last_trade_qty = 1000

        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.historical_volume = 15.0
        self.aggressivity = constants.Aggressivity.Passive.value

        # order params
        self.qty = 45
        self.price = 20
        self.waves = 3
        self.qty_child = 45
        self.price_child = 19.995
        # endregion

        # region Algo params
        self.would_reference_price = Reference.Primary.value
        self.would_price_offset = -1
        # endregion


        # region Venue params
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        # Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_1')
        self.key_params = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_3')
        self.key_params_mkt = self.data_set.get_verifier_key_parameters_by_name('verifier_key_parameters_4')
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        self.status_reject = Status.Reject
        self.status_eliminate = Status.Eliminate
        self.status_fill = Status.Fill
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.rule_list = []

        # # region SSH
        # self.config_file = "client_sats.xml"
        # self.xpath = ".//bpsOffsets"
        # self.new_config_value = 'false'
        # self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        # self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user, self.ssh_client_env.password, self.ssh_client_env.su_user, self.ssh_client_env.su_password)
        # self.default_config_value = self.ssh_client.get_and_update_file(self.config_file, {self.xpath: self.new_config_value})
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.now = datetime.utcnow()
        self.end_date = (self.now + timedelta(minutes=5)).strftime("%Y%m%d-%H:%M:%S")
        self.start_date = self.now.strftime("%Y%m%d-%H:%M:%S")

        # # region precondition: Prepare SATS configuration
        # self.ssh_client.send_command("qrestart SATS")
        # time.sleep(35)
        # # endregion

        # region rules
        rule_manager = RuleManager(Simulators.algo)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, self.qty_child, self.price_child)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_ioc_rule, ocr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.Open)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region insert data into mongoDB
        curve = AMM.get_straight_curve_for_mongo(trading_phases, volume=self.historical_volume)
        self.db_manager.insert_many_to_mongodb_with_drop(curve, f"Q{self.listing_id}")
        bca.create_event("Data in mongo inserted", self.test_id)
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region send trading phase
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.last_trade_qty).update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.last_trade_price)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle (35=D)
        self.case_id_1 = bca.create_event("Create Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_1)

        self.vwap_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_VWAP_Redburn_params()
        self.vwap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.vwap_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.vwap_order.update_fields_in_component('QuodFlatParameters', dict(Waves=self.waves, WouldPriceReference=self.would_reference_price, WouldPriceOffset=self.would_price_offset, StartDate2=self.start_date, EndDate2=self.end_date))

        self.vwap_order.update_fields_in_component('QuodFlatParameters', dict(Waves=self.waves, StartDate2=self.start_date, EndDate2=self.end_date, WouldPriceReference=self.would_reference_price, WouldPriceOffset=self.would_price_offset))

        self.fix_manager_sell.send_message_and_receive_response(self.vwap_order, self.case_id_1)
        # endregion
        time.sleep(5)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.vwap_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle', )

        pending_vwap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_vwap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_vwap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_vwap_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check VWAP child
        self.case_id_2 = bca.create_event("vwap DMA child order", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_2)

        self.vwap_child = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        self.vwap_child.change_parameters(dict(Price=self.price_child, OrderQty=self.qty_child, Account=self.account, Instrument='*', ExDestination=self.ex_destination_1, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.vwap_child, key_parameters=self.key_params, message_name='Buy side NewOrderSingle VWAP child')

        pending_vwap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_child, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_vwap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew VWAP child')

        new_vwap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_child, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_vwap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New VWAP child')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region cancel Order
        self.case_id_cancel = bca.create_event("Check Fill Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(self.case_id_cancel)

        time.sleep(3)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # # region config reset
        # self.default_config_value = self.ssh_client.get_and_update_file(self.config_file, {self.xpath: self.new_config_value})
        # self.ssh_client.send_command("qrestart SATS")
        # time.sleep(35)
        # self.ssh_client.close()
        # # endregion

        cancel_vwap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_child, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(cancel_vwap_child_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill VWAP child')

        cancel_vwap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.vwap_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(cancel_vwap_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Fill')
        # endregion
