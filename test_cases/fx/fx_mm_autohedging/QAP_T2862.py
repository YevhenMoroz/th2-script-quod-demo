from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportDropCopyFX import FixMessageExecutionReportDropCopyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.positon_verifier_fx import PositionVerifier


class QAP_T2862(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_pos_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.position_verifier = PositionVerifier(self.test_id)
        self.request_for_position_ext = FixMessageRequestForPositionsFX()
        self.request_for_position_int = FixMessageRequestForPositionsFX()
        self.position_report_ext = FixMessagePositionReportFX()
        self.position_report_int = FixMessagePositionReportFX()
        self.pos_report_none = FixMessageRequestForPositionsAckFX()
        self.trade_request = TradeEntryRequestFX()
        self.ah_exec_report = FixMessageExecutionReportDropCopyFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.client_ext = self.data_set.get_client_by_name("client_mm_6")
        self.account_ext = self.data_set.get_account_by_name("account_mm_6")
        self.client_int = self.data_set.get_client_by_name("client_int_3")
        self.account_int = self.data_set.get_account_by_name("account_int_3")
        self.currency = self.data_set.get_currency_by_name("currency_usd")
        self.usd_zar = self.data_set.get_symbol_by_name("symbol_20")
        self.sec_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instrument = {
            "SecurityType": self.sec_type_spo,
            "Symbol": self.usd_zar
        }
        self.first_trade_qty = "5000000"
        self.first_ah_qty = "4000000"
        self.second_trade_qty = "6000000"
        self.second_ah_qty = "6000000"
        self.external_pos_qty = "11000000"
        self.internal_pos_qty = "-1000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear position before start and check that they equal to 0
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)

        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        self.fix_manager.send_message_and_receive_response(self.request_for_position_ext, self.test_id)
        self.pos_report_none.set_params_from_reqeust(self.request_for_position_ext)

        self.fix_pos_verifier.check_fix_message(self.pos_report_none,
                                                message_name=f"Check position for {self.client_ext} before start")
        self.sleep(1)
        self.request_for_position_ext.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_ext)
        self.sleep(1)

        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        self.fix_manager.send_message_and_receive_response(self.request_for_position_int, self.test_id)
        self.pos_report_none.set_params_from_reqeust(self.request_for_position_int)
        self.fix_pos_verifier.check_fix_message(self.pos_report_none,
                                                message_name=f"Check position for {self.client_int} before start")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)

        # endregion

        # region Step 1
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client_ext,
                                                       "ExecQty": self.first_trade_qty})
        self.trade_request.change_instrument(self.usd_zar, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ord_id = self.trade_request.get_ah_ord_id(response)
        exec_id_ext = self.trade_request.get_exec_id(response)
        self.sleep(5)
        # endregion

        # region Step 2
        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        external_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_ext,
                                                                                   self.test_id)
        self.position_report_ext.set_params_from_reqeust(self.request_for_position_ext)
        self.position_report_ext.change_parameter("LastPositEventType", "5")
        self.position_report_ext.change_parameter("LastPositUpdateEventID", exec_id_ext)
        self.fix_pos_verifier.check_fix_message(self.position_report_ext,
                                                message_name=f"Check position for {self.client_ext} after order")
        self.position_verifier.check_base_position(external_report, self.first_trade_qty,
                                                   text=f"Check base for {self.client_ext}")
        self.sleep(1)
        self.request_for_position_ext.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_ext)
        self.sleep(1)
        #
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        internal_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_int,
                                                                                   self.test_id)
        self.position_report_int.set_params_from_reqeust(self.request_for_position_int)
        self.position_report_int.change_parameter("LastPositEventType", "5")
        self.fix_pos_verifier.check_fix_message(self.position_report_int,
                                                message_name=f"Check position for {self.client_int} after order")
        self.position_verifier.check_base_position(internal_report, self.internal_pos_qty,
                                                   text=f"Check base for {self.client_int}")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)
        # endregion

        # region Step 3
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameters(
            {"Account": self.client_int, "OrderQty": self.first_ah_qty,
             "Currency": self.currency, "ClOrdID": ord_id})
        self.ah_order.remove_parameter("Misc0")
        ah_order_params = ["ClOrdID"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_order, key_parameters=ah_order_params,
                                                      message_name="Check that we create AH order and send to market")

        self.ah_exec_report.set_params_from_trade_sor(self.trade_request)
        self.ah_exec_report.change_parameters(
            {"Currency": self.currency, "OrderID": ord_id, "Account": self.account_int, "CumQty": self.first_ah_qty,
             "OrderQty": self.first_ah_qty})
        ah_exec_params = ["OrderID", "OrdStatus", "ExecType"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report,
                                                      key_parameters=ah_exec_params,
                                                      message_name="Check AutoHedger ExecutionReport on DropCopy gtw")
        # endregion
        # region Step 4
        self.trade_request.set_default_params()
        self.trade_request.update_fields_in_component("TradeEntryRequestBlock",
                                                      {"ClientAccountGroupID": self.client_ext,
                                                       "ExecQty": self.second_trade_qty})
        self.trade_request.change_instrument(self.usd_zar, self.instr_type_spo)
        response: list = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        ord_id = self.trade_request.get_ah_ord_id(response)
        exec_id_ext = self.trade_request.get_exec_id(response)
        self.sleep(5)
        # endregion

        # region Step 5
        self.request_for_position_ext.set_default()
        self.request_for_position_ext.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_ext})
        external_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_ext,
                                                                                   self.test_id)
        self.position_report_ext.set_params_from_reqeust(self.request_for_position_ext)
        self.position_report_ext.change_parameter("LastPositEventType", "5")
        self.position_report_ext.change_parameter("LastPositUpdateEventID", exec_id_ext)
        self.fix_pos_verifier.check_fix_message(self.position_report_ext,
                                                message_name=f"Check position for {self.client_ext} after order")
        self.position_verifier.check_base_position(external_report, self.external_pos_qty,
                                                   text=f"Check base for {self.client_ext}")
        self.sleep(1)
        self.request_for_position_ext.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_ext)
        self.sleep(1)
        #
        self.request_for_position_int.set_default()
        self.request_for_position_int.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                         "Account": self.client_int})
        internal_report: list = self.fix_manager.send_message_and_receive_response(self.request_for_position_int,
                                                                                   self.test_id)
        self.position_report_int.set_params_from_reqeust(self.request_for_position_int)
        self.position_report_int.change_parameter("LastPositEventType", "5")
        self.fix_pos_verifier.check_fix_message(self.position_report_int,
                                                message_name=f"Check position for {self.client_int} after order")
        self.position_verifier.check_base_position(internal_report, self.internal_pos_qty,
                                                   text=f"Check base for {self.client_int}")
        self.request_for_position_int.set_unsubscribe()
        self.fix_manager.send_message(self.request_for_position_int)
        self.sleep(1)
        # endregion

        # region Step 6
        self.ah_order.set_default_sor_from_trade(self.trade_request)
        self.ah_order.change_parameters(
            {"Account": self.client_int, "OrderQty": self.second_trade_qty,
             "Currency": self.currency, "ClOrdID": ord_id})
        self.ah_order.remove_parameter("Misc0")
        ah_order_params = ["ClOrdID"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_order,
                                                      key_parameters=ah_order_params,
                                                      message_name="Check a new AH order sent to market")

        self.ah_exec_report.set_params_from_trade_sor(self.trade_request)
        self.ah_exec_report.change_parameters(
            {"Currency": self.currency, "OrderID": ord_id, "Account": self.account_int, "CumQty": self.second_trade_qty,
             "OrderQty": self.second_trade_qty})
        ah_exec_params = ["OrderID", "OrdStatus", "ExecType"]
        self.fix_drop_copy_verifier.check_fix_message(self.ah_exec_report,
                                                      key_parameters=ah_exec_params,
                                                      message_name="Check AutoHedger ExecutionReport on DropCopy gtw")
        # endregion
