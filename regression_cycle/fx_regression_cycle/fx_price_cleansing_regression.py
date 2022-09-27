from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_price_cleansing.QAP_T2637 import QAP_T2637
from test_cases.fx.fx_price_cleansing.QAP_T5124 import QAP_T5124
from test_cases.fx.fx_price_cleansing.QAP_T5126 import QAP_T5126
from test_cases.fx.fx_price_cleansing.QAP_T5127 import QAP_T5127
from test_cases.fx.fx_price_cleansing.QAP_T5128 import QAP_T5128
from test_cases.fx.fx_price_cleansing.QAP_T5129 import QAP_T5129
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None, session=None):
    report_id = bca.create_event(f"FX_PRICE_CLEANSING" if version is None else f"FX_PRICE_CLEANSING | {version}", parent_id)
    session_id = session if session is not None else set_session_id(target_server_win="ashcherb")
    main_window_name = "Quod Financial - Quod site 314"
    configuration = ComponentConfiguration("Price_Cleansing")

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id, main_window_name)
        QAP_T2637(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T5124(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T5126(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T5127(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T5128(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T5129(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()


    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
