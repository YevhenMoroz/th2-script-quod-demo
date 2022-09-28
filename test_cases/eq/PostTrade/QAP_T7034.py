import logging
import time
from pathlib import Path

from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7034(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client_by_name('client_com_1')
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit('instrument_3')
        self.fix_message.change_parameters(
            {'Account': self.client, "ExDestination": self.data_set.get_mic_by_name("mic_2"), "Currency": self.cur})
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.exec_destination = self.data_set.get_mic_by_name('mic_2')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_fees_message().change_message_params(
            {'commExecScope': self.data_set.get_fee_exec_scope_by_name("on_calculated"),
             "venueID": self.data_set.get_venue_by_name("venue_2"), "execCommissionProfileID": "1",
             "orderCommissionProfileID": "1"}).send_post_request()
        order_id = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty),
                                                                                            delay=0)
            # endregion
            # region create order
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameter("OrderID")
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            time.sleep(10)
            self.rule_manager.remove_rule(trade_rule)
            self.rule_manager.remove_rule(nos_rule)
        #  endregion
        # region check execution
        exec_report_1 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        exec_report_1.change_parameters(
            {'ReplyReceivedTime': "*", "Currency": self.cur,
             "LastMkt": self.exec_destination, "Text": "*", "OrderID": order_id})
        exec_report_1.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(exec_report_1)
        #  endregion
        # region check calculated
        no_party = {
            'NoParty': [
                {'PartyRole': "66",
                 'PartyID': "AccPR",
                 'PartyIDSource': "C"},
                {'PartyRole': "36",
                 'PartyID': "gtwquod4",
                 'PartyIDSource': "D"}
            ]
        }
        no_misc = {
            'NoMiscFees': {'MiscFeeAmt': '*',
                           'MiscFeeCurr': self.cur,
                           'MiscFeeType': "*"
                           }
        }
        exec_report_2 = FixMessageExecutionReportOMS(self.data_set).set_default_calculated(self.fix_message)
        exec_report_2.change_parameters(
            {"NoMiscFees": no_misc, "NoParty": no_party, 'QuodTradeQualifier': "*", "BookID": "*", "Currency": self.cur,
             "OrderID": order_id, "ExecBroker": "*",  "SecondaryOrderID": "*",
             "tag5120": "*", "CommissionData": "*"})
        exec_report_2.remove_parameters(['Parties', "TradeReportingIndicator"])
        self.fix_verifier_dc.check_fix_message_fix_standard(exec_report_2)
        #  endregion
