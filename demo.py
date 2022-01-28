import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from rule_management import RuleManager

from stubs import Stubs
from test_cases.fx.fx_mm_rfq.interpolation import QAP_4234, QAP_3851, QAP_3850, QAP_3807, QAP_3747
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_6571 import QAP_6571
from test_cases.fx.fx_taker_esp import QAP_5635, QAP_5537, QAP_5564, QAP_5589, QAP_5591, QAP_5598, QAP_5600
from test_cases.fx.qs_fx_routine import SendMD, rfq, DepositAndLoan, esp, rfq_swap_1w_2w
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
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

    data_set = FxDataSet()

    session_id=set_session_id()
    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe_2(report_id, session_id)
        # else:
        #     get_opened_fe(report_id, session_id)
        #
        # QAP_6571(report_id=report_id, session_id=session_id, data_set=data_set).execute()
        # QAP_2290.execute(report_id, session_id)

        # QAP_3747.execute(report_id)
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

        # DepositAndLoan.execute(report_id)
        # QAP_2251.execute(report_id)



        # SendMD.execute(report_id)

        # rfq.execute(report_id)
        # esp.execute(report_id)
        # rfq_swap_1w_2w.execute(report_id)



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

        #____________________________RULES________________________________________________
        rm = RuleManager()
        rm.add_fx_md_to('fix-fh-314-luna')
        # rm.add_fx_md_to('fix-fh-q-314-luna')
        # rm.add_fx_md_to('fix-fh-309-kratos')
        # Rule to update Quod with MD which we store in map  QuodMDUpdateFXRule
        # rm.add_QuodMDUpdateFXRule('fix-fh-314-luna', 3)
        # rm.add_QuodMDUpdateFXRule('fix-fh-309-kratos', 2)
        # rm.add_QuodMDAnswerRule('fix-fh-314-luna',interval=2)
        # rm.add_QuodMDAnswerRule('fix-fh-309-kratos',interval=1)
        # rm.add_fx_md_to('fix-fh-309-kratos')
        # rm.add_TRFQ('fix-bs-rfq-314-luna-standard')
        # rm.add_TRFQ('fix-bs-rfq-309-kratos-stand')
        # rm.add_RFQ('fix-bs-rfq-314-luna-standard')
        # rm.add_RFQ('fix-bs-rfq-309-kratos-stand')
        # rm.add_TRADE_ESP('fix-bs-esp-314-luna-standard')
        # rm.add_TRADE_ESP('fix-bs-esp-309-kratos-stand')


        # rm.print_active_rules()
        rm.remove_rule_by_id(15)



        # rm.print_active_rules_sim_test()
        # rm.remove_rule_by_id_test_sim(2)
        rm.print_active_rules()










    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)



if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()








