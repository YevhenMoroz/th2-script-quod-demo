import time
from datetime import datetime
from pathlib import Path
from random import randint

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.forex.RestApiPriceCleansingCrossedVenueRatesMessages import \
    RestApiPriceCleansingCrossedVenueRatesMessages
from test_framework.rest_api_wrappers.forex.RestApiPriceCleansingUnbalancedRatesMessages import \
    RestApiPriceCleansingUnbalancedRatesMessages


class QAP_T9140(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fx_fh_connectivity = SessionAliasFX().fx_fh_connectivity
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_env = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_gtw = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_mm = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_marketdata_th2 = FixManager(self.fix_env.buy_side_md, self.test_id)
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_md_snapshot_doubler = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.md_reject = FixMessageMarketDataRequestRejectFX()
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.gbp_usd = self.data_set.get_symbol_by_name('symbol_2')
        self.hsbc = self.data_set.get_venue_by_name('venue_2')
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.instr_type_wa = self.data_set.get_fx_instr_type_wa('fx_spot')
        self.rest_message = RestApiPriceCleansingUnbalancedRatesMessages(data_set=self.data_set)
        self.rest_manager = RestApiManager(self.rest_env, self.test_id)
        self.rest_message_params = None
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type,
        }
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.gbp_usd,
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type,
        }]
        self.md_id_hsbc = f"{self.gbp_usd}:{self.instr_type_wa}:REG:{self.hsbc}"
        self.md_id_hsbc_a = f"{self.gbp_usd}:{self.instr_type_wa}:REG:{self.hsbc}" + "_" + str(randint(100, 9999))
        self.md_id_hsbc_b = f"{self.gbp_usd}:{self.instr_type_wa}:REG:{self.hsbc}" + "_" + str(randint(100, 9999))
        self.md_id_hsbc_c = f"{self.gbp_usd}:{self.instr_type_wa}:REG:{self.hsbc}" + "_" + str(randint(100, 9999))
        self.md_req_id = ''
        self.md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19500,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19650,
                "MDEntrySize": 5000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Region Rule creation
        self.rest_message.set_default_params().create_unbalanced_rates_rule().set_venue(self.hsbc).set_symbol(
            self.gbp_usd)
        self.rest_message.change_params({"enrichEmptySideOfBook": "true"})
        self.rest_message.change_params({"removeDetectedUpdate": "false"})
        response = self.rest_message_params = self.rest_manager.parse_create_response(
            self.rest_manager.send_multiple_request(self.rest_message))
        time.sleep(4)
        # endregion

        self.md_request.set_md_req_parameters_taker(). \
            change_parameters({'MDReqID': self.md_id_hsbc_a}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_request.set_md_uns_parameters_maker(). \
            change_parameters({'MDReqID': self.md_id_hsbc_a})
        self.fix_manager_marketdata_th2.send_message(self.md_request)
        self.fix_md.change_parameter("MDReqID", self.md_id_hsbc)
        self.fix_md.change_parameter("NoMDEntries", self.md_entries)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fx_fh_connectivity, 'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_hsbc}")
        time.sleep(8)

        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.silver).change_parameter(
            'NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.md_request, ["*", "*"])
        self.fix_md_snapshot.get_parameter("NoMDEntries").pop(3)
        # self.fix_md_snapshot.add_tag({'PriceCleansingReason': '5'})
        self.fix_verifier.check_fix_message(self.fix_md_snapshot, ignored_fields=["header", "trailer", "CachedUpdate"])
        # endregion
        # region Step 3
        # self.md_reject.set_md_reject_params(self.md_request, self.text)
        # self.fix_verifier.check_fix_message(fix_message=self.md_reject,
        #                                     direction=DirectionEnum.FromQuod,
        #                                     key_parameters=["MDReqID"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Deleting rule
        self.rest_message.clear_message_params().set_params(
            self.rest_message_params).delete_unbalanced_rates_rule()
        self.rest_manager.send_post_request(self.rest_message)
        self.fix_md.set_market_data()
        self.fix_md.change_parameter("MDReqID", self.md_id_hsbc)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_hsbc}")
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
        self.sleep(4)
