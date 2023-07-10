import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageMultilegOrderCancelReplaceOMS import \
    FixMessageMultilegOrderCancelReplaceOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderMultiLegOMS import FixMessageNewOrderMultiLegOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.MultiLegOrderModificationRequestOMS import \
    MultiLegOrderModificationRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderMultiLegOMS import NewOrderMultiLegOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10972(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.new_order_multi_leg = NewOrderMultiLegOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.rule_manager = RuleManager(Simulators.equity)
        self.execution_report_fix = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier_buy_side = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.fix_manager_buy = FixManager(self.fix_env.buy_side, self.test_id)
        self.multileg_modification_request = MultiLegOrderModificationRequestOMS(self.data_set)
        self.fix_multileg_modification_request = FixMessageMultilegOrderCancelReplaceOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        near_leg_price = '11.0'
        far_leg_price = '12.0'
        # region step 1: Create DMA multi_leg order:
        self.new_order_multi_leg.set_default_dma_limit()
        qty = self.new_order_multi_leg.get_parameters()[JavaApiFields.NewOrderMultiLegBlock.value][
            JavaApiFields.OrdQty.value]
        price = self.new_order_multi_leg.get_parameters()[JavaApiFields.NewOrderMultiLegBlock.value][
            JavaApiFields.OrdQty.value]
        instrument_multy_leg = self.data_set.get_instrument_id_by_name('instrument_12_multileg_paris')
        listing_multy_leg = self.data_set.get_listing_id_by_name('listing_12_ml_paris')
        instrument_leg_first = self.data_set.get_instrument_id_by_name('instrument_12_leg_1_of_multileg_paris')
        instrument_leg_second = self.data_set.get_instrument_id_by_name('instrument_12_leg_2_of_multileg_paris')
        self.new_order_multi_leg.update_fields_in_component(JavaApiFields.NewOrderMultiLegBlock.value, {
            JavaApiFields.PositionEffect.value: SubmitRequestConst.PositionEffect_R.value,
            JavaApiFields.ListingList.value: {
                JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_multy_leg}]},
            JavaApiFields.InstrID.value: instrument_multy_leg,
            JavaApiFields.LegOrderElements.value: {JavaApiFields.LegOrderBlock.value: [
                {JavaApiFields.LegNumber.value: "1", JavaApiFields.LegPrice.value: near_leg_price,
                 JavaApiFields.LegInstrID.value:
                     instrument_leg_first},
                {JavaApiFields.LegNumber.value: "2", JavaApiFields.LegPrice.value: far_leg_price,
                 JavaApiFields.LegInstrID.value:
                     instrument_leg_second}]}
        })
        self.java_api_manager.send_message_and_receive_response(self.new_order_multi_leg)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        fix_instrument_leg_near = self.data_set.get_fix_leg_instrument_by_name('instrument_multileg_paris_leg_1')
        fix_instrument_leg_far = self.data_set.get_fix_leg_instrument_by_name('instrument_multileg_paris_leg_2')
        list_ignored_fields = ['Account', 'OrderQtyData', 'OrdType',
                               'MaxPriceLevels', 'TransactTime',
                               'Parties', 'SettlCurrency', 'LegSecurityExchange',
                               'ExDestination', 'Instrument', 'LegRatioQty']
        fix_message_noml = FixMessageNewOrderMultiLegOMS(self.data_set).set_default()
        fix_message_noml.change_parameters({'ClOrdID': order_id,
                                            'LegOrdGrp': {'NoLegs':
                                                [{
                                                    'LegOrderQty': '*',
                                                    'LegPositionEffect': 'C',
                                                    'InstrumentLeg': fix_instrument_leg_near
                                                },
                                                    {
                                                        'LegOrderQty': '*',
                                                        'LegPositionEffect': 'O',
                                                        'InstrumentLeg': fix_instrument_leg_far
                                                    }
                                                ]}})
        fix_message_noml.remove_parameters(['PositionEffect'])
        self.fix_verifier_buy_side.check_fix_message_fix_standard(fix_message_noml, ignored_fields=list_ignored_fields)
        # endregion

        # region step 2: Send 35 = 8 (39=0) message
        zero_value = '0.0'
        self.execution_report_fix.change_parameters({
            "Account": self.venue_client_name,
            "HandlInst": "1",
            "Side": "1",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            "OrderCapacity": "A",
            "ClOrdID": order_id,
            "Price": price,
            "Currency": self.data_set.get_currency_by_name("currency_1"),
            "Instrument": self.data_set.get_fix_instrument_by_name("instrument_multileg_paris"),
            "ExecType": "0",
            "OrdStatus": "0",
            "OrderID": order_id,
            "ExecID": '1',
            "LastQty": zero_value,
            "TransactTime": datetime.utcnow().isoformat(),
            "AvgPx": zero_value,
            "LeavesQty": qty,
            "CumQty": zero_value,
            "LastPx": zero_value,
        })
        self.fix_manager_buy.send_message_fix_standard(self.execution_report_fix)
        time.sleep(2)
        exec_type = \
            self.db_manager.execute_query(
                f"SELECT exectype FROM ordreply WHERE transid='{order_id}' AND exectype='{OrderReplyConst.ExecType_OPN.value}'")[
                0][0]
        self.fix_manager_buy.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.ExecType_OPN.value},
                                            {JavaApiFields.ExecType.value: exec_type},
                                            f'Verify that order has OrdStatus = {OrderReplyConst.ExecType_OPN.value} (step 2)')
        # endregion

        # region step 3 : Amend MultiLeg order
        new_price = '2'
        self.multileg_modification_request.set_default_modify(order_id, price=2)
        self.multileg_modification_request.update_fields_in_component(JavaApiFields.MultiLegOrderModificationRequestBlock.value,
                                                                      {
                                                                          JavaApiFields.PositionEffect.value: SubmitRequestConst.PositionEffect_R.value
                                                                      })
        self.java_api_manager.send_message_and_receive_response(self.multileg_modification_request)
        list_ignored_fields.extend(['ClOrdID', 'OrderID'])
        self.fix_multileg_modification_request.set_default(fix_message_noml.get_parameters())
        self.fix_multileg_modification_request.change_parameters({'Price': new_price,
                                                                  'LegOrdGrp': {'NoLegs':
                                                                      [{
                                                                          'LegPositionEffect': 'C',
                                                                          'InstrumentLeg': fix_instrument_leg_near
                                                                      },
                                                                          {
                                                                              'LegPositionEffect': 'O',
                                                                              'InstrumentLeg': fix_instrument_leg_far
                                                                          }
                                                                      ]}
                                                                  })
        self.fix_multileg_modification_request.remove_parameters(['PositionEffect'])
        self.fix_verifier_buy_side.check_fix_message_fix_standard(self.fix_multileg_modification_request,
                                                                  ignored_fields=list_ignored_fields)
        # endregion

        # region step 4: Send 35 = 8 (39=0, 150 = 5) message
        ord_modify_id = \
            self.db_manager.execute_query(
                f"SELECT ordmodifyid FROM ordmodify WHERE ordid='{order_id}'")[0][0]
        self.execution_report_fix.change_parameters({
            "Account": self.venue_client_name,
            "ClOrdID": ord_modify_id,
            "Price": new_price,
            "ExecType": "5",
            "OrdStatus": "0",
            "Currency": self.data_set.get_currency_by_name("currency_1"),
            "Instrument": self.data_set.get_fix_instrument_by_name("instrument_multileg_paris"),
            "OrderID": order_id,
            'OrigClOrdID': order_id,
            "ExecID": '2',
            "TransactTime": datetime.utcnow().isoformat(),
        })
        self.fix_manager_buy.send_message_fix_standard(self.execution_report_fix)
        time.sleep(2)
        actually_price =  \
            self.db_manager.execute_query(
                f"SELECT price FROM ordreply WHERE transid='{order_id}' AND exectype='{OrderReplyConst.ExecType_REP.value}'")[
                0][0]
        self.java_api_manager.compare_values({JavaApiFields.Price.value: str(float(new_price))},
                                             {JavaApiFields.Price.value: str(float(actually_price))},
                                             'Verify that order modified (step 4)')
        # endregion
