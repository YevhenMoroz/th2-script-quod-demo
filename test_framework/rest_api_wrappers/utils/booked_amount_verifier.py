import logging
from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.utils.verifier import data_validation


def booked_amount_validation(test_id, event_name, booked_amount_current, booked_amount_simulated, reserved_qty_current):

    verification_event = bca.create_event(event_name, test_id)
    try:
        booked_amount_current_status_keys = booked_amount_current.keys()

        for key, _ in booked_amount_simulated.items():
            if key in booked_amount_current_status_keys:
                data_validation(test_id=verification_event,
                                event_name=f"{key} value calculation",
                                expected_result=booked_amount_simulated[key],
                                actual_result=float(booked_amount_current[key]))
        data_validation(test_id=verification_event,
                        event_name="ReservedQty value calculation",
                        expected_result=booked_amount_simulated['reservedQty'],
                        actual_result=float(reserved_qty_current['reservedQty']))
    except (KeyError, IndexError, TypeError):
        bca.create_event(f'Validation step for Booked Amount Calculation was failed', status='FAILED',
                         parent_id=verification_event)
        logging.error("Error parsing", exc_info=True)
