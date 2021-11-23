import logging
import os
import time

from custom import basic_custom_actions as bca, basic_custom_actions
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from datetime import datetime, timedelta
from quod_qa.wrapper_test.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from quod_qa.wrapper_test.oms.FixMessageOrderCancelReplaceRequestOMS import FixMessageOrderCancelReplaceRequestOMS
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP2008(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_2008(self):
        rule_manager = RuleManager()
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        # region Declarations
        global fix_report
        client = "CLIENT1"
        price = '20'
        fix_message = FixMessageNewOrderSingleOMS()
        fix_message.set_default_dma_limit(Instrument.FR0004186856)
        fix_message.change_parameters({'Account': client, 'TimeInForce': '6',
                                       'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2),
                                                                       "%Y%m%d")})
        fix_message.add_ClordId(os.path.basename(__file__)[:-3])

        # endregion

        # region Create order via FIX
        try:
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                             'XPAR_' + client, 'XPAR',
                                                                                             float(price))
            fix_manager.send_message_and_receive_response_fix_standard(fix_message)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
        # endregion

        # region Check New Order Single
        cl_ord_id = fix_message.get_parameter('ClOrdID')
        execution_status = FixMessageExecutionReportOMS().set_default_new()
        execution_status.change_parameters({'ClOrdID': cl_ord_id, 'ReplyReceivedTime': '*', 'SecondaryOrderID': '*',
                                            'LastMkt': '*', 'Text': '*', 'ExpireDate': '*', 'TimeInForce': '6'})
        fix_verifier.check_fix_message_fix_standard(execution_status)
        # endregion

        # region Amend order via FIX
        fix_message_modify = FixMessageOrderCancelReplaceRequestOMS(
            {"Account": "CLIENT1",
             "Side": "1",
             'OrderQtyData': {'OrderQty': '300'},
             'Price': '20',
             "OrdType": "2",
             "HandlInst": "2",
             "ClOrdID": cl_ord_id,
             "OrigClOrdID": cl_ord_id,
             "Instrument": Instrument.FR0010436584.value,
             "TransactTime": datetime.utcnow().isoformat()
             })
        try:
            trade_rule = rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity, 'XPAR_' + client,
                                                                                'XPAR', True)
            fix_manager.send_message_and_receive_response_fix_standard(fix_message_modify)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(trade_rule)
        execution_status_modify = FixMessageExecutionReportOMS()
        execution_status_modify.set_default_replaced()
        execution_status_modify.change_parameters(
            {'ClOrdID': cl_ord_id, 'ReplyReceivedTime': '*', 'SecondaryOrderID': '*',
             'LastMkt': '*', 'Text': '*', 'ExpireDate': '*', 'TimeInForce': '6', 'OrderQtyData': {'OrderQty': '300'},
             'OrigClOrdID': '*'})
        fix_verifier.check_fix_message_fix_standard(execution_status_modify, ['ClOrdID', 'OrdStatus', 'ExecType'])
        # endregion
        # cancel_request
        fix_message_cancel = FixMessageOrderCancelRequest()
        fix_message_cancel.change_parameters(
            {"Account": "CLIENT1",
             "Side": "1",
             "ClOrdID": cl_ord_id,
             "OrigClOrdID": cl_ord_id,
             "Instrument": Instrument.FR0010436584.value,
             "TransactTime": datetime.utcnow().isoformat()
             })
        try:
            cancel_rule = rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity, 'XPAR_' + client,
                                                                          'XPAR', True)
            fix_manager.send_message_and_receive_response_fix_standard(fix_message_cancel)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(3)
            rule_manager.remove_rule(cancel_rule)
        # endregion
        # region checkCancel
        execution_status_cancel = FixMessageExecutionReportOMS()
        execution_status_cancel.set_default_cancel()
        execution_status_cancel.change_parameters(
            {'ClOrdID': cl_ord_id, 'ReplyReceivedTime': '*', 'SecondaryOrderID': '*',
             'LastMkt': '*', 'Text': '*', 'ExpireDate': '*', 'TimeInForce': '6', 'OrderQtyData': {'OrderQty': '300'},
             'OrigClOrdID': '*', 'CxlQty': '300'})
        fix_verifier.check_fix_message_fix_standard(execution_status_cancel, ['ClOrdID', 'OrdStatus', 'ExecType'])
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_2008()
