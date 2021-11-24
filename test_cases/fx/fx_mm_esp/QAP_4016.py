from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom.verifier import Verifier, VerificationMethod
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ModifyRatesTileRequest as ModifyMM, \
     ModifyRatesTileRequest
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest as ModifyESP, ContextActionRatesTile, \
     ActionsRatesTile
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest, DeselectRowsRequest

api = Stubs.api_service

md_entry = [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19655,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19979,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18900,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19989,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18400,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19998,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                }
            ]

def_md_symbol_eur_gbp = "USD/RUB:SPO:REG:HSBC"
symbol_eur_gbp = "USD/RUB"
from_currency = 'USD'
to_currency = 'RUB'
tenor = 'Spot'
instrument = 'USD/RUB-Spot'
client_tier = 'Palladium2'
venue = 'HSB'
rows_default = 3
rows_with_new_md = 4
rows_for_2m = 2
rows_for_tiered = 2
ask_pts_exp = 998
bid_pts_exp = 8400
margin_ask_pts_exp = 991
margin_bid_pts_exp = 8898
unconfigured_ask_pts_exp = 998
unconfigured_bid_pts_exp = 949
exp_px_1st_band_bid = 655
exp_px_1st_band_ask = 979

# region Test params
modify_params = {
        "instrSymbol": "USD/RUB",
        "quoteTTL": 120,
        "clientTierID": 2000011,
        "alive": "true",
        'pricingMethod': '',
        "clientTierInstrSymbolQty": '',
        "clientTierInstrSymbolTenor": [
            {
                "tenor": "SPO",
                "minSpread": None,
                "maxSpread": '',
                "marginPriceType": "PIP",
                "lastUpdateTime": '',
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "clientTierInstrSymbolTenorQty": [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 1,
                        'defaultBidMargin': None,
                        'defaultOfferMargin': None,
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 2,
                        'defaultBidMargin': None,
                        'defaultOfferMargin': None,
                    }
                ]
            }
        ],
        "clientTierInstrSymbolVenue": [
            {
                "venueID": "HSBC"
            }
        ],
        "clientTierInstrSymbolActGrp": [
            {
                "accountGroupID": "Palladium2"
            }
        ],
        "clientTierInstrSymbolFwdVenue": [
            {
                "venueID": "HSBC"
            },
            {
                "venueID": "HSBCR"
            }
        ],
        'clientTierInstrSymbolTieredQty': ''
    }
tiered_qty_2m_4m = [
    {'upperQty': 2000000},
    {'upperQty': 4000000}
]
tiered_qty_null = None
tenor_qty = [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 1,
                        'defaultBidMargin': None,
                        'defaultOfferMargin': None,
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 2,
                        'defaultBidMargin': None,
                        'defaultOfferMargin': None,
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 3,
                        'defaultBidMargin': None,
                        'defaultOfferMargin': None,
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 4,
                        'defaultBidMargin': None,
                        'defaultOfferMargin': None,
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 5,
                        'defaultBidMargin': None,
                        'defaultOfferMargin': None,
                    }
                ]
case_sweepable_qty = [
            {
                "upperQty": 1000000,
                "indiceUpperQty": 1,
                "publishPrices": "true"
            },
            {
                "upperQty": 2000000,
                "indiceUpperQty": 2,
                "publishPrices": "true"
            },
            {
                "upperQty": 3000000,
                "indiceUpperQty": 3,
                "publishPrices": "true"
            },
            {
                "upperQty": 4000000,
                "indiceUpperQty": 4,
                "publishPrices": "true"
            },
            {
                "upperQty": 5000000,
                "indiceUpperQty": 5,
                "publishPrices": "true"
            }
        ]
null_pricing_method = None
test_pricing_method = 'DIR'
null_spread = None
test_spread = '150'
null_margin = None
test_margin = '0.2'
exp_effective_margin = '-4.9'
tiered_band_exp = '4M'
additional_rows = [4, 5]
# endregion


def set_instrument(case_id, pricing_method, max_spread, margin, tiered_qty, sweepable_qty, tenor_qty):
    timestamp = str(datetime.now().timestamp())
    timestamp = timestamp.split(".", 1)
    timestamp = timestamp[0]
    modify_params['pricingMethod'] = pricing_method
    modify_params['clientTierInstrSymbolTieredQty'] = tiered_qty
    modify_params['clientTierInstrSymbolQty'] = sweepable_qty
    modify_params['clientTierInstrSymbolTenor'][0]['clientTierInstrSymbolTenorQty'] = tenor_qty
    modify_params['clientTierInstrSymbolTenor'][0]['lastUpdateTime'] = timestamp
    modify_params['clientTierInstrSymbolTenor'][0]['clientTierInstrSymbolTenorQty'][1]['defaultBidMargin'] = margin
    modify_params['clientTierInstrSymbolTenor'][0]['clientTierInstrSymbolTenorQty'][1]['defaultOfferMargin'] = margin
    modify_params['clientTierInstrSymbolTenor'][0]['maxSpread'] = max_spread
    api.sendMessage(
        request=SubmitMessageRequest(
            message=bca.wrap_message(modify_params, 'ModifyClientTierInstrSymbol', 'rest_wa314luna'),
            parent_event_id=case_id))


def set_only_one_band(case_id, pricing_method, max_spread, tiered_qty, sweepable_qty, tenor_qty):
    timestamp = str(datetime.now().timestamp())
    timestamp = timestamp.split(".", 1)
    timestamp = timestamp[0]
    modify_params['pricingMethod'] = pricing_method
    modify_params['clientTierInstrSymbolTieredQty'] = tiered_qty
    modify_params['clientTierInstrSymbolQty'] = sweepable_qty
    modify_params['clientTierInstrSymbolTenor'][0]['clientTierInstrSymbolTenorQty'] = tenor_qty
    modify_params['clientTierInstrSymbolTenor'][0]['lastUpdateTime'] = timestamp
    modify_params['clientTierInstrSymbolTenor'][0]['maxSpread'] = max_spread
    api.sendMessage(
        request=SubmitMessageRequest(
            message=bca.wrap_message(modify_params, 'ModifyClientTierInstrSymbol', 'rest_wa314luna'),
            parent_event_id=case_id))


def modify_cp_rates_tile(base_request, service, instr, client):
    modify_request = ModifyMM(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instr)
    call(service.modifyRatesTile, modify_request.build())


def modify_agg_rates_tile(base_request, service, from_c, to_c, ten):
    modify_request = ModifyESP(details=base_request)
    modify_request.set_instrument(from_c, to_c, ten)
    call(service.modifyRatesTile, modify_request.build())


def open_direct_venue(base_request, service, ven):
    modify_request = ModifyESP(details=base_request)
    venue_filter = ContextActionRatesTile.create_venue_filter(ven)
    add_dve_action = ContextActionRatesTile.open_direct_venue_panel()
    modify_request.add_context_actions([venue_filter, add_dve_action])
    call(service.modifyRatesTile, modify_request.build())


def add_venue_rows(base_request, service, ven):
    modify_request = ModifyESP(details=base_request)
    add_row = ActionsRatesTile().click_to_direct_venue_add_raw(ven)
    modify_request.add_actions([add_row, add_row, add_row, add_row, add_row])
    call(service.modifyRatesTile, modify_request.build())


def extract_pts_and_band(base_request, service, rows: int):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(rows)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidBase", "Base"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askBase", "Base"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidPx", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askPx", "Px"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("askEffectiveMargin", "+"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidEffectiveMargin", "-"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    deselect_rows_request = DeselectRowsRequest(details=base_request)
    call(service.deselectRows, deselect_rows_request.build())
    return [response['askPx'], response['bidPx'], response['bidBase'],
            response['bidEffectiveMargin'], response['askEffectiveMargin']]


def extract_tiered_pub_and_px(base_request, service, rows: int):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(rows)
    extract_table_request.is_tiered(True)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidPub", "Pub"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askPub", "Pub"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidPx", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askPx", "Px"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    return [response['askPx'], response['bidPx'], response['bidPub']]


def check_additional_band(base_request, case_id, service, rows: [int]):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    for i in rows:
        extract_table_request.set_row_number(i)
        extract_table_request.set_bid_extraction_field(ExtractionDetail("bidBand", "Band"))
        extract_table_request.set_ask_extraction_field(ExtractionDetail("askBand", "Band"))
        extract_table_request.set_bid_extraction_field(ExtractionDetail("bidPx", "Px"))
        extract_table_request.set_ask_extraction_field(ExtractionDetail("askPx", "Px"))
        response = call(service.extractRatesTileTableValues, extract_table_request.build())
        deselect_rows_request = DeselectRowsRequest(details=base_request)
        call(service.deselectRows, deselect_rows_request.build())
        verifier = Verifier(case_id)
        verifier.set_event_name(f'Checking that additional bands presented {i-3}')
        verifier.compare_values('askBand', 'NOT NULL', str(response['bidBand']), VerificationMethod.NOT_EQUALS)
        verifier.compare_values('bidBand', 'NOT NULL', str(response['askBand']), VerificationMethod.NOT_EQUALS)
        verifier.compare_values('askPx', '', str(response['askPx']))
        verifier.compare_values('bidPx', '', str(response['bidPx']))
        verifier.verify()


def extract_row(base_request, service, row):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidBand", "Band"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askBand", "Band"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidPx", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askPx", "Px"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    deselect_rows_request = DeselectRowsRequest(details=base_request)
    call(service.deselectRows, deselect_rows_request.build())
    return [response["askPx"], response["bidPx"], response["bidBand"]]


def check_only_one_band(base_request, case_id, service):
    first_band_values = extract_row(base_request, service, 1)
    second_band_values = extract_row(base_request, service, 2)
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking that only first band')
    verifier.compare_values('Configured band', '1M', first_band_values[2])
    verifier.compare_values('Configured askPx', '979', first_band_values[0])
    verifier.compare_values('Configured bidPx', '655', first_band_values[1])
    verifier.compare_values('Unconfigured band', '0', second_band_values[2])
    verifier.compare_values('Unconfigured askPx', '989', second_band_values[0])
    verifier.compare_values('Unconfigured bidPx', '8900', second_band_values[1])
    verifier.verify()


def check_tiered(case_id, pub_exp, ask_act, bid_act, pub_act):
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking that tiered Qty`s presented and pricing')
    verifier.compare_values('askPx', '', str(ask_act), VerificationMethod.NOT_EQUALS)
    verifier.compare_values('bidPx', '', str(bid_act), VerificationMethod.NOT_EQUALS)
    verifier.compare_values('Pub', pub_exp, pub_act)
    verifier.verify()


def check_effective_margin(case_id, expected, ask_act, bid_act, event_name):
    verifier = Verifier(case_id)
    verifier.set_event_name(event_name)
    verifier.compare_values('ask', expected, str(ask_act))
    verifier.compare_values('bid', expected, str(bid_act))
    verifier.verify()


def check_pts(case_id, ask_exp, bid_exp, ask_act, bid_act, base, expected_margins, event_name):
    verifier = Verifier(case_id)
    verifier.set_event_name(event_name)
    verifier.compare_values('ask', str(ask_exp), str(ask_act))
    verifier.compare_values('bid', str(bid_exp), str(bid_act))
    verifier.compare_values('Base', expected_margins, base)
    verifier.verify()


def switch_to_tired(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.toggle_tiered()
    call(service.modifyRatesTile, modify_request.build())


def switch_to_sweepable(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.toggle_sweepable()
    call(service.modifyRatesTile, modify_request.build())


def use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def execute(report_id, session_id):
    #
    # TODO: Add extraction from Taker ESP tile
    #
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_details = BaseTileDetails(base=case_base_request)
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    ar_service = Stubs.win_act_aggregated_rates_service
    pos_service = Stubs.act_fx_dealing_positions
    try:
        call(cp_service.createRatesTile, base_details.build())
        call(ar_service.createRatesTile, base_details.build())
        # Step 1
        set_instrument(case_id, test_pricing_method, null_spread, null_margin, tiered_qty_null,
                       case_sweepable_qty[:2], tenor_qty[:2])

        modify_cp_rates_tile(base_details, cp_service, instrument, client_tier)
        modify_agg_rates_tile(base_details, ar_service, from_currency, to_currency, tenor)
        open_direct_venue(base_details, ar_service, venue)
        add_venue_rows(base_details, ar_service, venue)

        FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_eur_gbp, symbol_eur_gbp).prepare_custom_md_spot(
            md_entry)).send_market_data_spot()
        result = extract_pts_and_band(base_details, cp_service, rows_default)
        check_pts(case_id, ask_pts_exp, bid_pts_exp, result[0], result[1], result[2], '',
                  'Checking that here are 3 rows,no base for 3d row')

        # Step 2
        set_instrument(case_id, test_pricing_method, null_spread, test_margin, tiered_qty_null,
                       case_sweepable_qty[:2], tenor_qty[:2])
        result = extract_pts_and_band(base_details, cp_service, rows_for_2m)
        check_pts(case_id, margin_ask_pts_exp, margin_bid_pts_exp, result[0], result[1], result[2], test_margin,
                  'Checking margins applied for 2nd band')
        result = extract_pts_and_band(base_details, cp_service, rows_default)
        check_pts(case_id, ask_pts_exp, bid_pts_exp, result[0], result[1], result[2], '',
                  'Checking that there is no margin for 3d band')
        # Step 3
        set_instrument(case_id, test_pricing_method, test_spread, test_margin, tiered_qty_null,
                       case_sweepable_qty[:2], tenor_qty[:2])
        result = extract_pts_and_band(base_details, cp_service, rows_default)
        check_effective_margin(case_id, exp_effective_margin, result[3], result[4], 'Checking effective margins')

        # Step 4
        set_instrument(case_id, test_pricing_method, test_spread, test_margin, tiered_qty_2m_4m,
                       case_sweepable_qty[:2], tenor_qty[:2])
        switch_to_tired(base_details, cp_service)
        result = extract_tiered_pub_and_px(base_details, cp_service, rows_for_tiered)
        check_tiered(case_id, tiered_band_exp, result[0], result[1], result[2])
        switch_to_sweepable(base_details, cp_service)

        # Step 5
        set_instrument(case_id, test_pricing_method, test_spread, test_margin, tiered_qty_2m_4m,
                       case_sweepable_qty, tenor_qty)
        use_default(base_details, cp_service)
        check_additional_band(base_details, case_id, cp_service, [4, 5])

        # Step 6
        set_only_one_band(case_id, test_pricing_method, test_spread, tiered_qty_2m_4m,
                          case_sweepable_qty[:1], tenor_qty[:1])
        check_only_one_band(base_details, case_id, cp_service)
    except Exception as ex:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
            call(ar_service.closeRatesTile, base_details.build())
            # Set default parameters
            set_instrument(case_id, null_pricing_method, null_spread, null_margin, tiered_qty_null,
                           case_sweepable_qty[:2], tenor_qty[:2])
        except Exception:
            logging.error("Error execution", exc_info=True)
