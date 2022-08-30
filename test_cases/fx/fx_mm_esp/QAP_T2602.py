from pathlib import Path
from time import sleep

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.data_sets.constants import DirectionEnum, Status

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd


class QAP_T2602(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_mm = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportFX()
        self.status_fill = Status.Fill
        self.account = data_set.get_account_by_name('account_mm_1')
        self.client = data_set.get_client_by_name('client_mm_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.new_order_single.set_default().change_parameters({'OrdType': '1'})

        self.new_order_single.remove_parameters(['Price', 'SettlDate'])
        response = self.fix_manager_mm.send_message_and_receive_response(self.new_order_single, self.test_id)

        for execution in response:
            if 'MO' not in execution.get_parameter('ExecID'):
                if 'EX' in execution.get_parameter('ExecID'):
                    execution.add_tag({'Account': self.account})
                else:
                    execution.add_tag({'Account': self.client})
                self.fix_verifier.check_fix_message(fix_message=execution, direction=DirectionEnum.FromQuod)
            sleep(5)
