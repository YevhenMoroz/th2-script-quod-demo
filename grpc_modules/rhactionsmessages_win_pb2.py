# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rhactionsmessages_win.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rhactionsmessages_win.proto',
  package='th2',
  syntax='proto3',
  serialized_options=_b('\n(com.exactpro.th2.act.grpc.hand.rhactionsB\024RhWinActionsMessagesP\000'),
  serialized_pb=_b('\n\x1brhactionsmessages_win.proto\x12\x03th2\x1a\x1egoogle/protobuf/wrappers.proto\"a\n\nWinLocator\x12\x0f\n\x07locator\x18\x01 \x01(\t\x12\x0f\n\x07matcher\x18\x02 \x01(\t\x12\x31\n\x0cmatcherIndex\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\"H\n\x07WinOpen\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x0f\n\x07workDir\x18\x04 \x01(\t\x12\x0f\n\x07\x61ppFile\x18\x05 \x01(\t\"\x83\x02\n\x08WinClick\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12$\n\x06\x62utton\x18\x04 \x01(\x0e\x32\x14.th2.WinClick.Button\x12,\n\x07xOffset\x18\x05 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12,\n\x07yOffset\x18\x06 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\"5\n\x06\x42utton\x12\x08\n\x04LEFT\x10\x00\x12\t\n\x05RIGHT\x10\x01\x12\n\n\x06MIDDLE\x10\x02\x12\n\n\x06\x44OUBLE\x10\x03\"\x86\x01\n\x0bWinSendText\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x0c\n\x04text\x18\x04 \x01(\t\x12\x13\n\x0b\x63learBefore\x18\x05 \x01(\t\x12\x14\n\x0cisDirectText\x18\x06 \x01(\t\"E\n\x12WinGetActiveWindow\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x12\n\nwindowName\x18\x04 \x01(\t\"o\n\x16WinGetElementAttribute\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x15\n\rattributeName\x18\x04 \x01(\t\"6\n\x07WinWait\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x0e\n\x06millis\x18\x04 \x01(\r\"j\n\x11WinToggleCheckBox\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x15\n\rexpectedState\x18\x04 \x01(\t\"U\n\x13WinClickContextMenu\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\"Q\n\x0fWinCheckElement\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\"?\n\x0cWinGetWindow\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x12\n\nwindowName\x18\x04 \x01(\t\"R\n\x10WinSearchElement\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\"\xc0\x01\n\x13WinWaitForAttribute\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x15\n\rattributeName\x18\x04 \x01(\t\x12\x15\n\rexpectedValue\x18\x05 \x01(\t\x12\x12\n\nmaxTimeout\x18\x06 \x01(\t\x12\x15\n\rcheckInterval\x18\x07 \x01(\t\x12\x10\n\x08\x66romRoot\x18\x08 \x01(\t\"\xa6\x01\n\x12WinScrollUsingText\x12!\n\x08locators\x18\x01 \x03(\x0b\x32\x0f.th2.WinLocator\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0f\n\x07\x65xecute\x18\x03 \x01(\t\x12\x12\n\ntextToSend\x18\x04 \x01(\t\x12\x15\n\rmaxIterations\x18\x05 \x01(\t\x12%\n\x0ctextLocators\x18\x06 \x03(\x0b\x32\x0f.th2.WinLocatorBB\n(com.exactpro.th2.act.grpc.hand.rhactionsB\x14RhWinActionsMessagesP\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,])



_WINCLICK_BUTTON = _descriptor.EnumDescriptor(
  name='Button',
  full_name='th2.WinClick.Button',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MIDDLE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOUBLE', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=448,
  serialized_end=501,
)
_sym_db.RegisterEnumDescriptor(_WINCLICK_BUTTON)


_WINLOCATOR = _descriptor.Descriptor(
  name='WinLocator',
  full_name='th2.WinLocator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locator', full_name='th2.WinLocator.locator', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='matcher', full_name='th2.WinLocator.matcher', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='matcherIndex', full_name='th2.WinLocator.matcherIndex', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=165,
)


_WINOPEN = _descriptor.Descriptor(
  name='WinOpen',
  full_name='th2.WinOpen',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinOpen.id', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinOpen.execute', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='workDir', full_name='th2.WinOpen.workDir', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='appFile', full_name='th2.WinOpen.appFile', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=167,
  serialized_end=239,
)


_WINCLICK = _descriptor.Descriptor(
  name='WinClick',
  full_name='th2.WinClick',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinClick.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinClick.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinClick.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='button', full_name='th2.WinClick.button', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='xOffset', full_name='th2.WinClick.xOffset', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='yOffset', full_name='th2.WinClick.yOffset', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _WINCLICK_BUTTON,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=242,
  serialized_end=501,
)


_WINSENDTEXT = _descriptor.Descriptor(
  name='WinSendText',
  full_name='th2.WinSendText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinSendText.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinSendText.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinSendText.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='th2.WinSendText.text', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='clearBefore', full_name='th2.WinSendText.clearBefore', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isDirectText', full_name='th2.WinSendText.isDirectText', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=504,
  serialized_end=638,
)


_WINGETACTIVEWINDOW = _descriptor.Descriptor(
  name='WinGetActiveWindow',
  full_name='th2.WinGetActiveWindow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinGetActiveWindow.id', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinGetActiveWindow.execute', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='windowName', full_name='th2.WinGetActiveWindow.windowName', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=640,
  serialized_end=709,
)


_WINGETELEMENTATTRIBUTE = _descriptor.Descriptor(
  name='WinGetElementAttribute',
  full_name='th2.WinGetElementAttribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinGetElementAttribute.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinGetElementAttribute.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinGetElementAttribute.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attributeName', full_name='th2.WinGetElementAttribute.attributeName', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=711,
  serialized_end=822,
)


_WINWAIT = _descriptor.Descriptor(
  name='WinWait',
  full_name='th2.WinWait',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinWait.id', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinWait.execute', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='millis', full_name='th2.WinWait.millis', index=2,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=824,
  serialized_end=878,
)


_WINTOGGLECHECKBOX = _descriptor.Descriptor(
  name='WinToggleCheckBox',
  full_name='th2.WinToggleCheckBox',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinToggleCheckBox.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinToggleCheckBox.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinToggleCheckBox.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expectedState', full_name='th2.WinToggleCheckBox.expectedState', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=880,
  serialized_end=986,
)


_WINCLICKCONTEXTMENU = _descriptor.Descriptor(
  name='WinClickContextMenu',
  full_name='th2.WinClickContextMenu',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinClickContextMenu.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinClickContextMenu.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinClickContextMenu.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=988,
  serialized_end=1073,
)


_WINCHECKELEMENT = _descriptor.Descriptor(
  name='WinCheckElement',
  full_name='th2.WinCheckElement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinCheckElement.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinCheckElement.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinCheckElement.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1075,
  serialized_end=1156,
)


_WINGETWINDOW = _descriptor.Descriptor(
  name='WinGetWindow',
  full_name='th2.WinGetWindow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinGetWindow.id', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinGetWindow.execute', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='windowName', full_name='th2.WinGetWindow.windowName', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1158,
  serialized_end=1221,
)


_WINSEARCHELEMENT = _descriptor.Descriptor(
  name='WinSearchElement',
  full_name='th2.WinSearchElement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinSearchElement.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinSearchElement.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinSearchElement.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1223,
  serialized_end=1305,
)


_WINWAITFORATTRIBUTE = _descriptor.Descriptor(
  name='WinWaitForAttribute',
  full_name='th2.WinWaitForAttribute',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinWaitForAttribute.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinWaitForAttribute.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinWaitForAttribute.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attributeName', full_name='th2.WinWaitForAttribute.attributeName', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expectedValue', full_name='th2.WinWaitForAttribute.expectedValue', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='maxTimeout', full_name='th2.WinWaitForAttribute.maxTimeout', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='checkInterval', full_name='th2.WinWaitForAttribute.checkInterval', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fromRoot', full_name='th2.WinWaitForAttribute.fromRoot', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1308,
  serialized_end=1500,
)


_WINSCROLLUSINGTEXT = _descriptor.Descriptor(
  name='WinScrollUsingText',
  full_name='th2.WinScrollUsingText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locators', full_name='th2.WinScrollUsingText.locators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='th2.WinScrollUsingText.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='execute', full_name='th2.WinScrollUsingText.execute', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='textToSend', full_name='th2.WinScrollUsingText.textToSend', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='maxIterations', full_name='th2.WinScrollUsingText.maxIterations', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='textLocators', full_name='th2.WinScrollUsingText.textLocators', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1503,
  serialized_end=1669,
)

_WINLOCATOR.fields_by_name['matcherIndex'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT32VALUE
_WINCLICK.fields_by_name['locators'].message_type = _WINLOCATOR
_WINCLICK.fields_by_name['button'].enum_type = _WINCLICK_BUTTON
_WINCLICK.fields_by_name['xOffset'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT32VALUE
_WINCLICK.fields_by_name['yOffset'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT32VALUE
_WINCLICK_BUTTON.containing_type = _WINCLICK
_WINSENDTEXT.fields_by_name['locators'].message_type = _WINLOCATOR
_WINGETELEMENTATTRIBUTE.fields_by_name['locators'].message_type = _WINLOCATOR
_WINTOGGLECHECKBOX.fields_by_name['locators'].message_type = _WINLOCATOR
_WINCLICKCONTEXTMENU.fields_by_name['locators'].message_type = _WINLOCATOR
_WINCHECKELEMENT.fields_by_name['locators'].message_type = _WINLOCATOR
_WINSEARCHELEMENT.fields_by_name['locators'].message_type = _WINLOCATOR
_WINWAITFORATTRIBUTE.fields_by_name['locators'].message_type = _WINLOCATOR
_WINSCROLLUSINGTEXT.fields_by_name['locators'].message_type = _WINLOCATOR
_WINSCROLLUSINGTEXT.fields_by_name['textLocators'].message_type = _WINLOCATOR
DESCRIPTOR.message_types_by_name['WinLocator'] = _WINLOCATOR
DESCRIPTOR.message_types_by_name['WinOpen'] = _WINOPEN
DESCRIPTOR.message_types_by_name['WinClick'] = _WINCLICK
DESCRIPTOR.message_types_by_name['WinSendText'] = _WINSENDTEXT
DESCRIPTOR.message_types_by_name['WinGetActiveWindow'] = _WINGETACTIVEWINDOW
DESCRIPTOR.message_types_by_name['WinGetElementAttribute'] = _WINGETELEMENTATTRIBUTE
DESCRIPTOR.message_types_by_name['WinWait'] = _WINWAIT
DESCRIPTOR.message_types_by_name['WinToggleCheckBox'] = _WINTOGGLECHECKBOX
DESCRIPTOR.message_types_by_name['WinClickContextMenu'] = _WINCLICKCONTEXTMENU
DESCRIPTOR.message_types_by_name['WinCheckElement'] = _WINCHECKELEMENT
DESCRIPTOR.message_types_by_name['WinGetWindow'] = _WINGETWINDOW
DESCRIPTOR.message_types_by_name['WinSearchElement'] = _WINSEARCHELEMENT
DESCRIPTOR.message_types_by_name['WinWaitForAttribute'] = _WINWAITFORATTRIBUTE
DESCRIPTOR.message_types_by_name['WinScrollUsingText'] = _WINSCROLLUSINGTEXT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WinLocator = _reflection.GeneratedProtocolMessageType('WinLocator', (_message.Message,), dict(
  DESCRIPTOR = _WINLOCATOR,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinLocator)
  ))
_sym_db.RegisterMessage(WinLocator)

WinOpen = _reflection.GeneratedProtocolMessageType('WinOpen', (_message.Message,), dict(
  DESCRIPTOR = _WINOPEN,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinOpen)
  ))
_sym_db.RegisterMessage(WinOpen)

WinClick = _reflection.GeneratedProtocolMessageType('WinClick', (_message.Message,), dict(
  DESCRIPTOR = _WINCLICK,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinClick)
  ))
_sym_db.RegisterMessage(WinClick)

WinSendText = _reflection.GeneratedProtocolMessageType('WinSendText', (_message.Message,), dict(
  DESCRIPTOR = _WINSENDTEXT,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinSendText)
  ))
_sym_db.RegisterMessage(WinSendText)

WinGetActiveWindow = _reflection.GeneratedProtocolMessageType('WinGetActiveWindow', (_message.Message,), dict(
  DESCRIPTOR = _WINGETACTIVEWINDOW,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinGetActiveWindow)
  ))
_sym_db.RegisterMessage(WinGetActiveWindow)

WinGetElementAttribute = _reflection.GeneratedProtocolMessageType('WinGetElementAttribute', (_message.Message,), dict(
  DESCRIPTOR = _WINGETELEMENTATTRIBUTE,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinGetElementAttribute)
  ))
_sym_db.RegisterMessage(WinGetElementAttribute)

WinWait = _reflection.GeneratedProtocolMessageType('WinWait', (_message.Message,), dict(
  DESCRIPTOR = _WINWAIT,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinWait)
  ))
_sym_db.RegisterMessage(WinWait)

WinToggleCheckBox = _reflection.GeneratedProtocolMessageType('WinToggleCheckBox', (_message.Message,), dict(
  DESCRIPTOR = _WINTOGGLECHECKBOX,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinToggleCheckBox)
  ))
_sym_db.RegisterMessage(WinToggleCheckBox)

WinClickContextMenu = _reflection.GeneratedProtocolMessageType('WinClickContextMenu', (_message.Message,), dict(
  DESCRIPTOR = _WINCLICKCONTEXTMENU,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinClickContextMenu)
  ))
_sym_db.RegisterMessage(WinClickContextMenu)

WinCheckElement = _reflection.GeneratedProtocolMessageType('WinCheckElement', (_message.Message,), dict(
  DESCRIPTOR = _WINCHECKELEMENT,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinCheckElement)
  ))
_sym_db.RegisterMessage(WinCheckElement)

WinGetWindow = _reflection.GeneratedProtocolMessageType('WinGetWindow', (_message.Message,), dict(
  DESCRIPTOR = _WINGETWINDOW,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinGetWindow)
  ))
_sym_db.RegisterMessage(WinGetWindow)

WinSearchElement = _reflection.GeneratedProtocolMessageType('WinSearchElement', (_message.Message,), dict(
  DESCRIPTOR = _WINSEARCHELEMENT,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinSearchElement)
  ))
_sym_db.RegisterMessage(WinSearchElement)

WinWaitForAttribute = _reflection.GeneratedProtocolMessageType('WinWaitForAttribute', (_message.Message,), dict(
  DESCRIPTOR = _WINWAITFORATTRIBUTE,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinWaitForAttribute)
  ))
_sym_db.RegisterMessage(WinWaitForAttribute)

WinScrollUsingText = _reflection.GeneratedProtocolMessageType('WinScrollUsingText', (_message.Message,), dict(
  DESCRIPTOR = _WINSCROLLUSINGTEXT,
  __module__ = 'rhactionsmessages_win_pb2'
  # @@protoc_insertion_point(class_scope:th2.WinScrollUsingText)
  ))
_sym_db.RegisterMessage(WinScrollUsingText)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
