import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.position_calculation_manager import PositionCalculationManager
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T8647(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.request_for_position = RequestForPositions()
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.account = self.data_set.get_venue_client_names_by_name('client_pos_1_venue_1')
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.quater_client_commission = 25

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:  Set Client Commission and Agent Fees via WebAdmin and set quartertodateclientcomm

        # part 1: update values for position
        self._precondition(self.quater_client_commission)
        # end_of_part

        # part 2: set Agent Fees and Client Commission
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        fee_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('paris')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=fee_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params({'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=fee_profile,
                                                                         client=self.client)
        self.rest_commission_sender.send_post_request()
        # end_of_part

        # endregion

        # region step 1 - 2: Create  and Trade DMA order with checking Position`s values
        result_for_washbook = self._extract_cum_values_for_washbook(self.wash_book)
        posit_qty = result_for_washbook[JavaApiFields.PositQty.value]
        gross_weighted_avg_px = result_for_washbook[JavaApiFields.GrossWeightedAvgPx.value]
        daily_agent_fees_before = result_for_washbook[JavaApiFields.DailyAgentFeeAmt.value]
        daily_client_commission_before = result_for_washbook[JavaApiFields.DailyClientCommission.value]
        daily_realized_gross_pl_before = result_for_washbook[JavaApiFields.DailyRealizedGrossPL.value]

        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {
            "AccountGroupID": self.client,
            'WashBookAccountID': self.wash_book,
            "ClOrdID": bca.client_orderid(9)})
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.account, self.mic, float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, self.account, self.mic, float(self.price), int(self.qty),0)
            self.ja_manager.send_message_and_receive_response(self.order_submit)
        except Exception as e:
            logging.error(e)
        finally:
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
        position_report = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                              [self.wash_book,
                                                                               JavaApiFields.PositQty.value]).get_parameters() \
            [JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        client_commission_and_fees = str(float(self.qty) * float(self.price) / 100 * 5)
        new_gross_weighted_avg_px = PositionCalculationManager.calculate_gross_weighted_avg_px_buy_side(
            gross_weighted_avg_px,
            position_report[JavaApiFields.PositQty.value],
            self.qty, self.price)

        daily_realized_gross_pl_after = PositionCalculationManager.calculate_today_gross_pl_buy_side(
            daily_realized_gross_pl_before, posit_qty,
            self.qty, self.price,
            new_gross_weighted_avg_px)
        daily_agent_fees_after = str(float(daily_agent_fees_before) + float(client_commission_and_fees))
        daily_client_commission_after = str(float(daily_client_commission_before) + float(client_commission_and_fees))
        self.ja_manager.compare_values({JavaApiFields.DailyRealizedGrossPL.value: daily_realized_gross_pl_after,
                                        JavaApiFields.DailyAgentFeeAmt.value: daily_agent_fees_after,
                                        JavaApiFields.DailyClientCommission.value: daily_client_commission_after,
                                        JavaApiFields.QuarterToDateClientComm.value: str(
                                            float(self.quater_client_commission))
                                        },
                                       position_report,
                                       f'Verifying that position of {self.wash_book} has properly values (step 2)')
        # endregion

    def _extract_cum_values_for_washbook(self, washbook):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              washbook)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()

    def _precondition(self, quater_client_commission):
        self.db_manager.update_query(
            f"UPDATE posit  SET quartertodateclientcomm = {quater_client_commission}  WHERE  instrid = '{self.instrument_id}' AND accountid = '{self.wash_book}';")
        self.ssh_client.send_command("qrestart QUOD.PKS")
        time.sleep(30)
