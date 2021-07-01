from datetime import datetime
from custom import tenor_settlement_date as tsd
from datetime import datetime, timedelta
from custom.tenor_settlement_date import wk1_front_end

import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction

from win_gui_modules.utils import prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def get_dealing_positions_details(del_act, base_request, symbol, account, date):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])

    sub_settle_date = ExtractionPositionsFieldsDetails("sub_positions.settldate", "Settle Date")
    sub_position = ExtractionPositionsFieldsDetails("sub_positions.position", "Position")
    lvl1_info = PositionsInfo.create(
        action=ExtractionPositionsAction.create_extraction_action(
            extraction_details=[sub_settle_date, sub_position]))
    lvl1_details = GetOrdersDetailsRequest.create(info=lvl1_info)
    lvl1_details.set_filter(["Settle Date", date])

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(),
            positions_by_currency=lvl1_details))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    print(response[sub_position.value])
    return float(response[sub_position.value].replace(",", ""))


def compare_position(case_id, pos_before, position, pos_after):
    expected_pos = pos_before + position

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare position")
    verifier.compare_values("Quote position", str(round(expected_pos, 2)), str(pos_after))

    verifier.verify()

#Preconditions
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Silver1'
account = 'Silver1_1'
settltype = 'W1'
symbol = 'EUR/USD'
currency = 'EUR'
securitytype = 'FXFWD'
securityidsource = '8'
side = '1'
orderqty = '1000000'
securityid = 'EUR/USD'
bands = [1000000]
settldate = tsd.wk1()
ExpireTime = (datetime.now() + timedelta(seconds=120)).strftime("%Y%m%d-%H:%M:%S.000"),
TransactTime = (datetime.utcnow().isoformat())






def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    pos_service = Stubs.act_fx_dealing_positions

    case_name = Path(__file__).name[:-3]
    client = "ASPECT_CITI"
    from_currency = "GBP"
    to_currency = "USD"
    near_tenor = "Spot"
    orderqty = 1000000
    symbol = from_currency + "/" + to_currency
    date_wk1 = wk1_front_end()
    date_wk1 = datetime.strptime(date_wk1, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)
    try:
        # Step 1
        pos_before = get_dealing_positions_details(pos_service, case_base_request, symbol, client, date_wk1)

        #Send rfq
        rfq= FixClientSellRfq(CaseParamsSellRfq(client, case_id, side=side, orderqty=orderqty, symbol=symbol,securitytype=securitytype,settldate=settldate,
                                           settltype=settltype, currency=currency,account=account)).\
            send_request_for_quote().\
            verify_quote_pending()
        price = rfq.extruct_filed('OfferPx')
        rfq.send_new_order_single(price).\
            verify_order_pending().\
            verify_order_filled_fwd()


        position = orderqty
        position_after = get_dealing_positions_details(pos_service, case_base_request, symbol, client, date_wk1)
        compare_position(case_id, pos_before, position, position_after)

    except Exception:
        logging.error("Error execution", exc_info=True)
