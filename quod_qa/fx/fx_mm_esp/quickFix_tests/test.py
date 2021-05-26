from quod_qa.fx.fx_mm_esp.common import requests
import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime




report_id = None
time_in_force='3'
req1=bca.client_orderid(10)
req2=bca.client_orderid(9)


qap_1520 = requests(md_req_id=req1,
                    cl_ord_id=req2,
                    time_in_force=time_in_force,
                    settl_date=(tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S'))
qap_1520.case_params.update()
a =qap_1520.settl_date=(tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d %H:%M:%S')












def execute(report_id):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Services setup
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    common_act = Stubs.win_act
    ob_act = Stubs.win_act_order_book

    # Case parameters setup
    case_id = bca.create_event('QAP_1518', report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    a = qap_1520.connectivity
    try:
        subscribe = fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                'Send MDR (subscribe)',
                qap_1520.connectivity,
                case_id,
                bca.message_to_grpc('MarketDataRequest', qap_1520.md_params, qap_1520.connectivity)
            ))




    except Exception as e:
            logging.error('Error execution', exc_info=True)

        # close_fe(self.case_id, self.session_id)


if __name__ == '__main__':
    pass

