import copy
import time
import uuid
from datetime import datetime

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from grpc_modules import act_fix_pb2
from grpc_modules import act_fix_pb2_grpc
from grpc_modules import event_store_pb2
from grpc_modules import infra_pb2
from grpc_modules import verifier_pb2

# Debug output
PrintMessages = False


class ActComponentCall:
    def __init__(self, address):
        self.address = address

    def __enter__(self):
        self.channel = grpc.insecure_channel(self.address)
        self.act = act_fix_pb2_grpc.ActStub(self.channel)
        return self.act

    def __exit__(self, exception_type, exception_value, traceback):
        grpc.insecure_channel(self.address).close()


def timestamps():
    report_start_time = datetime.now()
    seconds = int(report_start_time.timestamp())
    nanos = int(report_start_time.microsecond * 1000)
    return seconds, nanos


def client_orderid(length):
    return str(uuid.uuid1().time)[-length:]


def message_to_grpc(message_type, content):
    content = copy.deepcopy(content)
    for tag in content:
        if isinstance(content[tag], (str, int, float)):
            content[tag] = infra_pb2.Value(simple_value=str(content[tag]))
        elif isinstance(content[tag], dict):
            content[tag] = infra_pb2.Value(message_value=(message_to_grpc(tag, content[tag])))
        elif isinstance(content[tag], list):
            for group in content[tag]:
                # content[tag][content[tag].index(group)] = infra_pb2.Value(message_value=(message_to_grpc(tag, group)))
                content[tag][content[tag].index(group)] = infra_pb2.Value(message_value=(message_to_grpc(tag + '_' + tag + 'IDs', group)))
            content[tag] = infra_pb2.Value(
                message_value=infra_pb2.Message(
                    metadata=infra_pb2.MessageMetadata(
                        message_type=tag
                    ),
                    fields={
                        tag: infra_pb2.Value(
                            list_value=infra_pb2.ListValue(
                                values=content[tag]
                            )
                        )
                    }
                )
            )
    return infra_pb2.Message(
            metadata=infra_pb2.MessageMetadata(
                message_type=message_type
            ),
            fields=content
        )


def filter_to_grpc(message_type, content, keys=None):
    if keys is None:
        keys = ['ClOrdID']
    content = copy.deepcopy(content)
    for tag in content:
        if isinstance(content[tag], (str, int, float)):
            if content[tag] == '*':
                content[tag] = infra_pb2.ValueFilter(operation=infra_pb2.FilterOperation.NOT_EMPTY)
            elif content[tag] == '#':
                content[tag] = infra_pb2.ValueFilter(operation=infra_pb2.FilterOperation.EMPTY)
            else:
                content[tag] = infra_pb2.ValueFilter(simple_filter=str(content[tag]), key=(True if tag in keys else False))

        # if isinstance(content[tag], (str, int, float)):
        #     content[tag] = infra_pb2.ValueFilter(simple_filter=str(content[tag]))
        elif isinstance(content[tag], dict):
            content[tag] = infra_pb2.ValueFilter(message_filter=(filter_to_grpc(tag, content[tag], keys)))
        elif isinstance(content[tag], list):
            for group in content[tag]:
                content[tag][content[tag].index(group)] = infra_pb2.ValueFilter(
                    message_filter=filter_to_grpc(tag, group)
                )
            content[tag] = infra_pb2.ValueFilter(
                list_filter=infra_pb2.ListValueFilter(
                    values=content[tag]
                )
            )
    return infra_pb2.MessageFilter(
        messageType=message_type,
        fields=content
    )


def convert_to_request(description, connectivity, event_id, message, key_fields=None):
    connectivity = infra_pb2.ConnectionID(session_alias=connectivity)
    return act_fix_pb2.PlaceMessageRequest(
        message=message,
        connection_id=connectivity,
        parent_event_id=event_id,
        description=description,
        key_fields=key_fields
    )


def verify_response(verifier, description, filter, act_response, connectivity, event_id):
    connectivity = infra_pb2.ConnectionID(session_alias=connectivity)
    rule_request = verifier_pb2.CheckRuleRequest(
        connectivity_id=connectivity,
        filter=filter,
        checkpoint=act_response.checkpoint_id,
        timeout=3000,
        parent_event_id=event_id,
        description=description
    )
    if PrintMessages:
        print(rule_request)
    return verifier.submitCheckRule(rule_request)


def verify_sequence(verifier, description, prefilter, msg_filters, checkpoint, connectivity,
                    event_id, check_order=True, timeout=3000):
    connectivity = infra_pb2.ConnectionID(session_alias=connectivity)
    sequence_rule = verifier_pb2.CheckSequenceRuleRequest(
        connectivity_id=connectivity,
        pre_filter=prefilter,
        message_filters=msg_filters,
        checkpoint=checkpoint,
        timeout=timeout,
        parent_event_id=event_id,
        description=description,
        check_order=check_order
    )
    return verifier.submitCheckSequenceRule(sequence_rule)


def create_check_rule(description, filter, checkpoint, connectivity, event_id, timeout=3000):
    return verifier_pb2.CheckRuleRequest(
        connectivity_id=infra_pb2.ConnectionID(session_alias=connectivity),
        filter=filter,
        checkpoint=checkpoint,
        timeout=timeout,
        parent_event_id=event_id,
        description=description
    )


def create_check_sequence_rule(description, prefilter, msg_filters, checkpoint, connectivity,
                               event_id, check_order=True, timeout=3000):
    return verifier_pb2.CheckSequenceRuleRequest(
        connectivity_id=infra_pb2.ConnectionID(session_alias=connectivity),
        pre_filter=prefilter,
        message_filters=msg_filters,
        checkpoint=checkpoint,
        timeout=timeout,
        parent_event_id=event_id,
        description=description,
        check_order=check_order
    )


def create_event_id():
    return infra_pb2.EventID(id=str(uuid.uuid1()))


def create_event(event_store, event_name, event_id, parent_id=None):
    seconds, nanos = timestamps()
    event = infra_pb2.Event(
        id=event_id,
        name=event_name,
        start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        # end_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        parent_id=parent_id)
    return event_store.StoreEvent(event_store_pb2.StoreEventRequest(event=event))


def create_store_event_request(event_name, event_id, parent_id=None):
    seconds, nanos = timestamps()
    event = infra_pb2.Event(
        id=event_id,
        name=event_name,
        start_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        # end_timestamp=Timestamp(seconds=seconds, nanos=nanos),
        parent_id=parent_id
    )
    return event_store_pb2.StoreEventRequest(event=event)


def create_sub_filter(fields):
    fields = copy.deepcopy(fields)
    for field in fields:
        if isinstance(fields[field], str) or isinstance(fields[field], int) or isinstance(fields[field], float):
            if '*' == fields[field]: fields[field] = infra_pb2.ValueFilter(operation=infra_pb2.FilterOperation.NOT_EMPTY)
            else:
                fields[field] = infra_pb2.ValueFilter(simple_filter=fields[field])
    return infra_pb2.ValueFilter(message_filter=infra_pb2.MessageFilter(fields=fields))


def create_filter(msg_name, fields):
    fields = copy.deepcopy(fields)
    for field in fields:
        if isinstance(fields[field], (str, int, float)):
            if fields[field] == '*':
                fields[field] = infra_pb2.ValueFilter(operation=infra_pb2.FilterOperation.NOT_EMPTY)
            elif fields[field] == '#':
                fields[field] = infra_pb2.ValueFilter(operation=infra_pb2.FilterOperation.EMPTY)
            elif field == 'ClOrdID':
                fields[field] = infra_pb2.ValueFilter(simple_filter=fields[field], key=True)
            else:
                fields[field] = infra_pb2.ValueFilter(simple_filter=fields[field])
        elif isinstance(fields[field], dict):
            fields[field] = create_sub_filter(fields[field])
        elif isinstance(fields[field], list):
            fields[field] = infra_pb2.ValueFilter(
                message_filter=infra_pb2.MessageFilter(
                    fields={
                        field: infra_pb2.ValueFilter(
                            list_filter=infra_pb2.ListValueFilter(
                                values=list(map(create_sub_filter, fields[field])))
                        )
                    }
                )
            )
    return infra_pb2.MessageFilter(messageType=msg_name, fields=fields)

