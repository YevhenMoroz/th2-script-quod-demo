import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.fx.qs_fx_routine import SendMD

from rule_management import RuleManager
from stubs import Stubs
from test_cases.fx.fx_mm_autohedging import QAP_2251
from test_cases.fx.fx_mm_esp import QAP_1518
from test_cases.fx.fx_mm_rfq.interpolation import QAP_4234, QAP_3851, QAP_3850, QAP_3807, QAP_3806, QAP_3766, QAP_3805, \
    QAP_3747, QAP_3689, QAP_3739
from test_cases.fx.fx_mm_rfq.rejection import QAP_3735
from test_cases.fx.fx_taker_esp import QAP_5635, QAP_5537, QAP_5564
from test_cases.fx.qs_fx_routine import QAP_5176, DepositAndLoan
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()

def test_run():
    # Generation id and time for test run
    logging.getLogger().setLevel(logging.WARN)

    report_id = bca.create_event('KKL    ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))

    logger.info(f"Root event was created (id = {report_id.id})")
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"



    session_id=set_session_id()
    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)

        # QAP_2290.execute(report_id, session_id)
        #
        # QAP_5635.execute(report_id, session_id)
        # wrapper_test.execute(report_id,session_id)


        # QAP_5564_blocked_by_PFX_3932.execute(report_id,session_id)
        # for_test_77679.execute(report_id,session_id)
        # for_Daria.execute(report_id,session_id)
        # SendMD.execute(report_id)
        # QAP_3806.execute(report_id)

        # QAP_5591_blocked_by_PFX_3932.execute(report_id,session_id)


        # QAP_2326.execute(report_id, session_id)
        # QAP_568.execute(report_id, session_id)
        # QAP_5537.execute(report_id,session_id)
        # java_api.TestCase(report_id).execute()



        # QAP_2092WIP.execute(report_id,session_id)
        # QAP_1558.execute(report_id)
        # QAP_2290.execute(report_id,session_id)
        # QAP_2322.execute(report_id, session_id)

        DepositAndLoan.execute(report_id)
        # QAP_2251.execute(report_id)



        # SendMD.execute(report_id)
        #
        # QAP_5564_blocked_by_PFX_3932.execute(report_id,session_id)
        # QAP_5176.execute(report_id)
        # QAP_1518.execute(report_id)



        # rfq.execute(report_id)



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


        # rm = RuleManager()
        # rm.add_fx_md_to('fix-fh-q-314-luna')
        # rm.add_fx_md_to('fix-fh-309-kratos')
        # rm.print_active_rules()

        # rm.print_active_rules_sim_test()

        # rm.add_TRFQ('fix-bs-rfq-314-luna-standard')
        # rm.add_QuodMDAnswerRule('fix-fh-314-luna',interval=5)
        # rm.remove_rule_by_id(326)





        # rm.remove_rule_by_id(4)
        # rm.remove_rule_by_id(5)

        # rm.remove_rule_by_id(10)
        # rm.remove_rule_by_id_test_sim(4)
        # rm.remove_rule_by_id_test_sim(3)
        # # # rm.add_RFQ('fix-bs-rfq-314-luna-standard')
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



if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








