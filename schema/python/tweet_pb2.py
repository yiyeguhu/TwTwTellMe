# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tweet.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tweet.proto',
  package='',
  serialized_pb=_b('\n\x0btweet.proto\"n\n\x05Tweet\x12\x0c\n\x04text\x18\x01 \x02(\t\x12\x11\n\ttimestamp\x18\x02 \x02(\x05\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x04 \x01(\t\x12\x11\n\tcandidate\x18\x05 \x02(\t\x12\x11\n\tsentiment\x18\x06 \x01(\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TWEET = _descriptor.Descriptor(
  name='Tweet',
  full_name='Tweet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='Tweet.text', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Tweet.timestamp', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='state', full_name='Tweet.state', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country', full_name='Tweet.country', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='candidate', full_name='Tweet.candidate', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sentiment', full_name='Tweet.sentiment', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=125,
)

DESCRIPTOR.message_types_by_name['Tweet'] = _TWEET

Tweet = _reflection.GeneratedProtocolMessageType('Tweet', (_message.Message,), dict(
  DESCRIPTOR = _TWEET,
  __module__ = 'tweet_pb2'
  # @@protoc_insertion_point(class_scope:Tweet)
  ))
_sym_db.RegisterMessage(Tweet)


# @@protoc_insertion_point(module_scope)
