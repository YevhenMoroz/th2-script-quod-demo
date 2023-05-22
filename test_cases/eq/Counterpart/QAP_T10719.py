import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T10719(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_counterpart_1')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition: Set up needed configuration
        firm_counter_part = self.data_set.get_counterpart_id_java_api('counterpart_entering_firm')
        tree = ET.parse(self.local_path)
        element = ET.fromstring(f"<firmCounterpartID>{firm_counter_part['CounterpartID']}</firmCounterpartID>")
        quod = tree.getroot()
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS")
        time.sleep(80)
        # endregion

        # region step 1 : create CO
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': self.client,
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply[JavaApiFields.ClOrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verifying that CO order created (step 1)')
        # endregion

        # region step 2: Fully ManualExecute CO order:
        self.trade_entry.set_default(self.data_set, order_id)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        parties = {
            'NoParty': [
                self.data_set.get_counterpart_id_fix('counterpart_id_investment_firm_cl_counterpart'),
                self.data_set.get_counterpart_id_fix('counterpart_id_custodian_user'),
                self.data_set.get_counterpart_id_fix('counterpart_id_regulatory_body_venue_paris'),
                self.data_set.get_counterpart_id_fix('counterpart_id_market_maker_th2_route'),
                self.data_set.get_counterpart_id_fix('counterpart_java_api_user'),
                self.data_set.get_counterpart_id_fix('entering_firm')
            ]
        }
        list_of_ignored_fields = ['Account', 'ExecID',
                                  'GatingRuleCondName', 'OrderQtyData',
                                  'LastQty', 'GatingRuleName', 'OrderID',
                                  'TransactTime', 'Side', 'AvgPx',
                                  'QuodTradeQualifier', 'BookID',
                                  'SettlCurrency', 'SettlDate', 'Currency',
                                  'TimeInForce', 'PositionEffect',
                                  'TradeDate', 'HandlInst', 'LeavesQty',
                                  'CumQty', 'LastPx', 'OrdType',
                                  'tag5120', 'LastMkt', 'OrderCapacity',
                                  'QtyType', 'ExecBroker', 'Price',
                                  'VenueType', 'Instrument',
                                  'ExDestination', 'GrossTradeAmt']
        execution_report = FixMessageExecutionReportOMS(self.data_set).change_parameters(
            {"NoParty": parties,
             "ExecType": "F",
             "OrdStatus": "2",
             'ClOrdID': cl_ord_id
             })
        self.fix_verifier_dc.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS")
        time.sleep(80)
        os.remove("temp.xml")
