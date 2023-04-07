import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T10674 import QAP_T10674
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T11006 import QAP_T11006
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4201 import QAP_T4201
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4202 import QAP_T4202
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4256 import QAP_T4256
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4290 import QAP_T4290
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4308 import QAP_T4308
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4311 import QAP_T4311
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4353 import QAP_T4353
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4366 import QAP_T4366
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4477 import QAP_T4477
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4479 import QAP_T4479
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4480 import QAP_T4480
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4481 import QAP_T4481
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4482 import QAP_T4482
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T4483 import QAP_T4483
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T8725 import QAP_T8725
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9085 import QAP_T9085
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9086 import QAP_T9086
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9087 import QAP_T9087
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9088 import QAP_T9088
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9096 import QAP_T9096
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9101 import QAP_T9101
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9332 import QAP_T9332
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9339 import QAP_T9339
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9340 import QAP_T9340
from test_cases.algo.Algo_Redburn.Algo_MOC.QAP_T9341 import QAP_T9341
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
        configuration = ComponentConfigurationAlgo("PreClose_Auction")

        # region auction start
        QAP_T4482(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4481(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4480(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4479(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4477(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4483(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10674(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Auction Volume
        QAP_T9332(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9087(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11006(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region AuctionInitialSliceMultiplier
        QAP_T9339(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9340(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9341(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region WouldPrice
        QAP_T4366(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4353(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4308(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region MaxParticipation
        QAP_T4290(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4256(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4202(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region LimitPriceOffset
        QAP_T4311(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4201(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Bi-Lateral
        QAP_T9085(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9086(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9096(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9088(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9101(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region splitThreshold
        QAP_T8725(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()