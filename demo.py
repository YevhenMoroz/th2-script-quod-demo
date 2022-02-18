import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Care.QAP_1016 import QAP_1016
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.oms_data_set.oms_data_set import OmsDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.algo_data_set.algo_data_set import AlgoDataSet
from test_framework.data_sets.ret_data_set.ret_data_set import RetDataSet
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    pc_name = get_pc_name() # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing dataset
    data_set = OmsDataSet() # <--- provide your dataset (OmsDataSet(), FxDataSet(), AlgoDataSet(), RetDataSet())
    # initializing FE session
    session_id = set_session_id(pc_name)
    base_main_window = BaseMainWindow(bca.create_event(Path(__file__).name[:-3], report_id), session_id)
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("YOUR_COMPONENT") #  <--- provide your component from XML (DMA, iceberg, etc)
    fe_env = configuration.environment.get_list_fe_environment()[0]
    fe_folder = fe_env.folder
    fe_user = fe_env.user
    fe_pass = fe_env.password
    # endregion

    try:
        base_main_window.open_fe(report_id=report_id, folder=fe_folder, user=fe_user, password=fe_pass)
        QAP_1016(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment)\
            .execute()
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