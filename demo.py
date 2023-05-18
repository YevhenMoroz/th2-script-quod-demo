import logging
from datetime import datetime
from pathlib import Path



from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.PostTrade.QAP_T10867 import QAP_T10867
from test_cases.eq.PostTrade.QAP_T11138 import QAP_T11138
from test_cases.eq.PostTrade.QAP_T11139 import QAP_T11139
from test_cases.eq.PostTrade.QAP_T11140 import QAP_T11140
from test_cases.eq.PostTrade.QAP_T11257 import QAP_T11257
from test_cases.eq.PostTrade.QAP_T6995 import QAP_T6995
from test_cases.eq.PostTrade.QAP_T7112 import QAP_T7112
from test_cases.eq.PostTrade.QAP_T7217 import QAP_T7217

from test_cases.eq.PostTrade.QAP_T7462 import QAP_T7462
from test_cases.eq.PostTrade.QAP_T7463 import QAP_T7463
from test_cases.eq.PostTrade.QAP_T7550 import QAP_T7550
from test_cases.eq.PostTrade.QAP_T8731 import QAP_T8731
from test_cases.eq.PostTrade.QAP_T9126 import QAP_T9126
from test_cases.eq.PostTrade.QAP_T9201 import QAP_T9201

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageAllocationOMS import FixMessageAllocationOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.oms.es_messages.OrdReportOMS import OrdReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixAllocationInstructionOMS import FixAllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id
from protobuf_to_dict import protobuf_to_dict
logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    pc_name = "ymoroz"  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing FE session
    session_id = set_session_id("ymoroz2")
    base_main_window = BaseMainWindow(bca.create_event(Path(__file__).name[:-3], report_id), session_id)
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("DMA")  # <--- provide your component from XML (DMA, iceberg, etc)
    fe_env = configuration.environment.get_list_fe_environment()[0]
    fe_folder = fe_env.folder
    fe_user = fe_env.user_1
    fe_pass = fe_env.password_1
    java_api_manager = JavaApiManager("317_java_api_user2", report_id)
    nos = OrderSubmitOMS(configuration.data_set).set_default_dma_limit()
    nos2 = NewOrderReplyOMS(configuration.data_set).set_unsolicited_dma_limit()
    ord_rep = OrdReportOMS(configuration.data_set).set_default_open("175502612", "MO1230408201158316001")
    exec_rep = ExecutionReportOMS(configuration.data_set).set_default_trade("407194355")
    alloc_rec = FixAllocationInstructionOMS(configuration.data_set).set_default_preliminary("CO1230218111844196001")
    fix_manager = FixManager("fix-sell-317-standard-test", report_id)
    fix_manager42 = FixManager("fix-sell-317-standard42", report_id)
    fix_nos = FixMessageNewOrderSingleOMS(configuration.data_set).set_fix42_care_limit()
    # fix_nos2 = FixMessageNewOrderSingleOMS(configuration.data_set).set_default_dma_limit()
    # fix_nos.change_parameter("Account", "CLIENT_YMOROZ")
    # print(fix_nos.get_parameters())
    fix_alloc = FixMessageAllocationOMS()

    # print(fix_alloc.get_parameters())
    alloc = AllocationInstructionOMS(configuration.data_set)
    nol = NewOrderListOMS(configuration.data_set).set_default_order_list()
    # endregion

    try:
        # fix_alloc.set_fix42_preliminary(fix_nos,  "CLIENT_YMOROZ_SA1124sdf")
        # fix_manager42.send_message_and_receive_response_fix_standard(fix_alloc)

        # java_api_manager.send_message(exec_rep)
        QAP_T9126(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
