import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4256 import QAP_T4256
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4196 import QAP_T4196
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4197 import QAP_T4197
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4309 import QAP_T4309
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4312 import QAP_T4312
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4352 import QAP_T4352
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4368 import QAP_T4368
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4453 import QAP_T4453
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4454 import QAP_T4454
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4466 import QAP_T4466
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4467 import QAP_T4467
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4468 import QAP_T4468
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4469 import QAP_T4469
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4474 import QAP_T4474
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4484 import QAP_T4484
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4485 import QAP_T4485
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4486 import QAP_T4486
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4525 import QAP_T4525
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4541 import QAP_T4541
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4542 import QAP_T4542
from test_cases.algo.Algo_Redburn.Algo_MOO.QAP_T4543 import QAP_T4543
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Auction - MOO/MOC/Expiry (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        configuration = ComponentConfigurationAlgo("PreOpen_Auction")

        # region auction start
        QAP_T4485(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4484(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4525(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4486(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4453(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4454(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Auction volume
        QAP_T4474(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4196(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region AuctionInitialSliceMultiplier
        QAP_T4542(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4543(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4541(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Would Price
        QAP_T4467(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4466(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4469(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4368(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4352(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4468(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4309(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region MaxParticipation
        QAP_T4256(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4197(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region LimitPriceOffset
        QAP_T4312(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()