import os
import re
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportTradeEntryRequestFX import \
    FixMessageExecutionReportTradeEntryRequestFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.OrderQuoteFX import OrderQuoteFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionRequestFX import QuoteRequestActionRequestFX
from test_framework.java_api_wrappers.fx.TradeEntryRequestFX import TradeEntryRequestFX
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T11057(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.verifier = Verifier(self.test_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.java_quote = OrderQuoteFX()
        self.action_request = QuoteRequestActionRequestFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportTradeEntryRequestFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_1w = self.data_set.get_settle_date_by_name("wk1")
        self.settle_type_1w = self.data_set.get_settle_type_by_name("wk1")
        self.settle_date_2w = self.data_set.get_settle_date_by_name("wk2")
        self.settle_type_2w = self.data_set.get_settle_type_by_name("wk2")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.trade_request = TradeEntryRequestFX()
        self.execution_report = FixMessageExecutionReportTradeEntryRequestFX()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.config_file = "client_qf_kharkiv_quod7_th2.xml"
        self.local_path = resource_filename("test_resources.be_configs.fx_be_configs", self.config_file)
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/{self.config_file}"
        self.temp_path = "C:/Users/amedents/PycharmProjects/th2-script-quod-demo/temp"
        self.qty = random_qty(9, len=9)
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }
        self.verifier = Verifier()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.trade_request.set_default_params()
        self.java_api_manager.send_message(self.trade_request)
        self.ssh_client.get_file("/Logs/quod314/QUOD.QSFE.log",
                                 self.temp_path)
        logs = open(self.temp_path, "r")
        self.result = "pass"
        for line in logs:
            self.key = re.findall(r"^.*ListingQuoting_pkg\.ListingQuoting_r.*$", line)
            if self.key:
                self.result = "failed"
                break
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check that \"ListingQuoting_pkg.ListingQuoting_r\" is not present in logs")
        self.verifier.compare_values("status", "pass", self.result)
        self.verifier.verify()
        logs.close()
        os.remove(self.temp_path)
        # endregion

