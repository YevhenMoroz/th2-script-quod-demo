import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.ArchiveWindows.QAP_T8159 import QAP_T8159
from test_cases.eq.Bag.QAP_T7634 import QAP_T7634
from test_cases.eq.Basket.QAP_T7433 import QAP_T7433
from test_cases.eq.Basket.QAP_T7453 import QAP_T7453
from test_cases.eq.Care.QAP_T7626 import QAP_T7626
from test_cases.eq.Care.QAP_T7689 import QAP_T7689
from test_cases.eq.Commissions.QAP_T7497 import QAP_T7497
from test_cases.eq.Commissions.QAP_T7534 import QAP_T7534
from test_cases.eq.DMA.QAP_T7549 import QAP_T7549
from test_cases.eq.DMA.QAP_T7610 import QAP_T7610
from test_cases.eq.DMA.QAP_T7615 import QAP_T7615
from test_cases.eq.Gateway.QAP_T7507 import QAP_T7507
from test_cases.eq.GatingRules.QAP_T4928 import QAP_T4928
from test_cases.eq.GatingRules.QAP_T4929 import QAP_T4929
from test_cases.eq.GatingRules.QAP_T4930 import QAP_T4930
from test_cases.eq.GatingRules.QAP_T4931 import QAP_T4931
from test_cases.eq.Positions.QAP_T7598 import QAP_T7598
from test_cases.eq.Positions.QAP_T7606 import QAP_T7606
from test_cases.eq.PostTrade.QAP_T7517 import QAP_T7517
from test_cases.eq.PostTrade.QAP_T7550 import QAP_T7550
from test_cases.eq.PostTrade.QAP_T7552 import QAP_T7552
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"PEQ Acceptance v.194" if version is None else f"PEQ Acceptance v.194 | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("AcceptanceList")
    data_set = configuration.data_set
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = None #set_session_id(fe_env.target_server_win)
    # test_id = bca.create_event(Path(__file__).name[:-3], report_id)


    try:
        QAP_T4930(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4931(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4928(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T4929(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7549(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7689(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7626(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7615(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7610(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7608(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7606(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7598(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7561(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7552(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7550(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7549(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7541(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T8159(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7497(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7534(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7517(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7507(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7453(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7433(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7598(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7606(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7447(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7634(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Acceptance list was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        # Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    test_run(version="5.1.181.194")
    Stubs.factory.close()
