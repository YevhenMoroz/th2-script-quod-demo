import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.PostTrade.QAP_T6900 import QAP_T6900
from test_cases.eq.PostTrade.QAP_T6928 import QAP_T6928
from test_cases.eq.PostTrade.QAP_T6950 import QAP_T6950
from test_cases.eq.PostTrade.QAP_T6965 import QAP_T6965
from test_cases.eq.PostTrade.QAP_T6970 import QAP_T6970
from test_cases.eq.PostTrade.QAP_T6972 import QAP_T6972
from test_cases.eq.PostTrade.QAP_T6983 import QAP_T6983
from test_cases.eq.PostTrade.QAP_T7007 import QAP_T7007
from test_cases.eq.PostTrade.QAP_T7062 import QAP_T7062
from test_cases.eq.PostTrade.QAP_T7080 import QAP_T7080
from test_cases.eq.PostTrade.QAP_T7082 import QAP_T7082
from test_cases.eq.PostTrade.QAP_T7091 import QAP_T7091
from test_cases.eq.PostTrade.QAP_T7110 import QAP_T7110
from test_cases.eq.PostTrade.QAP_T7129 import QAP_T7129
from test_cases.eq.PostTrade.QAP_T7131 import QAP_T7131
from test_cases.eq.PostTrade.QAP_T7141 import QAP_T7141
from test_cases.eq.PostTrade.QAP_T7160 import QAP_T7160
from test_cases.eq.PostTrade.QAP_T7174 import QAP_T7174
from test_cases.eq.PostTrade.QAP_T7176 import QAP_T7176
from test_cases.eq.PostTrade.QAP_T7182 import QAP_T7182
from test_cases.eq.PostTrade.QAP_T7183 import QAP_T7183
from test_cases.eq.PostTrade.QAP_T7186 import QAP_T7186
from test_cases.eq.PostTrade.QAP_T7190 import QAP_T7190
from test_cases.eq.PostTrade.QAP_T7192 import QAP_T7192
from test_cases.eq.PostTrade.QAP_T7194 import QAP_T7194
from test_cases.eq.PostTrade.QAP_T7216 import QAP_T7216
from test_cases.eq.PostTrade.QAP_T7228 import QAP_T7228
from test_cases.eq.PostTrade.QAP_T7230 import QAP_T7230
from test_cases.eq.PostTrade.QAP_T7253 import QAP_T7253
from test_cases.eq.PostTrade.QAP_T7266 import QAP_T7266
from test_cases.eq.PostTrade.QAP_T7282 import QAP_T7282
from test_cases.eq.PostTrade.QAP_T7297 import QAP_T7297
from test_cases.eq.PostTrade.QAP_T7305 import QAP_T7305
from test_cases.eq.PostTrade.QAP_T7306 import QAP_T7306
from test_cases.eq.PostTrade.QAP_T7360 import QAP_T7360
from test_cases.eq.PostTrade.QAP_T7362 import QAP_T7362
from test_cases.eq.PostTrade.QAP_T7363 import QAP_T7363
from test_cases.eq.PostTrade.QAP_T7384 import QAP_T7384
from test_cases.eq.PostTrade.QAP_T7385 import QAP_T7385
from test_cases.eq.PostTrade.QAP_T7388 import QAP_T7388
from test_cases.eq.PostTrade.QAP_T7389 import QAP_T7389
from test_cases.eq.PostTrade.QAP_T7435 import QAP_T7435
from test_cases.eq.PostTrade.QAP_T7437 import QAP_T7437
from test_cases.eq.PostTrade.QAP_T7438 import QAP_T7438
from test_cases.eq.PostTrade.QAP_T7443 import QAP_T7443
from test_cases.eq.PostTrade.QAP_T7464 import QAP_T7464
from test_cases.eq.PostTrade.QAP_T7475 import QAP_T7475
from test_cases.eq.PostTrade.QAP_T7476 import QAP_T7476
from test_cases.eq.PostTrade.QAP_T7477 import QAP_T7477
from test_cases.eq.PostTrade.QAP_T7478 import QAP_T7478
from test_cases.eq.PostTrade.QAP_T7480 import QAP_T7480
from test_cases.eq.PostTrade.QAP_T7481 import QAP_T7481
from test_cases.eq.PostTrade.QAP_T7484 import QAP_T7484
from test_cases.eq.PostTrade.QAP_T7485 import QAP_T7485
from test_cases.eq.PostTrade.QAP_T7487 import QAP_T7487
from test_cases.eq.PostTrade.QAP_T7488 import QAP_T7488
from test_cases.eq.PostTrade.QAP_T7490 import QAP_T7490
from test_cases.eq.PostTrade.QAP_T7492 import QAP_T7492
from test_cases.eq.PostTrade.QAP_T7493 import QAP_T7493
from test_cases.eq.PostTrade.QAP_T7494 import QAP_T7494
from test_cases.eq.PostTrade.QAP_T7495 import QAP_T7495
from test_cases.eq.PostTrade.QAP_T7498 import QAP_T7498
from test_cases.eq.PostTrade.QAP_T7505 import QAP_T7505
from test_cases.eq.PostTrade.QAP_T7510 import QAP_T7510
from test_cases.eq.PostTrade.QAP_T7517 import QAP_T7517
from test_cases.eq.PostTrade.QAP_T7518 import QAP_T7518
from test_cases.eq.PostTrade.QAP_T7530 import QAP_T7530
from test_cases.eq.PostTrade.QAP_T7531 import QAP_T7531
from test_cases.eq.PostTrade.QAP_T7532 import QAP_T7532
from test_cases.eq.PostTrade.QAP_T7533 import QAP_T7533
from test_cases.eq.PostTrade.QAP_T7535 import QAP_T7535
from test_cases.eq.PostTrade.QAP_T7537 import QAP_T7537
from test_cases.eq.PostTrade.QAP_T7538 import QAP_T7538
from test_cases.eq.PostTrade.QAP_T7544 import QAP_T7544
from test_cases.eq.PostTrade.QAP_T7547 import QAP_T7547
from test_cases.eq.PostTrade.QAP_T7548 import QAP_T7548
from test_cases.eq.PostTrade.QAP_T7551 import QAP_T7551
from test_cases.eq.PostTrade.QAP_T7552 import QAP_T7552
from test_cases.eq.PostTrade.QAP_T8089 import QAP_T8089
from test_cases.eq.PostTrade.QAP_T8118 import QAP_T8118
from test_cases.eq.PostTrade.QAP_T8339 import QAP_T8339

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version='5.1.167.180'):
    report_id = bca.create_event(f"PostTrade Analysis" if version is None else f"PostTrade Analysis | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("PostTrade")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)

    try:
        base_main_window.open_fe(test_id, fe_env=fe_env, is_open=False)
        # base_main_window.import_layout(layout_path, layout_name)

        QAP_T7490(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7360(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7362(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7091(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6983(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7110(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7464(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7477(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7481(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7443(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7438(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T8339(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7131(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6950(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7389(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7388(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7475(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6972(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7216(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7230(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6970(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7297(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7228(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7532(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7538(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7552(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7531(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7551(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7488(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7537(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7183(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7194(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7007(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7192(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7306(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7305(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T8089(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6900(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7492(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7548(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7266(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7535(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7182(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7186(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7518(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7282(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7253(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T8118(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7495(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7485(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7530(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7498(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7505(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7478(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7176(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7062(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7082(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7476(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7359(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7141(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7484(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7080(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7480(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7510(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7517(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7174(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7494(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7493(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7547(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7544(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7487(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7533(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7385(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7190(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7129(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7160(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6928(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7384(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T6965(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7435(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7437(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7363(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"PostTrade regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        base_main_window.close_fe()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
