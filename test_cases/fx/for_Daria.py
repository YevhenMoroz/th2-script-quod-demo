import logging
import time
from pathlib import Path

from th2_grpc_act_gui_quod.act_ui_win_pb2 import VenueStatusesRequest
from th2_grpc_act_gui_quod.ar_operations_pb2 import ExtractOrderTicketValuesRequest, ExtractDirectVenueExecutionRequest

from custom.tenor_settlement_date import spo
from custom.verifier import Verifier, VerificationMethod
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from test_cases.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ExtractRatesTileTableValuesRequest, \
    ModifyRatesTileRequest
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, close_fe, prepare_fe303

api = Stubs.api_service
ob_act = Stubs.win_act_order_book
cp_service = Stubs.win_act_cp_service
pos_service = Stubs.act_fx_dealing_positions
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Osmium1'
client_tier = 'Osmium'
account_client = 'Osmium1_1'
side = '1'
ordtype = '2'
timeinforce = '4'
currency = 'EUR'
settle_currency = 'USD'
settle_type_spo = 0
symbol = 'EUR/USD'
security_type_spo = 'FXSPOT'
securityidsource = '8'
securityid = 'EUR/USD'
instrument_tier = 'EUR/USD-SPOT'
qty = 2000000
ordqty = 0
clOrdID = ''
ord_status = 'Filled'
status_open = 'Open'
status_cnld = 'Cancelled'
md = None
settle_date_spo = spo()


def set_send_hedge_order(status, case_id, algo_policy_id):
    modify_params = {
        "autoHedgerName": "OsmiumAH",
        "hedgeAccountGroupID": "QUOD3",
        "autoHedgerID": 1400008,
        "alive": "true",
        "hedgedAccountGroup": [
            {
                "accountGroupID": "Osmium1"
            }
        ],
        "autoHedgerInstrSymbol": [
            {
                "instrSymbol": "EUR/USD",
                "longUpperQty": 2000000,
                "longLowerQty": 0,
                "maintainHedgePositions": "true",
                "crossCurrPairHedgingPolicy": "DIR",
                "useSameLongShortQty": "true",
                "hedgingStrategy": "POS",
                "algoPolicyID": algo_policy_id,
                "shortLowerQty": 0,
                "shortUpperQty": 0,
                "timeInForce": "DAY",
                "sendHedgeOrders": status,
                "exposureDuration": 120,
                "hedgeOrderDestination": "EXT"
            }
        ]
    }
    print('ModifyAutoHedger message is sent by REST API')
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyAutoHedger', modify_params, 'rest_wa314luna'),
                                     parent_event_id=case_id))


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instrument)
    call(service.modifyRatesTile, modify_request.build())


def get_dealing_positions_details(del_act, base_request, symbol, account, value):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", value)
    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return float(response["dealingpositions.position"].replace(",", ""))


def compare_position(even_name, case_id, expected_pos, actual_pos):
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values("Quote position", str(float(expected_pos)), str(actual_pos))

    verifier.verify()


def check_order_book(even_name, case_id, base_request, act_ob, threshold, status_exp):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'OK', "Orig", 'AutoHedger', "Strategy", "test"])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', str(threshold), response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])

    verifier.verify()
    return response[order_id.name]


def verify_auto_hedger(case_id, order_id_before, order_id_after):
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Auto Hedger order")
    verifier.compare_values('Order ID', order_id_before, order_id_after)
    verifier.verify()


def execute(report_id, session_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        case_base_request = get_base_request(session_id, case_id)
        base_details = BaseTileDetails(base=case_base_request)

        try:
            # Preconditions





            check_order_book("Check AH is in Order book with OPEN Status", case_id, case_base_request, ob_act,
                             qty, status_open)
            actual_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client, "Position")






        except Exception as e:
            logging.error('Error execution', exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
        finally:
            pass

    except Exception as e:
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
        logging.error('Error execution', exc_info=True)
