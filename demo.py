import logging
import time
from getpass import getuser as get_pc_name

from MyFiles.SendMD_Simple import SendMD_Simple
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_price_cleansing.QAP_3452 import QAP_3452
from test_cases.fx.fx_price_cleansing.QAP_7939 import QAP_7939
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ') #+ datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing dataset

    # initializing FE session
    session_id = set_session_id(target_server_win="ashcherb")
    window_name = "Quod Financial - Quod site 314"
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = time.time()
    print(f"Test start")
    data_set = FxDataSet()
    # endregion
    Stubs.frontend_is_open = True
    # rule_manager = rule_management.RuleManager()
    # rule_manager.print_active_rules()

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id, window_name)

        # QAP_2098(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_2343(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_4149(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_3142(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_3761(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_3147.execute(report_id, session_id)
        # QAP_3146.execute(report_id, session_id)
        # QAP_2159.execute(report_id, session_id)
        # QAP_5551.execute(report_id, session_id)
        # QAP_2491.execute(report_id, session_id)
        # QAP_3734.execute(report_id, session_id)
        # QAP_3661.execute(report_id, session_id)
        # QAP_3140.execute(report_id)
        # QAP_3805.execute(report_id)
        # QAP_2382.execute(report_id)
        # QAP_6691(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6697(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7073(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_3452(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6931(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_6933(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_7279(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3452(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7939(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # test(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_5369.execute(report_id, session_id, data_set)
        # QAP_5589.execute(report_id, session_id)
        # QAP_5591.execute(report_id, session_id)
        # QAP_5537.execute(report_id, session_id, data_set)
        # QAP_3141.execute(report_id)
        # QAP_3140.execute(report_id)
        # MyTest(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # send_rfq.execute(report_id)
        # SendMD_Simple(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # SendMD_empty(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # send_md_crossed(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # SendMD_Settle_Date(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # Send_MD_FWD(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # send_md_to_update_prices(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # send_md_defferent_venues(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_7129(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7081(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7160(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7167(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7279(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6145(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6148.execute(report_id, session_id)
        # QAP_6149(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6153(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6353(report_id=report_id, session_id=session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6151.execute(report_id)
        # SendMD_QAP_6337(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # SendMD_QAP_6353(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # SendMD_QAP_6353(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # rule_management.RuleManager.print_active_rules()
        # QAP_4509.execute(report_id)
        # QAP_4510.execute(report_id)
        # QAP_2966.execute(report_id)
        # QAP_2646.execute(report_id, session_id)
        # QAP_2296.execute(report_id, session_id)
        # stop_fxfh()
        # QAP_3414.execute(report_id)
        # QAP_3415.execute(report_id)
        # QAP_3418.execute(report_id)
        # start_fxfh()
        # prepare_position()
        # rm = RuleManager()
        # rm.print_active_rules()

        # Testing(report_id, session_id, configuration.data_set).execute()

        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # Send_RFQ(report_id, data_set=configuration.data_set).execute()


        end = time.time()
        print(f"Test duration is {end - start_time} seconds")

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
