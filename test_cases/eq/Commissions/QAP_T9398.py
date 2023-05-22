import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import  JavaApiFields, \
    SubmitRequestConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9398(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.mic = self.data_set.get_mic_by_name('mic_2')
        self.venue = self.data_set.get_venue_id('eurex')
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_2")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.qty = '100'
        self.price = '20'
        self.comm_profile = self.data_set.get_comm_profile_by_name('bas_qty')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up commission (precondition)
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client,
                                                                         comm_profile=self.comm_profile)
        self.rest_commission_sender.change_message_params({'venueID': self.venue})
        self.rest_commission_sender.send_post_request()

        # region step 1 (create Care order)
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'ListingList': {'ListingBlock': [{'ListingID': self.listing_id}]},
                                                      'InstrID': self.instrument_id, 'AccountGroupID': self.client,
                                                      'OrdQty': self.qty, "Price": self.price})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        ord_id = ord_notif[JavaApiFields.OrdID.value]
        cl_ord_id = ord_notif[JavaApiFields.ClOrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.Currency.value: self.cur}, ord_notif,
                                             "Check currency in the order")

        # region Step 2-3 (Split and execute order)
        self.order_submit2.set_default_child_dma(ord_id, cl_ord_id)
        self.order_submit2.update_fields_in_component("NewOrderSingleBlock", {'OrdQty': self.qty,
                                                                              "ClOrdID": bca.client_orderid(9),
                                                                              'ListingList': {'ListingBlock': [
                                                                                  {'ListingID': self.listing_id}]},
                                                                              'InstrID': self.instrument_id,
                                                                              'AccountGroupID': self.client,
                                                                              "Price": self.price})
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic,
                                                                                          int(self.price),
                                                                                          int(self.qty),
                                                                                          0)
            self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        comm_list = {
            JavaApiFields.CommissionBasis.value: 'BPS',
            JavaApiFields.CommissionAmount.value: '0.002',
            JavaApiFields.CommissionRate.value: '1.0',
            JavaApiFields.CommissionAmountType.value: 'BRK',
            JavaApiFields.CommissionCurrency.value: self.com_cur
        }

        ord_notif_dma = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        ord_id_dma = ord_notif_dma[JavaApiFields.OrdID.value]
        act_cl_comm = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             ExecutionReportConst.ExecType_TRD.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0]
        self.java_api_manager.compare_values(comm_list, act_cl_comm, 'Check client commission of the child execution')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
