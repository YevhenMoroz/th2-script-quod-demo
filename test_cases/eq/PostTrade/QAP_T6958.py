import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T6958(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '100'
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.ja_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (precondition)
        self.nos.set_default_care_limit()
        expire_date = (datetime.now().strftime("%Y%m%d"))
        self.nos.update_fields_in_component("NewOrderSingleBlock", {"TimeInForce": "GTD", "ExpireDate": expire_date})
        self.ja_manager.send_message_and_receive_response(self.nos)
        order_id = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value) \
            .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        # endregion

        # region partially filled CO order
        cum_qty = str(int(self.qty) / 2)
        self.trade_entry.set_default_trade(order_id, exec_qty=cum_qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        exec_rep = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.ja_manager.compare_values({JavaApiFields.CumQty.value: cum_qty}, exec_rep, "Check DayCumQty")
        # endregion

        # region call end of day procedures
        self.db_manager.execute_query('BEGIN;SELECT eod_expireOrders();COMMIT;', False)
        # endregion
        # region check order after perform of procedure
        ord_status = self.db_manager.execute_query(f"SELECT ordstatus FROM ordr WHERE ordid='{order_id}'")[0][0]
        self.ja_manager.compare_values({"ordstatus": "EXP"}, {"ordstatus": ord_status}, "Check order status")
        # endregion
