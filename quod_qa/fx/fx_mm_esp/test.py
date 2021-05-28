import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from quod_qa.fx.fx_wrapper.CaseParams import CaseParams
from quod_qa.fx.fx_wrapper.MarketDataRequst import MarketDataRequst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium2'
connectivity = 'fix-ss-esp-314-luna-standard'
settltype = '0'
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [1000000, 5000000, 10000000]
md = None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=23)).date().strftime('%Y%m%d %H:%M:%S')



def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        simulator = Stubs.simulator
        act = Stubs.fix_act

        params = CaseParams(connectivity, client, case_id, settltype=settltype, settldate=settldate,
                            symbol=symbol, securitytype=securitytype, securityidsource=securityidsource,
                            securityid=securityid)
        # md = MarketDataRequst(params). \
        #     set_md_params() \
        #     .send_md_request() \
        #     .prepare_md_response(bands)
        # md.verify_md_pending()

        md = MarketDataRequst(params)
        md.set_md_params()
        md.send_md_request_timeout()
        md.prepare_md_response()
        md.verify_md_pending()

        md.CheckMarketDataSequence()
        price1 = md.extruct_filed('price')
        md.send_md_unsubscribe()







    except Exception as e:
        logging.error('Error execution', exc_info=True)

    finally:
        md.send_md_unsubscribe()
    pass
