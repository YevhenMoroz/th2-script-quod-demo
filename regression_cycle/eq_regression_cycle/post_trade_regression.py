import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.Care.QAP_T7381 import QAP_T7381
from test_cases.eq.PostTrade.QAP_T6900 import QAP_T6900
from test_cases.eq.PostTrade.QAP_T6928 import QAP_T6928
from test_cases.eq.PostTrade.QAP_T6950 import QAP_T6950
from test_cases.eq.PostTrade.QAP_T6958 import QAP_T6958
from test_cases.eq.PostTrade.QAP_T6970 import QAP_T6970
from test_cases.eq.PostTrade.QAP_T6972 import QAP_T6972
from test_cases.eq.PostTrade.QAP_T7015 import QAP_T7015
from test_cases.eq.PostTrade.QAP_T7016 import QAP_T7016
from test_cases.eq.PostTrade.QAP_T7034 import QAP_T7034
from test_cases.eq.PostTrade.QAP_T7062 import QAP_T7062
from test_cases.eq.PostTrade.QAP_T7080 import QAP_T7080
from test_cases.eq.PostTrade.QAP_T7082 import QAP_T7082
from test_cases.eq.PostTrade.QAP_T7091 import QAP_T7091
from test_cases.eq.PostTrade.QAP_T7106 import QAP_T7106
from test_cases.eq.PostTrade.QAP_T7110 import QAP_T7110
from test_cases.eq.PostTrade.QAP_T7129 import QAP_T7129
from test_cases.eq.PostTrade.QAP_T7131 import QAP_T7131
from test_cases.eq.PostTrade.QAP_T7141 import QAP_T7141
# from test_cases.eq.PostTrade.QAP_T7160 import QAP_T7160
from test_cases.eq.PostTrade.QAP_T7174 import QAP_T7174
from test_cases.eq.PostTrade.QAP_T7176 import QAP_T7176
from test_cases.eq.PostTrade.QAP_T7182 import QAP_T7182
from test_cases.eq.PostTrade.QAP_T7183 import QAP_T7183
from test_cases.eq.PostTrade.QAP_T7186 import QAP_T7186
from test_cases.eq.PostTrade.QAP_T7190 import QAP_T7190
from test_cases.eq.PostTrade.QAP_T7192 import QAP_T7192
from test_cases.eq.PostTrade.QAP_T7194 import QAP_T7194
from test_cases.eq.PostTrade.QAP_T7216 import QAP_T7216
from test_cases.eq.PostTrade.QAP_T7253 import QAP_T7253
from test_cases.eq.PostTrade.QAP_T7266 import QAP_T7266
from test_cases.eq.PostTrade.QAP_T7282 import QAP_T7282
from test_cases.eq.PostTrade.QAP_T7297 import QAP_T7297
from test_cases.eq.PostTrade.QAP_T7305 import QAP_T7305
from test_cases.eq.PostTrade.QAP_T7306 import QAP_T7306
from test_cases.eq.PostTrade.QAP_T7362 import QAP_T7362
from test_cases.eq.PostTrade.QAP_T7384 import QAP_T7384
from test_cases.eq.PostTrade.QAP_T7385 import QAP_T7385
from test_cases.eq.PostTrade.QAP_T7388 import QAP_T7388
from test_cases.eq.PostTrade.QAP_T7389 import QAP_T7389
# from test_cases.eq.PostTrade.QAP_T7435 import QAP_T7435
from test_cases.eq.PostTrade.QAP_T7437 import QAP_T7437
from test_cases.eq.PostTrade.QAP_T7475 import QAP_T7475
from test_cases.eq.PostTrade.QAP_T7477 import QAP_T7477
from test_cases.eq.PostTrade.QAP_T7478 import QAP_T7478
from test_cases.eq.PostTrade.QAP_T7484 import QAP_T7484
from test_cases.eq.PostTrade.QAP_T7487 import QAP_T7487
from test_cases.eq.PostTrade.QAP_T7488 import QAP_T7488
from test_cases.eq.PostTrade.QAP_T7490 import QAP_T7490
from test_cases.eq.PostTrade.QAP_T7492 import QAP_T7492
from test_cases.eq.PostTrade.QAP_T7493 import QAP_T7493
from test_cases.eq.PostTrade.QAP_T7494 import QAP_T7494
from test_cases.eq.PostTrade.QAP_T7517 import QAP_T7517
from test_cases.eq.PostTrade.QAP_T8089 import QAP_T8089
from test_cases.eq.PostTrade.QAP_T8118 import QAP_T8118
from test_cases.fx.fx_mm_rfq.QAP_T7983 import QAP_T7983
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"PostTrade Analysis" if version is None else f"PostTrade Analysis | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("PostTrade")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("regression_cycle\eq_regression_cycle/layouts")
    layout_name = "all_columns_layout.xml"

    try:
        base_main_window.open_fe(test_id, fe_env=fe_env, is_open=False)
        base_main_window.import_layout(layout_path, layout_name)

        QAP_T6900(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6928(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6950(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6958(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6970(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6972(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7983(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7015(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7016(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7034(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7062(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7080(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7082(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7091(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7106(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7110(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7129(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7131(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7141(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7160(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7174(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7176(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7182(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7183(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7186(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7190(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7192(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7194(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7216(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T6228(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7253(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7266(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7282(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7297(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7305(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7306(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7359(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7360(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7362(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7363(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7383(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7384(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7385(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7388(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7389(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7435(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7437(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7438(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7443(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T6464(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7475(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7476(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7477(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7478(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7480(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7381(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7484(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7485(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7487(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7488(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7490(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7491(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7492(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7493(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7494(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7495(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7498(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7499(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7500(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7501(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7503(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7504(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7505(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7506(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7507(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7510(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7517(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7518(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7530(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7531(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7532(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7533(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7535(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7537(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7538(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7544(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7547(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7548(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7551(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7552(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T8089(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T8118(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()




    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"PostTrade regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
