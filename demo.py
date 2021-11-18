import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.fx_mm_autohedging import QAP_2159, QAP_2228, QAP_2255, QAP_2322, QAP_3939, QAP_2470, QAP_3146, QAP_3147, \
    QAP_5551, QAP_3354, QAP_3067, QAP_2326
from quod_qa.fx.fx_mm_esp import QAP_1554, QAP_2872, QAP_1518
from quod_qa.fx.fx_mm_rfq import for_test_77679
from quod_qa.fx.fx_mm_rfq.interpolation import QAP_4234, QAP_3851, QAP_3850, QAP_3807, QAP_3739, QAP_3734
from quod_qa.fx.fx_mm_rfq.rejection import QAP_3735, QAP_3740

from quod_qa.fx.fx_taker_esp import QAP_5537, QAP_5635_not_ready, QAP_5600_not_ready, QAP_5589_not_ready, \
    QAP_5369_not_ready, QAP_5564_blocked_by_PFX_3932, QAP_5591_blocked_by_PFX_3932, QAP_5598_not_ready, QAP_3253
from quod_qa.fx.fx_taker_rfq import QAP_568
from quod_qa.fx.qs_fx_routine import SendMD, rfq_spot, java_api, java_api_MDReq
from quod_qa.fx.ui_wrappers import wrapper_test
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run


    report_id = bca.create_event('KKL    ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"


    test_cases = {
        'case_id': bca.create_event_id(),
        'TraderConnectivity': 'fix-ss-rfq-314-luna-standard',
        'Account': 'Iridium1',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
    }

    session_id=set_session_id()
    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        # QAP_2290.execute(report_id, session_id)
        #
        # QAP_5635.execute(report_id, session_id)
        # wrapper_test.execute(report_id,session_id)


        # QAP_5564_blocked_by_PFX_3932.execute(report_id,session_id)
        for_test_77679.execute(report_id,session_id)
        # for_Daria.execute(report_id,session_id)
        # SendMD.execute(report_id)
        # QAP_2872.execute(report_id)

        # QAP_5591_blocked_by_PFX_3932.execute(report_id,session_id)


        # QAP_2326.execute(report_id, session_id)
        # QAP_568.execute(report_id, session_id)
        # QAP_5537.execute(report_id,session_id)
        # java_api.TestCase(report_id).execute()



        # QAP_2092WIP.execute(report_id,session_id)
        # QAP_1558.execute(report_id)
        # QAP_2290.execute(report_id,session_id)
        # QAP_2322.execute(report_id, session_id)

        # java_api_MDReq.TestCase().execute(report_id)




        # rfq_spot.execute(report_id)
        # esp_1W.execute(report_id)
        # java_api.TestCase(report_id).execute()
        # java_api_Subscribe.TestCase().execute(report_id)
        # example_java_api.TestCase(report_id).execute()


        # QAP_3689.execute(report_id)
        # QAP_2353.execute(report_id)
        # QAP_3806.execute(report_id)

        # QAP_3747.execute(report_id)



        # QAP_3689.execute(report_id)


        rm = RuleManager()

        # rm.add_TRFQ('fix-bs-rfq-314-luna-standard')
        # rm.remove_rule_by_id(326)
        # rm.add_QuodMDAnswerRule('fix-fh-314-luna',interval=5)
        # rm.print_active_rules()


        # rm.print_active_rules_sim_test()



        # rm.remove_rule_by_id(4)
        # rm.remove_rule_by_id(5)

        # rm.remove_rule_by_id(10)
        # rm.remove_rule_by_id_test_sim(4)
        # rm.remove_rule_by_id_test_sim(3)
        # # # rm.add_RFQ('fix-bs-rfq-314-luna-standard')
        # rm.add_fx_md_to('fix-fh-q-314-luna')
        # rm.add_fx_md_to_test_sim('fix-fh-314-luna')
        # rm.add_fx_md_to_test_sim('fix-fh-q-314-luna')
        # rm.add_TRFQ_test_sim('fix-bs-rfq-314-luna-standard')
        # rm.add_TRFQ('fix-bs-rfq-314-luna-standard')
        # # rm.add_RFQ('fix-bs-rfq-314-luna-standard')
        # # rm.remove_rule_by_id(574)
        # rm.print_active_rules()


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

#
   #     rm.print_active_rules()
#
    #   ui_tests.execute(report_id)

    #except Exception:
        #logging.error("Error execution", exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








