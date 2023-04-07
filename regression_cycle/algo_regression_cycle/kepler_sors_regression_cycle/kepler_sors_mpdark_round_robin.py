import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10485 import QAP_T10485
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10486 import QAP_T10486
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10487 import QAP_T10487
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10493 import QAP_T10493
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10501 import QAP_T10501
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10502 import QAP_T10502
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10504 import QAP_T10504
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10508 import QAP_T10508
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10509 import QAP_T10509
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10510 import QAP_T10510
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10517 import QAP_T10517
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10523 import QAP_T10523
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10524 import QAP_T10524
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10525 import QAP_T10525
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10526 import QAP_T10526
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10527 import QAP_T10527
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10528 import QAP_T10528
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10529 import QAP_T10529
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10530 import QAP_T10530
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10531 import QAP_T10531
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10532 import QAP_T10532
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10533 import QAP_T10533
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10534 import QAP_T10534
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10536 import QAP_T10536
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10541 import QAP_T10541
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10542 import QAP_T10542
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10543 import QAP_T10543
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10544 import QAP_T10544
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10546 import QAP_T10546
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10547 import QAP_T10547
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10623 import QAP_T10623
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10624 import QAP_T10624
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10625 import QAP_T10625
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10664 import QAP_T10664
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10671 import QAP_T10671
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10679 import QAP_T10679
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10681 import QAP_T10681
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10682 import QAP_T10682
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10683 import QAP_T10683
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10684 import QAP_T10684
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10691 import QAP_T10691
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10694 import QAP_T10694
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10699 import QAP_T10699
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10700 import QAP_T10700
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10701 import QAP_T10701
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10702 import QAP_T10702
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10705 import QAP_T10705
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10714 import QAP_T10714
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10725 import QAP_T10725
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10740 import QAP_T10740
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T10741 import QAP_T10741
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T9292 import QAP_T9292
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"MPDark (RoundRobin)" if version is None else f"MPDark (RoundRobin) (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region MP Dark (Dark Phase Only)
        configuration = ComponentConfiguration("Mp_dark")
        QAP_T9292(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10485(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10486(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10487(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10493(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10501(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10502(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10504(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10508(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10509(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10510(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10517(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10523(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10524(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10525(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10526(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10527(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10528(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10529(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10530(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10531(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10532(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10533(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10534(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10536(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10541(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10542(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10543(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10544(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10546(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10547(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10624(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10623(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10625(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10664(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10671(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10679(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10681(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10682(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10683(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10684(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10691(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10699(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10694(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10700(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10702(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10701(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10705(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10714(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10725(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10740(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10741(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
