import logging
import os
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from stubs import Stubs
from test_cases.eq.Care.QAP_T7403 import QAP_T7403
from test_cases.eq.Care.QAP_T7411 import QAP_T7411
from test_cases.eq.Care.QAP_T7418 import QAP_T7418
from test_cases.eq.Care.QAP_T7419 import QAP_T7419
from test_cases.eq.Care.QAP_T7420 import QAP_T7420
from test_cases.eq.Care.QAP_T7421 import QAP_T7421
from test_cases.eq.Care.QAP_T7422 import QAP_T7422
from test_cases.eq.Care.QAP_T7423 import QAP_T7423
from test_cases.eq.Care.QAP_T7432 import QAP_T7432
from test_cases.eq.Care.QAP_T7461 import QAP_T7461
from test_cases.eq.Care.QAP_T7479 import QAP_T7479
from test_cases.eq.Care.QAP_T7502 import QAP_T7502
from test_cases.eq.Care.QAP_T7509 import QAP_T7509
from test_cases.eq.Care.QAP_T7515 import QAP_T7515
from test_cases.eq.Care.QAP_T7519 import QAP_T7519
from test_cases.eq.Care.QAP_T7523 import QAP_T7523
from test_cases.eq.Care.QAP_T7524 import QAP_T7524
from test_cases.eq.Care.QAP_T7553 import QAP_T7553
from test_cases.eq.Care.QAP_T7554 import QAP_T7554
from test_cases.eq.Care.QAP_T7555 import QAP_T7555
from test_cases.eq.Care.QAP_T7619 import QAP_T7619
from test_cases.eq.Care.QAP_T7620 import QAP_T7620
from test_cases.eq.Care.QAP_T7621 import QAP_T7621
from test_cases.eq.Care.QAP_T7622 import QAP_T7622
from test_cases.eq.Care.QAP_T7623 import QAP_T7623
from test_cases.eq.Care.QAP_T7624 import QAP_T7624
from test_cases.eq.Care.QAP_T7626 import QAP_T7626
from test_cases.eq.Care.QAP_T7628 import QAP_T7628
from test_cases.eq.Care.QAP_T7629 import QAP_T7629
from test_cases.eq.Care.QAP_T7632 import QAP_T7632
from test_cases.eq.Care.QAP_T7633 import QAP_T7633
from test_cases.eq.Care.QAP_T7654 import QAP_T7654
from test_cases.eq.Care.QAP_T7655 import QAP_T7655
from test_cases.eq.Care.QAP_T7656 import QAP_T7656
from test_cases.eq.Care.QAP_T7657 import QAP_T7657
from test_cases.eq.Care.QAP_T7658 import QAP_T7658
from test_cases.eq.Care.QAP_T7659 import QAP_T7659
from test_cases.eq.Care.QAP_T7660 import QAP_T7660
from test_cases.eq.Care.QAP_T7661 import QAP_T7661
from test_cases.eq.Care.QAP_T7662 import QAP_T7662
from test_cases.eq.Care.QAP_T7663 import QAP_T7663
from test_cases.eq.Care.QAP_T7664 import QAP_T7664
from test_cases.eq.Care.QAP_T7665 import QAP_T7665
from test_cases.eq.Care.QAP_T7666 import QAP_T7666
from test_cases.eq.Care.QAP_T7667 import QAP_T7667
from test_cases.eq.Care.QAP_T7668 import QAP_T7668
from test_cases.eq.Care.QAP_T7669 import QAP_T7669
from test_cases.eq.Care.QAP_T7670 import QAP_T7670
from test_cases.eq.Care.QAP_T7671 import QAP_T7671
from test_cases.eq.Care.QAP_T7674 import QAP_T7674
from test_cases.eq.Care.QAP_T7676 import QAP_T7676
from test_cases.eq.Care.QAP_T7677 import QAP_T7677
from test_cases.eq.Care.QAP_T7679 import QAP_T7679
from test_cases.eq.Care.QAP_T7680 import QAP_T7680
from test_cases.eq.Care.QAP_T7681 import QAP_T7681
from test_cases.eq.Care.QAP_T7682 import QAP_T7682
from test_cases.eq.Care.QAP_T7683 import QAP_T7683
from test_cases.eq.Care.QAP_T7684 import QAP_T7684
from test_cases.eq.Care.QAP_T7685 import QAP_T7685
from test_cases.eq.Care.QAP_T7686 import QAP_T7686
# from test_cases.eq.Care.QAP_T7687 import QAP_T7687
from test_cases.eq.Care.QAP_T7688 import QAP_T7688
from test_cases.eq.Care.QAP_T7689 import QAP_T7689
from test_cases.eq.Care.QAP_T7692 import QAP_T7692
from test_cases.eq.Care.QAP_T7695 import QAP_T7695
from test_cases.eq.Care.QAP_T7696 import QAP_T7696
from test_cases.eq.Care.QAP_T7697 import QAP_T7697
from test_cases.eq.Care.QAP_T7698 import QAP_T7698
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def test_run(parent_id= None, version=None):
    report_id = bca.create_event(f"Care Analysis" if version is None else f"Care Analysis | {version}", parent_id)
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Care")
    fe_env = configuration.environment.get_list_fe_environment()[0]
    session_id = set_session_id(fe_env.target_server_win)
    data_set = configuration.data_set
    test_id = bca.create_event(Path(__file__).name[:-3], report_id)
    base_main_window = BaseMainWindow(test_id, session_id)
    layout_path = os.path.abspath("regression_cycle\eq_regression_cycle/layouts")
    layout_name = "all_columns_layout.xml"
    try:
        base_main_window.open_fe(test_id, fe_env=fe_env, is_open=False)
        base_main_window.import_layout(layout_path, layout_name)
        QAP_T7698(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7697(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7689(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7688(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7687(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7686(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7685(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7684(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7683(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7682(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7681(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7680(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7677(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7676(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7674(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7673(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        # QAP_T7672(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7671(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7670(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7669(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7668(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7667(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7666(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7665(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7664(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7663(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7662(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7661(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7660(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7659(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7658(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7657(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7656(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7655(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7654(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7633(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7632(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7629(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7628(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7626(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7623(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7622(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7621(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7553(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7524(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7523(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7519(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7515(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7509(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7502(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7479(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7432(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7423(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7419(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7418(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7403(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7411(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7418(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7419(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7420(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7421(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7422(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7423(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7432(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        # QAP_T7454(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
        #     .execute()
        QAP_T7461(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7554(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7555(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7619(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7620(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7624(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7679(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7692(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7695(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_T7696(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Care regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
        base_main_window.close_fe()



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
