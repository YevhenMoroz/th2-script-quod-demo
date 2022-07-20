import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3432 import QAP_3432
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3433 import QAP_3433
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3437 import QAP_3437
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3445 import QAP_3445
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3446 import QAP_3446
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3453 import QAP_3453
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3486 import QAP_3486
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3497 import QAP_3497
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3498 import QAP_3498
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3500 import QAP_3500
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3504 import QAP_3504
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3506 import QAP_3506
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3507 import QAP_3507
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3512 import QAP_3512
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3524 import QAP_3524
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3526 import QAP_3526
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3527 import QAP_3527
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3529 import QAP_3529
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3549 import QAP_3549
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3627 import QAP_3627
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3713 import QAP_3713
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3730 import QAP_3730
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3731 import QAP_3731
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3732 import QAP_3732
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3733 import QAP_3733
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_3994 import QAP_3994
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_4055 import QAP_4055
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_6067 import QAP_6067
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_8219 import QAP_8219

from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3150 import QAP_3150
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3151 import QAP_3151
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3153 import QAP_3153
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3154 import QAP_3154

from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2407 import QAP_2407
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2408 import QAP_2408
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2409 import QAP_2409
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2410 import QAP_2410
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2411 import QAP_2411
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2503 import QAP_2503
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2665 import QAP_2665
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2666 import QAP_2666
from test_cases.algo.Algo_Kepler.Algo_SORPING.QAP_2667 import QAP_2667

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
logging.getLogger().setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('skolesnyk tests')
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region MP Dark (Dark Phase Only)
        configuration = ComponentConfiguration("mp_dark")
        QAP_3497(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3498(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3500(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3504(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3506(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3507(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3512(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3524(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3526(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3527(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3529(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3549(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3713(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3730(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3731(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3732(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3733(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_8219(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region MP Dark (LIS + Dark phase)
        QAP_3432(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3433(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3437(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3445(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3446(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3453(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3453(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3486(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3627(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region MP Dark (other)
        QAP_3994(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4055(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_6067(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

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

        # region Iceberg: Route/Venue
        configuration = ComponentConfiguration("sors_iceberg")
        QAP_3150(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3151(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3153(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3154(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region SORPING
        configuration = ComponentConfiguration("sorping")
        QAP_2407(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2408(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2409(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2410(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2411(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2503(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2665(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2666(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2667(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()