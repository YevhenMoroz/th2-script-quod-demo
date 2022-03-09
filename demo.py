import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_taker_rfq.QAP_568 import QAP_568
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run():
    # Generation id and time for test run
    pc_name = get_pc_name()  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing dataset
    data_set = FxDataSet()  # <--- provide your dataset (OmsDataSet(), FxDataSet(), AlgoDataSet(), RetDataSet())
    # initializing FE session
    session_id = set_session_id()
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("ESP_MM")  # <--- provide your component from XML (DMA, iceberg, etc)

    # endregion
    Stubs.frontend_is_open = True

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        QAP_568(report_id, session_id, configuration.data_set).execute()



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
