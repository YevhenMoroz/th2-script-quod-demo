import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_TWAP import QAP_T4332, QAP_T4286, QAP_T4335
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4606 import QAP_T4606
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4652 import QAP_T4652
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4653 import QAP_T4653
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4654 import QAP_T4654
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4667 import QAP_T4667
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4668 import QAP_T4668
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4669 import QAP_T4669
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4670 import QAP_T4670
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4671 import QAP_T4671
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4672 import QAP_T4672
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4677 import QAP_T4677
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4678 import QAP_T4678
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4679 import QAP_T4679
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4680 import QAP_T4680
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4681 import QAP_T4681
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4682 import QAP_T4682
from test_cases.algo.Algo_TWAP import QAP_T4692, QAP_T4693, QAP_T4694, QAP_T4695, QAP_T4557, QAP_T4696, QAP_T4572, QAP_T4697, QAP_T4579, QAP_T4698, QAP_T4600, QAP_T4699, QAP_T4605, QAP_T4700, QAP_T4655, QAP_T4701, QAP_T4664, QAP_T4702, QAP_T4665, QAP_T4666, QAP_T4687, QAP_T4690, QAP_T4691
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"TWAP - Additional Features (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region TWAP Additional Featured
        configuration = ComponentConfigurationAlgo("Twap")
        QAP_T4606(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4652(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4653(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4654(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4667(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4668(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4669(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4670(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4671(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4672(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4677(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4678(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4679(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4680(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4681(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4682(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Needs Refactoring
        # QAP_T4692.execute(report_id)
        # QAP_T4693.execute(report_id)
        # QAP_T4694.execute(report_id)
        # QAP_T4695.execute(report_id)
        # QAP_T4557.execute(report_id)
        # QAP_T4696.execute(report_id)
        # QAP_T4572.execute(report_id)
        # QAP_T4697.execute(report_id)
        # QAP_T4579.execute(report_id)
        # QAP_T4698.execute(report_id)
        # QAP_T4600.execute(report_id)
        # QAP_T4699.execute(report_id)
        # QAP_T4605.execute(report_id)
        # QAP_T4700.execute(report_id)
        # QAP_T4655.execute(report_id)
        # QAP_T4701.execute(report_id)
        # QAP_T4664.execute(report_id)
        # QAP_T4702.execute(report_id)
        # QAP_T4665.execute(report_id)
        # QAP_T4666.execute(report_id)
        # QAP_T4687.execute(report_id)
        # QAP_T4690.execute(report_id)
        # QAP_T4691.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()