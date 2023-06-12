from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTakerDC import FixMessageNewOrderSingleTakerDC
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsAckFX import FixMessageRequestForPositionsAckFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from custom import basic_custom_actions as bca
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.java_api_wrappers.fx.FixPositionTransferInstructionFX import FixPositionTransferInstructionFX
from test_framework.positon_verifier_fx import PositionVerifier


class QAP_T10635(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.dc_connectivity = self.environment.get_list_fix_environment()[0].drop_copy
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_drop_copy_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.fix_manager = FixManager(self.pks_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.position_report = FixMessagePositionReportFX()
        self.pos_report_ack = FixMessageRequestForPositionsAckFX()
        self.position_verifier = PositionVerifier(self.test_id)
        self.position_transfer = FixPositionTransferInstructionFX()
        self.ah_order = FixMessageNewOrderSingleTakerDC()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.client_ext = self.data_set.get_client_by_name("client_int_1")
        self.account_ext = self.data_set.get_account_by_name("account_int_1")
        self.client_int = self.data_set.get_client_by_name("client_int_3")
        self.account_int = self.data_set.get_account_by_name("account_int_3")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.spot = self.data_set.get_security_type_by_name("fx_spot")
        self.instr_type_spo = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instrument = {
            "SecurityType": self.spot,
            "Symbol": self.eur_usd
        }
        self.position_verifier = PositionVerifier(self.test_id)
        self.base_qty = "-3000000"
        self.destination_qty = "3000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        # endregion

        # region Step 1
        self.position_transfer.set_default_params(self.account_ext, self.account_int)
        self.position_transfer.change_symbol(self.eur_usd)
        self.position_transfer.change_qty(self.destination_qty)
        self.java_api_manager.send_message(self.position_transfer)
        # endregion
        # region Step 2
        self.request_for_position.set_default()
        self.request_for_position.change_parameters({"Instrument": self.instrument, "Currency": self.currency,
                                                     "Account": self.client_ext})
        position_response: list = self.fix_manager.send_message_and_receive_response(self.request_for_position,
                                                                                     self.test_id)
        self.position_verifier.check_base_position(position_response, self.base_qty, text="Check base for source")
        self.pos_report_ack.set_params_from_reqeust(self.request_for_position)
        self.pos_report_ack.change_parameter("TotalNumPosReports", "1")
        self.pos_report_ack.change_parameter("PosReqResult", "0")
        self.fix_verifier.check_fix_message(self.pos_report_ack)

        self.position_report.set_params_from_reqeust(self.request_for_position, )
        self.position_report.change_parameter("LastPositEventType", "12")

        self.fix_verifier.check_fix_message(self.position_report, message_name="Check Source position")

        self.sleep(2)
        self.request_for_position.set_unsubscribe()
        self.ah_order.set_default_params()
        self.ah_order.change_parameters({"Account": self.client_int, "OrderQty": self.destination_qty})
        self.fix_drop_copy_verifier.check_fix_message(self.ah_order, key_parameters=["OrderQty", "Account"],
                                                      message_name="Check that AH created")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.cancel_request.set_params(self.account_ext)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        self.cancel_request.set_params(self.account_int)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
