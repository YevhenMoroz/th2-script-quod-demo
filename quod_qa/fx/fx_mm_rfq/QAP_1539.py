import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.MarketDataRequst import MarketDataRequst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Iridium1'
settltype = '0'
symbol = 'EUR/USD'
currency = 'EUR'
securitytype = 'FXSPOT'
securityidsource = '8'
side = '1'
orderqty = '1000000'
securityid = 'EUR/USD'
bands = [1000000]
md = None
settldate = tsd.spo()
ExpireTime = (datetime.now() + timedelta(seconds=120)).strftime("%Y%m%d-%H:%M:%S.000"),
TransactTime = (datetime.utcnow().isoformat())
defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)

        # Preconditions
        params_sell = CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate,
                                        symbol=symbol, securitytype=securitytype)
        FixClientSellEsp(params_sell).send_md_request().send_md_unsubscribe()
        # Send market data to the HSBC venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)). \
            send_market_data_spot()

        # Step 1-5
        params = CaseParamsSellRfq(client, case_id, side=side, orderqty=orderqty, symbol=symbol,
                                   securitytype=securitytype,
                                   settldate=settldate, settltype=settltype, currency=currency)

        FixClientSellRfq(params). \
            send_request_for_quote(). \
            verify_quote_pending(). \
            send_quote_cancel(). \
            verify_quote_cancel()

    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
