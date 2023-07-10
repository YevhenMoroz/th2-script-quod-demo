import datetime
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10952(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_2')
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.new_ord_single = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1 part 1: Create CO orders with SettlType = T + 2
        settl_date_first = (datetime.datetime.now() + datetime.timedelta(days=1))
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        order_id_first = self._create_co_dma_order({
            JavaApiFields.SettlType.value: 'TP2',
            JavaApiFields.SettlDate.value: settl_date_first.strftime('%Y-%m-%dT%H:%M:%S')}, 'step 1 part 1',
            expected_settl_date=settl_date_first.strftime('%Y-%m-%d'))
        # endregion

        # region step 1 part 2: Create CO order with SettlDate = T + 4
        settl_date_second = (datetime.datetime.today() + datetime.timedelta(days=4))
        self.order_submit.remove_fields_from_component(JavaApiFields.NewOrderSingleBlock.value,
                                                       [JavaApiFields.SettlType.value])
        order_id_second = self._create_co_dma_order(
            {JavaApiFields.SettlDate.value: settl_date_second.strftime('%Y-%m-%dT%H:%M:%S'),
             JavaApiFields.ClOrdID.value: bca.client_orderid(9)}, 'step 1 part 2',
            expected_settl_date=settl_date_second.strftime('%Y-%m-%d'))
        # endregion

        # region step 2 part 1: Create DMA child order via Direct for first CO order
        self.order_submit.set_default_child_dma(order_id_first)
        settl_date_expected = (datetime.datetime.now() + datetime.timedelta(days=2))
        self._create_co_dma_order({JavaApiFields.SettlDate.value: settl_date_expected.strftime('%Y-%m-%dT%H:%M:%S')},
                                  step='step 2 part 1', is_dma=True,
                                  expected_settl_date=settl_date_expected.strftime('%Y-%m-%d'))
        # endregion

        # region step 2 part 2: Create DMA child order via Direct for second CO order
        self.order_submit.set_default_child_dma(order_id_second)
        self._create_co_dma_order({JavaApiFields.SettlDate.value: settl_date_expected}, step='step 2 part 2',
                                  is_dma=True, expected_settl_date=settl_date_expected.strftime('%Y-%m-%d'))
        # endregion

    def _create_co_dma_order(self, parameter_dict: dict, step, is_dma=False, expected_settl_date=None):
        if not is_dma:
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, parameter_dict)
            trans_status_expected = OrderReplyConst.TransStatus_OPN.value
        else:
            trans_status_expected = OrderReplyConst.TransStatus_SEN.value
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_rep = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = ord_rep[JavaApiFields.OrdID.value]
        expected_result = {JavaApiFields.TransStatus.value: trans_status_expected,
                           JavaApiFields.SettlDate.value: expected_settl_date + 'T12:00'}
        self.ja_manager.compare_values(expected_result, ord_rep, f'Verify that Order created ({step})')
        return order_id
