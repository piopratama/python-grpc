# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: streaming.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'streaming.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fstreaming.proto\x12\tstreaming\" \n\rStreamRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"!\n\x0eStreamResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2W\n\x10StreamingService\x12\x43\n\nStreamData\x12\x18.streaming.StreamRequest\x1a\x19.streaming.StreamResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'streaming_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STREAMREQUEST']._serialized_start=30
  _globals['_STREAMREQUEST']._serialized_end=62
  _globals['_STREAMRESPONSE']._serialized_start=64
  _globals['_STREAMRESPONSE']._serialized_end=97
  _globals['_STREAMINGSERVICE']._serialized_start=99
  _globals['_STREAMINGSERVICE']._serialized_end=186
# @@protoc_insertion_point(module_scope)