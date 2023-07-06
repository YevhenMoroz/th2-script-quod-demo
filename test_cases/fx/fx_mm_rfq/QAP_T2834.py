from pathlib import Path

from paramiko.client import SSHClient

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import check_value_in_db
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX
from test_framework.ssh_wrappers.ssh_client import SshClient


class QAP_T2834(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.rfq_reject = FixMessageQuoteRequestRejectFX(data_set=self.data_set)
        self.eur_rub = self.data_set.get_symbol_by_name('symbol_ndf_6')
        self.sec_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.spo_ndf_date = self.data_set.get_settle_date_by_name('spo_ndf')
        self.client_iridium = self.data_set.get_client_by_name("client_mm_3")
        self.instrument = {
            "Symbol": self.eur_rub,
            "SecurityType": self.sec_type_spot}
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.verifier = Verifier(self.test_id)
        self.result = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                            Account=self.client_iridium,
                                                                            Instrument=self.instrument,
                                                                            SettlDate=self.spo_ndf_date)
        cl_quote_request_id = str(self.quote_request.get_parameter("QuoteReqID"))
        self.fix_manager.send_message(self.quote_request)
        quote_request_id = str(
            check_value_in_db(cl_quote_request_id, key_parameter="clientquotereqid", table="quoterequest",
                              extracting_value="quoterequestid"))
        self.result = self.ssh_client.find_regex_pattern("/Logs/quod314/QUOD.QS_RFQ_FIX_TH2.log",
                                           rf"^.*QuoteRequestReject.*{quote_request_id}.*FreeNotes=\"no available depth on EUR/RUB SPO - manual intervention required\".*$")
        if self.result:
            self.result = "true"
            print("QuoteRequestReject is found")
        self.verifier.set_event_name("Check rule - Check QuoteRequest Reject")
        self.verifier.compare_values("Send QuoteRequest Reject", self.result, "true")
        # endregion
