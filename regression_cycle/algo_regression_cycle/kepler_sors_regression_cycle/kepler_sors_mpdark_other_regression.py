import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4158 import QAP_T4158
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4360 import QAP_T4360
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4429 import QAP_T4429
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4431 import QAP_T4431
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4522 import QAP_T4522
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4707 import QAP_T4707
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4708 import QAP_T4708
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4710 import QAP_T4710
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4711 import QAP_T4711
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4712 import QAP_T4712
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4713 import QAP_T4713
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4714 import QAP_T4714
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4715 import QAP_T4715
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4716 import QAP_T4716
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4719 import QAP_T4719
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4720 import QAP_T4720
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4721 import QAP_T4721
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4722 import QAP_T4722
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4723 import QAP_T4723
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4725 import QAP_T4725
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4738 import QAP_T4738
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4739 import QAP_T4739
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4521 import QAP_T4521
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4578 import QAP_T4578
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4674 import QAP_T4674
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4675 import QAP_T4675
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4717 import QAP_T4717
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4729 import QAP_T4729
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4724 import QAP_T4724
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4718 import QAP_T4718
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4358 import QAP_T4358
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4726 import QAP_T4726

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"MPDark (other)" if version is None else f"MPDark (other) for th2 integration (cloned) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfiguration("Mp_dark")
        # region MP Dark (other)
        QAP_T4158(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4360(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4429(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4431(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4521(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4522(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4578(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4674(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4675(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4707(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4708(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4710(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4711(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4712(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4713(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4714(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4715(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4716(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4717(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4718(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4719(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4720(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4721(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4722(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4723(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4724(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4725(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4726(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4729(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4738(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4739(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4358(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()