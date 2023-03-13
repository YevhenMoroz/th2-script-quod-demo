import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5028 import QAP_T5028
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5029 import QAP_T5029
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5030 import QAP_T5030
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5031 import QAP_T5031
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5032 import QAP_T5032
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5033 import QAP_T5033
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5034 import QAP_T5034
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5035 import QAP_T5035
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5036 import QAP_T5036
from test_cases.algo.Algo_Kepler.Algo_MIC_identification.QAP_T5037 import QAP_T5037
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Kepler MIC Identification" if version is None else f"Kepler MIC Identification (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Instrument identification
        configuration = ComponentConfiguration("Sorping")
        QAP_T5028(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5029(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5030(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5031(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5032(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5033(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5034(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5035(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5036(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5037(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()