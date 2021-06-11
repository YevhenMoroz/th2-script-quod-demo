from pathlib import Path

from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from custom import basic_custom_actions as bca
import logging

from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
account = 'Palladium1_1'
side = '1'
orderqty = '1000000'
ordtype = '2'
timeinforce = '3'
currency = 'EUR'
settlcurrency = 'USD'
settltype = 0
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [2000000, 6000000, 12000000]
md = None
settldate = spo()
defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'


def check_trades_book(base_request, ob_act, case_id, exec_id, price):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["ExecID", exec_id])
    trades_price = ExtractionDetail("tradeBook.price", "ExecPrice")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[trades_price])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Trade Book")
    verifier.compare_values("Price", price, response[trades_price.name])
    verifier.verify()


def check_order_book(base_request, act_ob, case_id):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob_tif = ExtractionDetail("orderBook.tif", "TIF")
    exec_id = ExtractionDetail("executions.id", "ExecID")
    exec_price = ExtractionDetail("executions.price", "ExecPrice")

    exec_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[exec_id,
                                                                                                      exec_price]))
    exec_details = OrdersDetails.create(info=exec_info)

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_tif]),
            sub_order_details=exec_details))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Tif", "ImmediateOrCancel", response[ob_tif.name])
    verifier.verify()
    id_exec = response[exec_id.name]
    price = response[exec_price.name]
    return [id_exec, price]


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    ob_act = Stubs.win_act_order_book

    try:

        # Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate, symbol=symbol,
                                           securitytype=securitytype)). \
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)).send_market_data_spot()

        # Step 1-4
        params = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                   timeinforce=timeinforce, currency=currency,
                                   settlcurrency=settlcurrency, settltype=settltype, settldate=settldate, symbol=symbol,
                                   securitytype=securitytype,
                                   securityidsource=securityidsource, securityid=securityid, account=account)
        params.prepare_md_for_verification(bands)
        md = FixClientSellEsp(params).send_md_request().verify_md_pending()
        price = md.extruct_filed('Price')
        md.send_new_order_single(price). \
            verify_order_pending(). \
            verify_order_filled()

        # Step 5
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        order_info = check_order_book(case_base_request, ob_act, case_id)
        check_trades_book(case_base_request, ob_act, case_id, order_info[0], order_info[1])


    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()
