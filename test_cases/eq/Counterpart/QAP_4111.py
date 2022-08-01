import logging
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_4111(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.price = self.fix_message.get_parameter("Price")
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message.change_parameters({"Account": self.client})
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region send fix message
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region check order is created
        parties = {
            'NoPartyIDs': [
                {'PartyRole': "67",
                 'PartyID': "InvestmentFirm - ClCounterpart",
                 'PartyIDSource': "C"},
                {'PartyRole': "34",
                 'PartyID': "RegulatoryBody - Venue(Paris)",
                 'PartyIDSource': "C"},
                {'PartyRole': "36",
                 'PartyID': "*",
                 'PartyRoleQualifier': "1011",
                 'PartyIDSource': "D"},
                {'PartyRole': "66",
                 'PartyID': "MarketMaker - TH2Route",
                 'PartyIDSource': "C"}
            ]
        }
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {'Parties': parties})
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        # endregion
        # region manual execution
        self.order_book.manual_execution(price=self.price, execution_firm=OrderBookColumns.exec_firm_value.value,
                                         contra_firm=OrderBookColumns.contra_firm_value.value,
                                         filter_dict={OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        parties = {
            'NoPartyIDs': [
                {'PartyRole': "67",
                 'PartyID': "InvestmentFirm - ClCounterpart",
                 'PartyIDSource': "C"},
                {'PartyRole': "34",
                 'PartyID': "RegulatoryBody - Venue(Paris)",
                 'PartyIDSource': "C"},
                {'PartyRole': "36",
                 'PartyID': "*",
                 'PartyIDSource': "D"},
                {'PartyRole': "66",
                 'PartyID': "MarketMaker - TH2Route",
                 'PartyIDSource': "C"},
                {'PartyRole': "17",
                 'PartyID': 'ContraFirm',
                 'PartyIDSource': "C"},
                {'PartyRole': "1",
                 'PartyID': "ExecutingFirm",
                 'PartyIDSource': "C"}
            ]
        }
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": parties, 'VenueType': "*", 'LastMkt': "*", "MiscFeesGrp": "*", "CommissionData":{'Commission':"*", 'CommType':"*"}})
        exec_report2.remove_parameters(["SecondaryExecID",  "SecondaryOrderID","SettlCurrency", "LastExecutionPolicy"])
        self.fix_verifier.check_fix_message_fix_standard(exec_report2)
        exec_firm = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                           [OrderBookColumns.exec_firm.value], [1],
                                                           {OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        self.order_book.compare_values({"Firm": OrderBookColumns.exec_firm_value.value},
                                       exec_firm[0],
                                       "Check  Exec Firm value")
        contra_firm = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                        [OrderBookColumns.contra_firm.value], [1],
                                                        {OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
        self.order_book.compare_values({'Firm': OrderBookColumns.contra_firm_value.value},
                                        contra_firm[0],
                                       "Check Contra Firm value")

        # endregion
