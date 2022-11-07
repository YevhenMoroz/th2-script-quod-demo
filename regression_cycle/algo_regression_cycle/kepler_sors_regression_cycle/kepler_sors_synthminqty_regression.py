import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4077 import QAP_T4077
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4076 import QAP_T4076
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4075 import QAP_T4075
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4074 import QAP_T4074
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4073 import QAP_T4073
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4072 import QAP_T4072
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4071 import QAP_T4071
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4070 import QAP_T4070
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4069 import QAP_T4069
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4068 import QAP_T4068
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4067 import QAP_T4067
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4066 import QAP_T4066
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4065 import QAP_T4065
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4063 import QAP_T4063
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4064 import QAP_T4064
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_T4062 import QAP_T4062

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"SynthMinQty" if version is None else f"Synthetic MinQty | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region SynthMinQty
        configuration = ComponentConfiguration("Synth_min_qty")
        QAP_T4077(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4076(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4075(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4074(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4073(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4072(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4071(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4070(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4069(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4068(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4067(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4066(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4065(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4064(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4063(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4062(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()