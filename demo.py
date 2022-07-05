import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_mm_esp.QAP_6932 import QAP_6932
from test_cases.fx.fx_mm_esp.QAP_6933 import QAP_6933
from test_cases.fx.fx_mm_rfq.QAP_3108 import QAP_3108
from test_cases.fx.fx_taker_esp.QAP_6289 import QAP_6289
from test_framework.configurations.component_configuration import ComponentConfiguration
# from test_framework.for_testing import Testing
from win_gui_modules.utils import set_session_id, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event(f'amedents ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing dataset

    # initializing FE session
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    session_id = set_session_id(target_server_win="amedents")
    # region environment and fe values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)
    start_time = datetime.now()
    print(f"Start time: {start_time}")
    # endregion
    Stubs.frontend_is_open = True
    main_window = "Quod Financial - Quod site 314"
    try:
        # QAP_MD(report_id, data_set=configuration.data_set).execute()

        QAP_3108(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_7160.execute(report_id)
        # QAP_5600(report_id).execute()

        # get_opened_fe(report_id, session_id, main_window)
        # QAP_1554.execute(report_id, session_id)
        # QAP_6933.execute(report_id, session_id, data_set=configuration.data_set)
        # QAP_6932(report_id, session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_6932(report_id, session_id).execute()

        # QAP_5600.execute(report_id, session_id, data_set=configuration.data_set)
        # QAP_2103(report_id, session_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_1536(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # rm = RuleManager()
        # rm.remove_rule_by_id(9)
        # rm.add_fx_md_to("fix-fh-309-kratos")
        # rm.print_active_rules()

        print(f"Duration is {datetime.now() - start_time}")

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
