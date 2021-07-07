import logging
import math
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.common_tools import round_decimals_up, round_decimals_down
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest, ExtractRatesTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from datetime import datetime, timedelta


def create_or_get_pricing_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_pricing_tile(base_request, service, instrument, client):
    from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def create_band_dict(expected_bands: tuple, actual_bands: list):
    expected_bands_iterator = iter(expected_bands)
    result_dict = {}
    for act_band in actual_bands:
        exp_band = next(expected_bands_iterator)
        result_dict.update({exp_band: act_band})
    return result_dict


def extract_column_band(base_request, service, row_id):
    from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row_id)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidBand", "Band"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askBand", "Band"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    return response


def check_band_on_pricing_tile(case_id, band_dict: dict, event_name):
    verifier = Verifier(case_id)
    verifier.set_event_name(event_name)
    for expected_band, actual_band in band_dict.items():
        verifier.compare_values(f"Bid Band {expected_band}", expected_band, actual_band.get('rateTile.bidBand'))
        verifier.compare_values(f"Ask Band {expected_band}", expected_band, actual_band.get('rateTile.askBand'))
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    start = datetime.now()
    case_id = bca.create_event(case_name, report_id)
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    case_base_request = get_base_request(session_id=session_id, event_id=case_id)
    base_details = BaseTileDetails(base=case_base_request)

    # Instrument setup
    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    instrument = from_curr + '/' + to_curr + '-' + tenor

    # Expected bands
    expected_band_palladium1 = ('2M', '6M', '12M')
    expected_band_palladium2 = ('1M', '5M', '10M')

    # Actual bands
    actual_band_palladium1 = []
    actual_band_palladium2 = []

    # Tiers
    tier_palladium1 = 'Palladium1'
    tier_palladium2 = 'Palladium2'

    try:

        # Step 1 Open CP rates tile

        create_or_get_pricing_tile(base_details, cp_service)

        # Step 2 Extracting Bands for the first tier

        modify_pricing_tile(base_details, cp_service, instrument, tier_palladium1)
        for i in range(len(expected_band_palladium1)):
            actual_band_palladium1.append(extract_column_band(base_details, cp_service, i + 1))

        # Step 3 Extracting bands for the second tier

        modify_pricing_tile(base_details, cp_service, instrument, tier_palladium2)
        for i in range(len(expected_band_palladium2)):
            actual_band_palladium2.append(extract_column_band(base_details, cp_service, i + 1))

        # Step 4 Checking the equality of the expected and actual bands

        palladium1_bands = create_band_dict(expected_band_palladium1, actual_band_palladium1)
        palladium2_bands = create_band_dict(expected_band_palladium2, actual_band_palladium2)

        check_band_on_pricing_tile(case_id, palladium1_bands, 'Checking Palladium1 bands')
        check_band_on_pricing_tile(case_id, palladium2_bands, 'Checking Palladium2 bands')

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tiles
            print(f'{case_name} duration time = ' + str(datetime.now() - start))
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
