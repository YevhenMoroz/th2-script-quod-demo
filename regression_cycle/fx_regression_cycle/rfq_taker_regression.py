from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_taker_rfq.QAP_T2599 import QAP_T2599
from test_cases.fx.fx_taker_rfq.QAP_T2708 import QAP_T2708
from test_cases.fx.fx_taker_rfq.QAP_T2941 import QAP_T2941
from test_cases.fx.fx_taker_rfq.QAP_T2802 import QAP_T2802
from test_cases.fx.fx_taker_rfq.QAP_T2770 import QAP_T2770
from test_cases.fx.fx_taker_rfq.QAP_T2769 import QAP_T2769
from test_cases.fx.fx_taker_rfq.QAP_T2762 import QAP_T2762
from test_cases.fx.fx_taker_rfq.QAP_T2748 import QAP_T2748
from test_cases.fx.fx_taker_rfq.QAP_T2747 import QAP_T2747
from test_cases.fx.fx_taker_rfq.QAP_T3075 import QAP_T3075
from test_cases.fx.fx_taker_rfq.QAP_T3074 import QAP_T3074
from test_cases.fx.fx_taker_rfq.QAP_T3073 import QAP_T3073
from test_cases.fx.fx_taker_rfq.QAP_T3071 import QAP_T3071
from test_cases.fx.fx_taker_rfq.QAP_T3070 import QAP_T3070
from test_cases.fx.fx_taker_rfq.QAP_T3069 import QAP_T3069
from test_cases.fx.fx_taker_rfq.QAP_T3068 import QAP_T3068
from test_cases.fx.fx_taker_rfq.QAP_T3066 import QAP_T3066
from test_cases.fx.fx_taker_rfq.QAP_T3065 import QAP_T3065
from test_cases.fx.fx_taker_rfq.QAP_T3064 import QAP_T3064
from test_cases.fx.fx_taker_rfq.QAP_T3063 import QAP_T3063
from test_cases.fx.fx_taker_rfq.QAP_T3061 import QAP_T3061
from test_cases.fx.fx_taker_rfq.QAP_T3060 import QAP_T3060
from test_cases.fx.fx_taker_rfq.QAP_T3059 import QAP_T3059
from test_cases.fx.fx_taker_rfq.QAP_T3058 import QAP_T3058
from test_cases.fx.fx_taker_rfq.QAP_T3057 import QAP_T3057
from test_cases.fx.fx_taker_rfq.QAP_T3056 import QAP_T3056
from test_cases.fx.fx_taker_rfq.QAP_T3055 import QAP_T3055
from test_cases.fx.fx_taker_rfq.QAP_T3053 import QAP_T3053
from test_cases.fx.fx_taker_rfq.QAP_T3051 import QAP_T3051
from test_cases.fx.fx_taker_rfq.QAP_T3050 import QAP_T3050
from test_cases.fx.fx_taker_rfq.QAP_T3049 import QAP_T3049
from test_cases.fx.fx_taker_rfq.QAP_T3047 import QAP_T3047
from test_cases.fx.fx_taker_rfq.QAP_T3046 import QAP_T3046
from test_cases.fx.fx_taker_rfq.QAP_T3045 import QAP_T3045
from test_cases.fx.fx_taker_rfq.QAP_T3044 import QAP_T3044
from test_cases.fx.fx_taker_rfq.QAP_T3043 import QAP_T3043
from test_cases.fx.fx_taker_rfq.QAP_T3042 import QAP_T3042
from test_cases.fx.fx_taker_rfq.QAP_T3110 import QAP_T3110
from test_cases.fx.fx_taker_rfq.QAP_T3041 import QAP_T3041
from test_cases.fx.fx_taker_rfq.QAP_T3040 import QAP_T3040
from test_cases.fx.fx_taker_rfq.QAP_T3039 import QAP_T3039
from test_cases.fx.fx_taker_rfq.QAP_T3038 import QAP_T3038
from test_cases.fx.fx_taker_rfq.QAP_T3037 import QAP_T3037
from test_cases.fx.fx_taker_rfq.QAP_T3036 import QAP_T3036
from test_cases.fx.fx_taker_rfq.QAP_T3035 import QAP_T3035
from test_cases.fx.fx_taker_rfq.QAP_T3034 import QAP_T3034
from test_cases.fx.fx_taker_rfq.QAP_T3028 import QAP_T3028
from test_cases.fx.fx_taker_rfq.QAP_T3027 import QAP_T3027
from test_cases.fx.fx_taker_rfq.QAP_T3026 import QAP_T3026
from test_cases.fx.fx_taker_rfq.QAP_T3025 import QAP_T3025
from test_cases.fx.fx_taker_rfq.QAP_T3015 import QAP_T3015
from test_cases.fx.fx_taker_rfq.QAP_T3013 import QAP_T3013
from test_cases.fx.fx_taker_rfq.QAP_T3012 import QAP_T3012
from test_cases.fx.fx_taker_rfq.QAP_T2415 import QAP_T2415
from test_cases.fx.fx_taker_rfq.QAP_T3009 import QAP_T3009
from test_cases.fx.fx_taker_rfq.QAP_T3003 import QAP_T3003
from test_cases.fx.fx_taker_rfq.QAP_T3002 import QAP_T3002
from test_cases.fx.fx_taker_rfq.QAP_T2998 import QAP_T2998
from test_cases.fx.fx_taker_rfq.QAP_T2996 import QAP_T2996
from test_cases.fx.fx_taker_rfq.QAP_T2995 import QAP_T2995
from test_cases.fx.fx_taker_rfq.QAP_T2994 import QAP_T2994
from test_cases.fx.fx_taker_rfq.QAP_T2993 import QAP_T2993
from test_cases.fx.fx_taker_rfq.QAP_T2989 import QAP_T2989
from test_cases.fx.fx_taker_rfq.QAP_T2988 import QAP_T2988
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.import_layouts.layout_loader import LayoutLoader

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"FX_Taker_RFQ" if version is None else f"FX_Taker_RFQ | {version}", parent_id)
    session_id = set_session_id(target_server_win="ostronov")
    configuration = ComponentConfiguration("RFQ_Taker")
    try:
        window_name = "Quod Financial - Quod site 314"
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id, window_name)

        LayoutLoader(report_id, session_id).import_layout("rfq_taker_layout.xml", "fx")

        QAP_T3110(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3075(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3074(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3073(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T3072.execute(report_id, session_id)
        QAP_T3071(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3070(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3069(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3068(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3066(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3065(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3064(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3063(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T3062.execute(report_id, session_id)
        QAP_T3061(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3060(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3059(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3058(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3057(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3056(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3055(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3053(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3051(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3050(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3049(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T3048.execute(report_id, session_id)
        QAP_T3047(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3046(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3045(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3044(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3043(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3042(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3041(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3040(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3039(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3038(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3037(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3036(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3035(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3034(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T3033.execute(report_id, session_id)
        # QAP_T3032.execute(report_id, session_id)
        QAP_T3028(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3027(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3026(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3025(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T3023.execute(report_id, session_id)
        # QAP_T3020.execute(report_id, session_id)
        QAP_T3015(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T3014.execute(report_id, session_id)
        QAP_T3013(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3012(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3009(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T3008.execute(report_id, session_id)
        QAP_T3003(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T3002(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2998(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2996(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2995(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2994(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2993(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2989(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2988(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T2961.execute(report_id, session_id)
        QAP_T2941(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T2825.execute(report_id, session_id)
        QAP_T2802(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2770(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2769(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2762(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2748(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2747(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T2746.execute(report_id, session_id)
        QAP_T2415(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T2744.execute(report_id, session_id)
        QAP_T2708(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        QAP_T2599(report_id=report_id, session_id=session_id, data_set=configuration.data_set).execute()
        # QAP_T2612.execute(report_id, session_id)
        # QAP_T3014.execute(report_id, session_id)
        # QAP_T2717.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
