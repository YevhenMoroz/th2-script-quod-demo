import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.oms.oms_order_book_archive import OMSOrderBookArchive

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7541(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side
        self.bs_connectivity = self.environment.get_list_fix_environment()[0].buy_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.ord_book_archive = OMSOrderBookArchive(self.test_id, self.session_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        client = self.fix_message.get_parameter('Account')
        from_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S %p')
        price = self.fix_message.get_parameter('Price')
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(price))
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        until_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S %p')
        # endregion
        # region Order Book Archive action
        total = self.ord_book_archive.import_order_from_db(from_time, until_time, client, get_total_orders=True)
        self.ord_book_archive.compare_values({"Total orders": "0"}, total, "compare total",
                                             VerificationMethod.NOT_EQUALS)
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
