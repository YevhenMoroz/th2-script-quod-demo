from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_mm_esp.QAP_T2375 import QAP_T2375
from test_cases.fx.fx_mm_esp.QAP_T2386 import QAP_T2386
from test_cases.fx.fx_mm_esp.QAP_T2406 import QAP_T2406
from test_cases.fx.fx_mm_esp.QAP_T2411 import QAP_T2411
from test_cases.fx.fx_mm_esp.QAP_T2413 import QAP_T2413
from test_cases.fx.fx_mm_esp.QAP_T2426 import QAP_T2426
from test_cases.fx.fx_mm_esp.QAP_T2430 import QAP_T2430
from test_cases.fx.fx_mm_esp.QAP_T2431 import QAP_T2431
from test_cases.fx.fx_mm_esp.QAP_T2432 import QAP_T2432
from test_cases.fx.fx_mm_esp.QAP_T2434 import QAP_T2434
from test_cases.fx.fx_mm_esp.QAP_T2437 import QAP_T2437
from test_cases.fx.fx_mm_esp.QAP_T2438 import QAP_T2438
from test_cases.fx.fx_mm_esp.QAP_T2446 import QAP_T2446
from test_cases.fx.fx_mm_esp.QAP_T2451 import QAP_T2451
from test_cases.fx.fx_mm_esp.QAP_T2459 import QAP_T2459
from test_cases.fx.fx_mm_esp.QAP_T2460 import QAP_T2460
from test_cases.fx.fx_mm_esp.QAP_T2464 import QAP_T2464
from test_cases.fx.fx_mm_esp.QAP_T2479 import QAP_T2479
from test_cases.fx.fx_mm_esp.QAP_T2497 import QAP_T2497
from test_cases.fx.fx_mm_esp.QAP_T2518 import QAP_T2518
from test_cases.fx.fx_mm_esp.QAP_T2710 import QAP_T2710
from test_cases.fx.fx_mm_esp.QAP_T2719 import QAP_T2719
from test_cases.fx.fx_mm_esp.QAP_T2729 import QAP_T2729
from test_cases.fx.fx_mm_esp.QAP_T2730 import QAP_T2730
from test_cases.fx.fx_mm_esp.QAP_T2733 import QAP_T2733
from test_cases.fx.fx_mm_esp.QAP_T2734 import QAP_T2734
from test_cases.fx.fx_mm_esp.QAP_T2735 import QAP_T2735
from test_cases.fx.fx_mm_esp.QAP_T2742 import QAP_T2742
from test_cases.fx.fx_mm_esp.QAP_T2749 import QAP_T2749
from test_cases.fx.fx_mm_esp.QAP_T2751 import QAP_T2751
from test_cases.fx.fx_mm_esp.QAP_T2801 import QAP_T2801
from test_cases.fx.fx_mm_esp.QAP_T2838 import QAP_T2838
from test_cases.fx.fx_mm_esp.QAP_T2870 import QAP_T2870
from test_cases.fx.fx_mm_esp.QAP_T2892 import QAP_T2892
from test_cases.fx.fx_mm_esp.QAP_T2896 import QAP_T2896
from test_cases.fx.fx_mm_esp.QAP_T2902 import QAP_T2902
from test_cases.fx.fx_mm_esp.QAP_T2911 import QAP_T2911
from test_cases.fx.fx_mm_esp.QAP_T2917 import QAP_T2917
from test_cases.fx.fx_mm_esp.QAP_T2947 import QAP_T2947
from test_cases.fx.fx_mm_esp.QAP_T2948 import QAP_T2948
from test_cases.fx.fx_mm_esp.QAP_T2953 import QAP_T2953
from test_cases.fx.fx_mm_esp.QAP_T2964 import QAP_T2964
from test_cases.fx.fx_mm_esp.QAP_T2965 import QAP_T2965
from test_cases.fx.fx_mm_esp.QAP_T2966 import QAP_T2966
from test_cases.fx.fx_mm_esp.QAP_T2986 import QAP_T2986
from test_cases.fx.fx_mm_esp.QAP_T7936 import QAP_T7936
from test_cases.fx.fx_mm_esp.QAP_T8162 import QAP_T8162
from test_cases.fx.fx_taker_esp.QAP_T2456 import QAP_T2456
from test_cases.fx.fx_mm_esp.QAP_T2457 import QAP_T2457
from test_cases.fx.fx_mm_esp.QAP_T2458 import QAP_T2458
from test_cases.fx.fx_mm_esp.QAP_T2462 import QAP_T2462
from test_cases.fx.fx_mm_esp.QAP_T2543 import QAP_T2543
from test_cases.fx.fx_mm_esp.QAP_T2561 import QAP_T2561
from test_cases.fx.fx_mm_esp.QAP_T2562 import QAP_T2562
from test_cases.fx.fx_mm_esp.QAP_T2578 import QAP_T2578
from test_cases.fx.fx_mm_esp.QAP_T2602 import QAP_T2602
from test_cases.fx.fx_mm_esp.QAP_T2605 import QAP_T2605
from test_cases.fx.fx_mm_esp.QAP_T2615 import QAP_T2615
from test_cases.fx.fx_mm_esp.QAP_T2619 import QAP_T2619
from test_cases.fx.fx_mm_esp.QAP_T2622_manual import QAP_T2622
from test_cases.fx.fx_mm_esp.QAP_T2650 import QAP_T2650
from test_cases.fx.fx_mm_esp.QAP_T2652 import QAP_T2652
from test_cases.fx.fx_mm_esp.QAP_T2684 import QAP_T2684
from test_cases.fx.fx_mm_esp.QAP_T2722 import QAP_T2722
from test_cases.fx.fx_mm_esp.QAP_T2736 import QAP_T2736
from test_cases.fx.fx_mm_esp.QAP_T2745 import QAP_T2745
from test_cases.fx.fx_mm_esp.QAP_T2758 import QAP_T2758
from test_cases.fx.fx_mm_esp.QAP_T2768 import QAP_T2768
from test_cases.fx.fx_mm_esp.QAP_T2832 import QAP_T2832
from test_cases.fx.fx_mm_esp.QAP_T2883 import QAP_T2883
from test_cases.fx.fx_mm_esp.QAP_T2889 import QAP_T2889
from test_cases.fx.fx_mm_esp.QAP_T2890 import QAP_T2890
from test_cases.fx.fx_mm_esp.QAP_T2891 import QAP_T2891
from test_cases.fx.fx_mm_esp.QAP_T2893 import QAP_T2893
from test_cases.fx.fx_mm_esp.QAP_T2894 import QAP_T2894
from test_cases.fx.fx_mm_esp.QAP_T2895 import QAP_T2895
from test_cases.fx.fx_mm_esp.QAP_T2897 import QAP_T2897
from test_cases.fx.fx_mm_esp.QAP_T2915 import QAP_T2915
from test_cases.fx.fx_mm_esp.QAP_T2916 import QAP_T2916
from test_cases.fx.fx_mm_esp.QAP_T2919 import QAP_T2919
from test_cases.fx.fx_mm_esp.QAP_T2920 import QAP_T2920
from test_cases.fx.fx_mm_esp.QAP_T2921 import QAP_T2921
from test_cases.fx.fx_mm_esp.QAP_T2926 import QAP_T2926
# from test_cases.fx.fx_mm_esp.QAP_T2947 import QAP_T2947
from test_cases.fx.fx_mm_esp.QAP_T2955 import QAP_T2955
from test_cases.fx.fx_mm_esp.QAP_T2956 import QAP_T2956
from test_cases.fx.fx_mm_esp.QAP_T2957 import QAP_T2957
from test_cases.fx.fx_mm_esp.QAP_T2968 import QAP_T2968
from test_cases.fx.fx_mm_esp.QAP_T2983 import QAP_T2983
from test_cases.fx.fx_taker_esp.QAP_T2624 import QAP_T2624
from test_framework.configurations.component_configuration import ComponentConfiguration, ComponentConfigurationFX

from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=""):
    #  !!!START FXFH_Q MDA_Q!!! before running regression
    report_id = bca.create_event(f"FX_MM_ESP_automation" if version is None else f"FX_MM_ESP_automation | {version}",
                                 parent_id)
    session_id = set_session_id("amedents")
    main_window_name = "Quod Financial - Quod site 314"
    configuration = ComponentConfigurationFX("ESP_MM")

    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id, main_window_name)

        # region FIX test
        QAP_T2375(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2386(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T2406(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2411(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2413(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2426(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2430(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T2431(report_id, data_set=configuration.data_set, environment=configuration.environment).execute() #Problem with quantity set
        QAP_T2432(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2434(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2437(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T2438(report_id, data_set=configuration.data_set, environment=configuration.environment).execute() # to write cfg modification
        QAP_T2446(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2451(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2457(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2458(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2459(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2460(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2462(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2479(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2497(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2518(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2543(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2561(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2562(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2578(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2602(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2605(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2615(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2619(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2650(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2652(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2684(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2710(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2722(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2729(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2730(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2733(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2734(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2735(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2736(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2745(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2749(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2751(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2758(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2768(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2801(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2832(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2838(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2870(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2883(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2889(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2890(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2891(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2892(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2893(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2894(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2895(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2896(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2897(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2902(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2911(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2915(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2916(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2917(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2919(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2920(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T2921(report_id, data_set=configuration.data_set, environment=configuration.environment).execute() problem with quantity set
        QAP_T2926(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2947(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2948(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2953(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2955(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2956(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2957(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2964(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2965(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2966(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2968(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2983(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T7936(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8162(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        QAP_T2464(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # # region UI test
        # QAP_T2742(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T2423(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2433(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2710(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2749(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2753(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2759(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2784(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2792(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2870(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2898(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2902(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2913(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2943(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2947(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2948(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2954(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2960(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2964(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2965(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2966(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2980(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2985(report_id, session_id, configuration.data_set, configuration.environment).execute()
        # QAP_T2986(report_id, session_id, configuration.data_set, configuration.environment).execute()
        #
        # QAP_T2547.execute(report_id, session_id)
        # QAP_T2782.execute(report_id, session_id)
        # QAP_T2793.execute(report_id, session_id)
        # QAP_T2911.execute(report_id, session_id)
        # # endregion

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
