from custom import basic_custom_actions as bca
from custom.verifier import Verifier


def data_validation(test_id, event_name, expected_result, actual_result):
    try:
        verifier = Verifier(test_id)
        verifier.set_event_name(event_name)
        verifier.compare_values(event_name, expected_result, actual_result)
        verifier.verify()
    except (KeyError, IndexError, TypeError):
        bca.create_event(f'Validation step was failed - {event_name}', status='FAILED', parent_id=test_id)
