import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7017(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.urg = 'LOW'
        self.params1 = {
            "Account": self.data_set.get_client_by_name("client_co_1"),
            "HandlInst": "3",
            "Side": "1",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': data_set.get_account_by_name("client_co_1_acc_1"),
                                          'AllocQty': "100"}]},
            "Instrument": self.data_set.get_fix_instrument_by_name("instrument_1"),
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": "20",
            "Currency": data_set.get_currency_by_name("currency_1"),
            "TargetStrategy": "1021",
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LOW'
                }
            ]}
        }
        self.params2 = {
            "Account": self.data_set.get_client_by_name("client_co_1"),
            "HandlInst": "3",
            "Side": "2",
            'OrderQtyData': {'OrderQty': "100"},
            "TimeInForce": "0",
            "OrdType": "2",
            'ListSeqNo': "2",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.data_set.get_account_by_name("client_co_1_acc_1"),
                                          'AllocQty': "100"}]},
            "Instrument": self.data_set.get_fix_instrument_by_name("instrument_1"),
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            "TransactTime": datetime.utcnow().isoformat(),
            "Price": "20",
            "Currency": self.data_set.get_currency_by_name("currency_1"),
            "TargetStrategy": "1022",  # 2021 = TWAP_ASIA
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LOW'
                }
            ]}
        }
        self.fix_message.change_parameter('ListOrdGrp', {'NoOrders': [self.params1, self.params2]})
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        # endregion

        # region check exec report
        execution_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.fix_message)
        execution_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.fix_message, 1)
        execution_report1.change_parameters(
            {'TargetStrategy': '1021'})
        execution_report2.change_parameters(
            {'TargetStrategy': '1022'})
        list_of_ignored_fields = ['StrategyParametersGrp', 'trailer', 'header','GatingRuleName', 'GatingRuleCondName']
        self.fix_verifier.check_fix_message(execution_report1,
                                            ignored_fields=list_of_ignored_fields)
        self.fix_verifier.check_fix_message(execution_report2,
                                            ignored_fields=list_of_ignored_fields)
        # endregion
