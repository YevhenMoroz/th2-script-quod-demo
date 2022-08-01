import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4538 import QAP_4538
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4539 import QAP_4539
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4540 import QAP_4540
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4541 import QAP_4541
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4542 import QAP_4542
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4556 import QAP_4556
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4558 import QAP_4558
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4559 import QAP_4559
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4560 import QAP_4560
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4561 import QAP_4561
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4562 import QAP_4562
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4564 import QAP_4564
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4566 import QAP_4566
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4690 import QAP_4690
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4678 import QAP_4678
from test_cases.algo.Algo_Kepler.Algo_SynthMinQty.QAP_4706 import QAP_4706

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None):
    # Generation id and time for test run
    report_id = bca.create_event('SynthMinQty', parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region SynthMinQty
        configuration = ComponentConfiguration("synth_min_qty")
        QAP_4538(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4539(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4540(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4541(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4542(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4556(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4558(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4559(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4560(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4561(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4562(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4564(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4566(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4678(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4690(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4706(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()