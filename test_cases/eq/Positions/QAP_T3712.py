import datetime
import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, PositionValidities, \
    SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.java_api_wrappers.pks_messages.RetailPositionConversionRequest import \
    RetailPositionConversionRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T3712(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pos_3_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.account = self.data_set.get_account_by_name('client_pos_3_acc_4')
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        self.qty = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.OrdQty.value]
        self.instr_id = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[
            JavaApiFields.InstrID.value]
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.order_modify = OrderModificationRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.retail_position_conversion_request = RetailPositionConversionRequest()
        self.request_for_position = RequestForPositions()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        self.db_manager.execute_query(
            f"UPDATE institution SET posflatteningtime='{(tm(datetime.datetime.utcnow().isoformat()) + bd(n=8)).date().strftime('%Y-%m-%dT%H:%M:%S')}' WHERE institutionname ='QUOD FINANCIAL 1'")
        self.db_manager.execute_query(
            f"DELETE FROM retailposit WHERE instrid = '{self.instrument_id}' AND accountid = '{self.account}'")
        self.ssh_client.send_command('qrestart QUOD.ORS QUOD.ESBUYTH2TEST QUOD.PKS')
        time.sleep(120)
        # endregion
        # region Step 1: Create DMA orders
        pos_validity_list = [PositionValidities.PosValidity_ITD.value, PositionValidities.PosValidity_TP1.value,
                             PositionValidities.PosValidity_TP2.value, PositionValidities.PosValidity_TP3.value,
                             PositionValidities.PosValidity_TP4.value, PositionValidities.PosValidity_TP5.value,
                             PositionValidities.PosValidity_TP6.value, PositionValidities.PosValidity_TP7.value]
        route_params = {JavaApiFields.RouteBlock.value: [
            {JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.AccountGroupID.value: self.client,
                                                      JavaApiFields.RouteList.value: route_params,
                                                      JavaApiFields.PreTradeAllocationBlock.value: {
                                                          JavaApiFields.PreTradeAllocationList.value: {
                                                              JavaApiFields.PreTradeAllocAccountBlock.value: [
                                                                  {JavaApiFields.AllocAccountID.value: self.account,
                                                                   JavaApiFields.AllocQty.value: self.qty}]}}})
        self._create_orders(pos_validity_list)
        # endregion

        # region step 2: Check that retails_positions created
        position_good_till_date_dict = {
            PositionValidities.PosValidity_ITD.value: (tm(datetime.datetime.utcnow().isoformat())).date().strftime(
                '%Y%m%d'),
            PositionValidities.PosValidity_TP1.value: (
                    tm(datetime.datetime.utcnow().isoformat()) + datetime.timedelta(days=1)).date().strftime('%Y%m%d'),
            PositionValidities.PosValidity_TP2.value: (
                    tm(datetime.datetime.utcnow().isoformat()) + datetime.timedelta(days=2)).strftime('%Y%m%d'),
            PositionValidities.PosValidity_TP3.value: (
                    tm(datetime.datetime.utcnow().isoformat()) + datetime.timedelta(days=3)).strftime('%Y%m%d'),
            PositionValidities.PosValidity_TP4.value: (
                    tm(datetime.datetime.utcnow().isoformat()) + datetime.timedelta(days=4)).strftime('%Y%m%d'),
            PositionValidities.PosValidity_TP5.value: (
                    tm(datetime.datetime.utcnow().isoformat()) + datetime.timedelta(days=5)).date().strftime('%Y%m%d'),
            PositionValidities.PosValidity_TP6.value: (
                    tm(datetime.datetime.utcnow().isoformat()) + datetime.timedelta(days=6)).date().strftime('%Y%m%d'),
            PositionValidities.PosValidity_TP7.value: (
                    tm(datetime.datetime.utcnow().isoformat()) + datetime.timedelta(days=7)).date().strftime('%Y%m%d')}
        position_records = self._extract_position(self.account)
        self._sort_records(position_records)
        counter = 0
        for key in position_good_till_date_dict.keys():
            self.ja_manager.compare_values({JavaApiFields.PosGoodTillDate.value: position_good_till_date_dict[key]},
                                           position_records[counter],
                                           f'Verify that position has properly {JavaApiFields.PosGoodTillDate.value}')
            counter = counter + 1
        # endregion

        # region step 3:
        pos_validity_list.clear()
        pos_validity_list.append(PositionValidities.PosValidity_DEL.value)
        self._create_orders(pos_validity_list)
        # endregion

        # region step 4:
        position_report = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                              [JavaApiFields.PosGoodTillDate.value,
                                                                               self.account,
                                                                               JavaApiFields.PositQty.value]).get_parameters() \
            [JavaApiFields.PositionReportBlock.value][JavaApiFields.RetailPositList.value][
            JavaApiFields.RetailPositBlock.value][0]
        self.ja_manager.compare_values({JavaApiFields.PosGoodTillDate.value: '19700101'},
                                       position_report,
                                       f'Verify that new records has properly {JavaApiFields.PosGoodTillDate.value} value (step 4)')
        # endregion

    def _extract_position(self, account):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              account)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        position_records = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][
            JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.RetailPositList.value][JavaApiFields.RetailPositBlock.value]
        position_records_by_instrument = []
        for position_record in position_records:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                position_records_by_instrument.append(position_record)
        return position_records_by_instrument

    # endregion

    def _sort_records(self, records):
        for i in range(len(records)):
            minimum = i
            for j in range(i + 1, len(records)):
                if datetime.datetime.strptime(records[j][JavaApiFields.PosGoodTillDate.value],
                                              '%Y%m%d') < datetime.datetime.strptime(
                    records[minimum][JavaApiFields.PosGoodTillDate.value], '%Y%m%d'):
                    minimum = j

            records[minimum], records[i] = records[i], records[minimum]

    def _create_orders(self, pos_validity_list: list):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            for pos_validity in pos_validity_list:
                self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                             {JavaApiFields.AccountGroupID.value: self.client,
                                                              JavaApiFields.ClOrdID.value: bca.client_orderid(9),
                                                              JavaApiFields.PosValidity.value: pos_validity,
                                                              })
                self.ja_manager.send_message_and_receive_response(self.order_submit, response_time=15000)
                order_reply = self.ja_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
                self.ja_manager.compare_values({JavaApiFields.PosValidity.value: pos_validity},
                                               order_reply,
                                               f'Verify that order has {JavaApiFields.PosValidity.value} equals {pos_validity}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.db_manager.execute_query(
            f"DELETE FROM retailposit WHERE instrid = '{self.instrument_id}' AND accountid = '{self.account}'")
        self.ssh_client.send_command('qrestart QUOD.ORS QUOD.ESBUYTH2TEST QUOD.PKS')
        time.sleep(120)
