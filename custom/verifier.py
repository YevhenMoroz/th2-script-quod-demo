import json
from enum import Enum

from google.protobuf.timestamp_pb2 import Timestamp
from th2_grpc_common.common_pb2 import EventID, Event, EventBatch

from custom.basic_custom_actions import timestamps, create_event_id
from stubs import Stubs


class VerificationMethod(Enum):
    EQUALS = "EQUAL"
    NOT_EQUALS = "NOT EQUAL"
    CONTAINS = "CONTAINS"


class Verifier:
    def __init__(self, parent_id: EventID = None):
        self.parent_id = parent_id
        self.event_name = None
        self.success = True
        self.result = dict()
        self.fields = dict()

    def set_parent_id(self, parent_id: EventID):
        self.parent_id = parent_id

    def set_event_name(self, event_name: str):
        self.event_name = event_name

    def compare_values(self, printed_name: str, expected_value: str, actual_value: str,
                       verification_method: VerificationMethod = VerificationMethod.EQUALS):
        if verification_method in VerificationMethod.EQUALS:
            passed = expected_value == actual_value
        elif verification_method in VerificationMethod.NOT_EQUALS:
            passed = expected_value != actual_value
        elif verification_method in VerificationMethod.CONTAINS:
            passed = expected_value in actual_value
        else:
            raise Exception("Unexpected verification method")

        self.fields.update(
            {
                printed_name:
                    {
                        "expected": expected_value,
                        "actual": actual_value,
                        "key": False,
                        "type": "field",
                        "operation": verification_method.value,
                        "status": "PASSED" if passed else "FAILED"
                    }
            })
        self.success &= passed

    def _build_json(self) -> list:
        return [
            {
                "fields": self.fields,
                "type": "verification"
            }
        ]

    def verify(self):
        event_store = Stubs.event_store
        seconds, nanos = timestamps()
        event = Event(
            id=create_event_id(),
            name=self.event_name,
            status="SUCCESS" if self.success else "FAILED",
            body=bytes(json.dumps(self._build_json()), 'utf-8'),
            start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
            parent_id=self.parent_id)
        event_batch = EventBatch()
        event_batch.events.append(event)
        event_store.send(event_batch)

