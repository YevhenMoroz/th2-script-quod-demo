from datetime import datetime
from logging import getLogger, INFO

from custom.basic_custom_actions import timestamps, create_event
from custom.verifier import Verifier, VerificationMethod
from win_gui_modules.utils import set_session_id
from win_gui_modules.wrappers import *

logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()
    case_name = "Verifier example"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    try:
        verifier = Verifier(case_id)
        verifier.set_event_name("Test verification")
        verifier.compare_values("Param0", "A", "A")
        verifier.compare_values("Param1", "B", "B")
        verifier.compare_values("Param2", "A", "B", VerificationMethod.NOT_EQUALS)
        verifier.compare_values("Param3", "B", "AAB", VerificationMethod.CONTAINS)
        verifier.verify()

    except Exception:
        logger.error("Error execution", exc_info=True)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
