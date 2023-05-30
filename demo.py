import logging
from getpass import getuser as get_pc_name
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Gateway.QAP_T10497 import QAP_T10497
from test_cases.eq.Gateway.QAP_T7015 import QAP_T7015
from test_cases.eq.Gateway.QAP_T7106 import QAP_T7106
from test_cases.eq.Gateway.QAP_T7139 import QAP_T7139
from test_cases.eq.Gateway.QAP_T7167 import QAP_T7167
from test_cases.eq.Gateway.QAP_T7173 import QAP_T7173
from test_cases.eq.Gateway.QAP_T7499 import QAP_T7499
from test_cases.eq.Gateway.QAP_T7500 import QAP_T7500
from test_cases.eq.Gateway.QAP_T7501 import QAP_T7501
from test_cases.eq.Gateway.QAP_T7503 import QAP_T7503
from test_cases.eq.Gateway.QAP_T7504 import QAP_T7504
from test_cases.eq.Gateway.QAP_T7507 import QAP_T7507
from test_cases.eq.Gateway.QAP_T7514 import QAP_T7514
from test_cases.eq.Gateway.QAP_T8705 import QAP_T8705
from test_cases.eq.Gateway.QAP_T8741 import QAP_T8741
from test_cases.eq.Gateway.QAP_T9070 import QAP_T9070
from test_cases.eq.GatingRules.QAP_T10668 import QAP_T10668
from test_cases.eq.GatingRules.QAP_T8825 import QAP_T8825
from test_cases.eq.GatingRules.QAP_T8827 import QAP_T8827
from test_cases.eq.Positions.QAP_T6893 import QAP_T6893
from test_cases.eq.PostTrade.QAP_T10397 import QAP_T10397
from test_cases.eq.PostTrade.QAP_T6900 import QAP_T6900
from test_cases.eq.PostTrade.QAP_T6928 import QAP_T6928
from test_cases.eq.PostTrade.QAP_T6948 import QAP_T6948
from test_cases.eq.PostTrade.QAP_T6950 import QAP_T6950
from test_cases.eq.PostTrade.QAP_T6958 import QAP_T6958
from test_cases.eq.PostTrade.QAP_T6965 import QAP_T6965
from test_cases.eq.PostTrade.QAP_T6972 import QAP_T6972
from test_cases.eq.PostTrade.QAP_T7080 import QAP_T7080
from test_cases.eq.PostTrade.QAP_T7188 import QAP_T7188
from test_cases.eq.PostTrade.QAP_T7230 import QAP_T7230
from test_cases.eq.PostTrade.QAP_T7359 import QAP_T7359
from test_cases.eq.PostTrade.QAP_T7360 import QAP_T7360
from test_cases.eq.PostTrade.QAP_T7462 import QAP_T7462
from test_cases.eq.PostTrade.QAP_T7464 import QAP_T7464
from test_cases.eq.PostTrade.QAP_T7465 import QAP_T7465
from test_cases.eq.PostTrade.QAP_T7468 import QAP_T7468
from test_cases.eq.PostTrade.QAP_T7476 import QAP_T7476
from test_cases.eq.PostTrade.QAP_T7477 import QAP_T7477
from test_cases.eq.PostTrade.QAP_T7481 import QAP_T7481
from test_cases.eq.PostTrade.QAP_T7505 import QAP_T7505
from test_cases.eq.PostTrade.QAP_T7510 import QAP_T7510
from test_cases.eq.PostTrade.QAP_T7517 import QAP_T7517
from test_cases.eq.PostTrade.QAP_T7530 import QAP_T7530
from test_cases.eq.PostTrade.QAP_T7531 import QAP_T7531
from test_cases.eq.PostTrade.QAP_T7532 import QAP_T7532
from test_cases.eq.PostTrade.QAP_T7535 import QAP_T7535
from test_cases.eq.PostTrade.QAP_T7538 import QAP_T7538
from test_cases.eq.PostTrade.QAP_T7547 import QAP_T7547
from test_cases.eq.PostTrade.QAP_T7548 import QAP_T7548
from test_cases.eq.PostTrade.QAP_T7551 import QAP_T7551
from test_cases.eq.PostTrade.QAP_T7552 import QAP_T7552
from test_cases.eq.PostTrade.QAP_T8089 import QAP_T8089
from test_cases.eq.PostTrade.QAP_T8118 import QAP_T8118
from test_cases.eq.PostTrade.QAP_T8339 import QAP_T8339
from test_cases.eq.PostTrade.QAP_T9155 import QAP_T9155
from test_cases.eq.PostTrade.QAP_T9175 import QAP_T9175
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    pc_name = 'mantonov'  # getting PC name
    report_id = bca.create_event(f'[{pc_name}] ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # initializing FE session
    session_id = set_session_id(pc_name)
    base_main_window = BaseMainWindow(bca.create_event(Path(__file__).name[:-3], report_id), session_id)
    # region creation FE environment and initialize fe_ values
    configuration = ComponentConfiguration("YOUR_COMPONENT")  # <--- provide your component from XML (DMA, iceberg, etc)
    fe_env = configuration.environment.get_list_fe_environment()[0]
    fe_folder = fe_env.folder
    fe_user = fe_env.user_1
    fe_pass = fe_env.password_1
    # endregion

    try:
        # base_main_window.open_fe(report_id=report_id, fe_env=fe_env, user_num=1)
        QAP_T8827(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                 environment=configuration.environment) \
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
