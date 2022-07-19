import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from stubs import Stubs
# from test_cases.fx.fx_taker_esp.QAP_6289 import QAP_6289
from test_cases.fx.fx_mm_rfq.QAP_2345 import QAP_2345
from test_cases.fx.fx_mm_rfq.QAP_2353 import QAP_2353
from test_cases.fx.fx_mm_rfq.QAP_3106 import QAP_3106
from test_cases.fx.fx_mm_rfq.QAP_3107 import QAP_3107
from test_cases.fx.fx_mm_rfq.QAP_3108 import QAP_3108
from test_cases.fx.fx_mm_rfq.QAP_3109 import QAP_3109
from test_cases.fx.fx_mm_rfq.QAP_3110 import QAP_3110
from test_cases.fx.fx_mm_rfq.QAP_3111 import QAP_3111
from test_cases.fx.fx_mm_rfq.QAP_3112 import QAP_3112
from test_cases.fx.fx_mm_rfq.QAP_3113 import QAP_3113
from test_cases.fx.fx_mm_rfq.QAP_7997 import QAP_7997
from test_cases.fx.fx_mm_rfq.interpolation.QAP_3851 import QAP_3851
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_3763 import QAP_3763
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_3937 import QAP_3937
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_3938 import QAP_3938
from test_cases.fx.fx_mm_rfq.rejection.QAP_3735 import QAP_3735
from test_cases.fx.fx_mm_rfq.rejection.QAP_3764 import QAP_3764
from test_framework.configurations.component_configuration import ComponentConfiguration
# from test_framework.for_testing import Testing
from win_gui_modules.utils import set_session_id, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


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
        # get_opened_fe(report_id, session_id, main_window)
        QAP_3113(report_id, session_id,
                 configuration.data_set,
                 configuration.environment).execute()
        # old versions:
        # QAP_MD(report_id, data_set=configuration.data_set).execute()
        # QAP_7160.execute(report_id)
        # QAP_1554.execute(report_id, session_id)
        # QAP_6933.execute(report_id, session_id, data_set=configuration.data_set)
        # QAP_6932(report_id, session_id).execute()
        # QAP_1536(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # rm = RuleManager()
        # rm.remove_rule_by_id(9)
        # rm.add_fx_md_to("fix-fh-309-kratos")
        # rm.print_active_rules()
        # endregion
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
