// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: common_datas.proto

#ifndef PROTOBUF_common_5fdatas_2eproto__INCLUDED
#define PROTOBUF_common_5fdatas_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 2006000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 2006001 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
#include "common.pb.h"
// @@protoc_insertion_point(includes)

namespace common_datas {

// Internal implementation detail -- do not call these.
void  protobuf_AddDesc_common_5fdatas_2eproto();
void protobuf_AssignDesc_common_5fdatas_2eproto();
void protobuf_ShutdownFile_common_5fdatas_2eproto();

class menu_items;
class menu_items_ask;
class menu_items_ans;

enum item_api_type {
  TerminalVersionItems = 1
};
bool item_api_type_IsValid(int value);
const item_api_type item_api_type_MIN = TerminalVersionItems;
const item_api_type item_api_type_MAX = TerminalVersionItems;
const int item_api_type_ARRAYSIZE = item_api_type_MAX + 1;

const ::google::protobuf::EnumDescriptor* item_api_type_descriptor();
inline const ::std::string& item_api_type_Name(item_api_type value) {
  return ::google::protobuf::internal::NameOfEnum(
    item_api_type_descriptor(), value);
}
inline bool item_api_type_Parse(
    const ::std::string& name, item_api_type* value) {
  return ::google::protobuf::internal::ParseNamedEnum<item_api_type>(
    item_api_type_descriptor(), name, value);
}
// ===================================================================

class menu_items : public ::google::protobuf::Message {
 public:
  menu_items();
  virtual ~menu_items();

  menu_items(const menu_items& from);

  inline menu_items& operator=(const menu_items& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const menu_items& default_instance();

  void Swap(menu_items* other);

  // implements Message ----------------------------------------------

  menu_items* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const menu_items& from);
  void MergeFrom(const menu_items& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // optional bytes id = 1;
  inline bool has_id() const;
  inline void clear_id();
  static const int kIdFieldNumber = 1;
  inline const ::std::string& id() const;
  inline void set_id(const ::std::string& value);
  inline void set_id(const char* value);
  inline void set_id(const void* value, size_t size);
  inline ::std::string* mutable_id();
  inline ::std::string* release_id();
  inline void set_allocated_id(::std::string* id);

  // optional bytes title = 2;
  inline bool has_title() const;
  inline void clear_title();
  static const int kTitleFieldNumber = 2;
  inline const ::std::string& title() const;
  inline void set_title(const ::std::string& value);
  inline void set_title(const char* value);
  inline void set_title(const void* value, size_t size);
  inline ::std::string* mutable_title();
  inline ::std::string* release_title();
  inline void set_allocated_title(::std::string* title);

  // @@protoc_insertion_point(class_scope:common_datas.menu_items)
 private:
  inline void set_has_id();
  inline void clear_has_id();
  inline void set_has_title();
  inline void clear_has_title();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::std::string* id_;
  ::std::string* title_;
  friend void  protobuf_AddDesc_common_5fdatas_2eproto();
  friend void protobuf_AssignDesc_common_5fdatas_2eproto();
  friend void protobuf_ShutdownFile_common_5fdatas_2eproto();

  void InitAsDefaultInstance();
  static menu_items* default_instance_;
};
// -------------------------------------------------------------------

class menu_items_ask : public ::google::protobuf::Message {
 public:
  menu_items_ask();
  virtual ~menu_items_ask();

  menu_items_ask(const menu_items_ask& from);

  inline menu_items_ask& operator=(const menu_items_ask& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const menu_items_ask& default_instance();

  void Swap(menu_items_ask* other);

  // implements Message ----------------------------------------------

  menu_items_ask* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const menu_items_ask& from);
  void MergeFrom(const menu_items_ask& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // optional .common_datas.item_api_type enum_type = 1;
  inline bool has_enum_type() const;
  inline void clear_enum_type();
  static const int kEnumTypeFieldNumber = 1;
  inline ::common_datas::item_api_type enum_type() const;
  inline void set_enum_type(::common_datas::item_api_type value);

  // optional bytes os_version = 2;
  inline bool has_os_version() const;
  inline void clear_os_version();
  static const int kOsVersionFieldNumber = 2;
  inline const ::std::string& os_version() const;
  inline void set_os_version(const ::std::string& value);
  inline void set_os_version(const char* value);
  inline void set_os_version(const void* value, size_t size);
  inline ::std::string* mutable_os_version();
  inline ::std::string* release_os_version();
  inline void set_allocated_os_version(::std::string* os_version);

  // optional .common.common_ask_header ask_header = 3;
  inline bool has_ask_header() const;
  inline void clear_ask_header();
  static const int kAskHeaderFieldNumber = 3;
  inline const ::common::common_ask_header& ask_header() const;
  inline ::common::common_ask_header* mutable_ask_header();
  inline ::common::common_ask_header* release_ask_header();
  inline void set_allocated_ask_header(::common::common_ask_header* ask_header);

  // @@protoc_insertion_point(class_scope:common_datas.menu_items_ask)
 private:
  inline void set_has_enum_type();
  inline void clear_has_enum_type();
  inline void set_has_os_version();
  inline void clear_has_os_version();
  inline void set_has_ask_header();
  inline void clear_has_ask_header();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::std::string* os_version_;
  ::common::common_ask_header* ask_header_;
  int enum_type_;
  friend void  protobuf_AddDesc_common_5fdatas_2eproto();
  friend void protobuf_AssignDesc_common_5fdatas_2eproto();
  friend void protobuf_ShutdownFile_common_5fdatas_2eproto();

  void InitAsDefaultInstance();
  static menu_items_ask* default_instance_;
};
// -------------------------------------------------------------------

class menu_items_ans : public ::google::protobuf::Message {
 public:
  menu_items_ans();
  virtual ~menu_items_ans();

  menu_items_ans(const menu_items_ans& from);

  inline menu_items_ans& operator=(const menu_items_ans& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }

  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }

  static const ::google::protobuf::Descriptor* descriptor();
  static const menu_items_ans& default_instance();

  void Swap(menu_items_ans* other);

  // implements Message ----------------------------------------------

  menu_items_ans* New() const;
  void CopyFrom(const ::google::protobuf::Message& from);
  void MergeFrom(const ::google::protobuf::Message& from);
  void CopyFrom(const menu_items_ans& from);
  void MergeFrom(const menu_items_ans& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  ::google::protobuf::uint8* SerializeWithCachedSizesToArray(::google::protobuf::uint8* output) const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  public:
  ::google::protobuf::Metadata GetMetadata() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // repeated .common_datas.menu_items item = 1;
  inline int item_size() const;
  inline void clear_item();
  static const int kItemFieldNumber = 1;
  inline const ::common_datas::menu_items& item(int index) const;
  inline ::common_datas::menu_items* mutable_item(int index);
  inline ::common_datas::menu_items* add_item();
  inline const ::google::protobuf::RepeatedPtrField< ::common_datas::menu_items >&
      item() const;
  inline ::google::protobuf::RepeatedPtrField< ::common_datas::menu_items >*
      mutable_item();

  // optional .common.result_info result = 2;
  inline bool has_result() const;
  inline void clear_result();
  static const int kResultFieldNumber = 2;
  inline const ::common::result_info& result() const;
  inline ::common::result_info* mutable_result();
  inline ::common::result_info* release_result();
  inline void set_allocated_result(::common::result_info* result);

  // @@protoc_insertion_point(class_scope:common_datas.menu_items_ans)
 private:
  inline void set_has_result();
  inline void clear_has_result();

  ::google::protobuf::UnknownFieldSet _unknown_fields_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::RepeatedPtrField< ::common_datas::menu_items > item_;
  ::common::result_info* result_;
  friend void  protobuf_AddDesc_common_5fdatas_2eproto();
  friend void protobuf_AssignDesc_common_5fdatas_2eproto();
  friend void protobuf_ShutdownFile_common_5fdatas_2eproto();

  void InitAsDefaultInstance();
  static menu_items_ans* default_instance_;
};
// ===================================================================


// ===================================================================

// menu_items

// optional bytes id = 1;
inline bool menu_items::has_id() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void menu_items::set_has_id() {
  _has_bits_[0] |= 0x00000001u;
}
inline void menu_items::clear_has_id() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void menu_items::clear_id() {
  if (id_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    id_->clear();
  }
  clear_has_id();
}
inline const ::std::string& menu_items::id() const {
  // @@protoc_insertion_point(field_get:common_datas.menu_items.id)
  return *id_;
}
inline void menu_items::set_id(const ::std::string& value) {
  set_has_id();
  if (id_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    id_ = new ::std::string;
  }
  id_->assign(value);
  // @@protoc_insertion_point(field_set:common_datas.menu_items.id)
}
inline void menu_items::set_id(const char* value) {
  set_has_id();
  if (id_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    id_ = new ::std::string;
  }
  id_->assign(value);
  // @@protoc_insertion_point(field_set_char:common_datas.menu_items.id)
}
inline void menu_items::set_id(const void* value, size_t size) {
  set_has_id();
  if (id_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    id_ = new ::std::string;
  }
  id_->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:common_datas.menu_items.id)
}
inline ::std::string* menu_items::mutable_id() {
  set_has_id();
  if (id_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    id_ = new ::std::string;
  }
  // @@protoc_insertion_point(field_mutable:common_datas.menu_items.id)
  return id_;
}
inline ::std::string* menu_items::release_id() {
  clear_has_id();
  if (id_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    return NULL;
  } else {
    ::std::string* temp = id_;
    id_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
    return temp;
  }
}
inline void menu_items::set_allocated_id(::std::string* id) {
  if (id_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    delete id_;
  }
  if (id) {
    set_has_id();
    id_ = id;
  } else {
    clear_has_id();
    id_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }
  // @@protoc_insertion_point(field_set_allocated:common_datas.menu_items.id)
}

// optional bytes title = 2;
inline bool menu_items::has_title() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void menu_items::set_has_title() {
  _has_bits_[0] |= 0x00000002u;
}
inline void menu_items::clear_has_title() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void menu_items::clear_title() {
  if (title_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    title_->clear();
  }
  clear_has_title();
}
inline const ::std::string& menu_items::title() const {
  // @@protoc_insertion_point(field_get:common_datas.menu_items.title)
  return *title_;
}
inline void menu_items::set_title(const ::std::string& value) {
  set_has_title();
  if (title_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    title_ = new ::std::string;
  }
  title_->assign(value);
  // @@protoc_insertion_point(field_set:common_datas.menu_items.title)
}
inline void menu_items::set_title(const char* value) {
  set_has_title();
  if (title_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    title_ = new ::std::string;
  }
  title_->assign(value);
  // @@protoc_insertion_point(field_set_char:common_datas.menu_items.title)
}
inline void menu_items::set_title(const void* value, size_t size) {
  set_has_title();
  if (title_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    title_ = new ::std::string;
  }
  title_->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:common_datas.menu_items.title)
}
inline ::std::string* menu_items::mutable_title() {
  set_has_title();
  if (title_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    title_ = new ::std::string;
  }
  // @@protoc_insertion_point(field_mutable:common_datas.menu_items.title)
  return title_;
}
inline ::std::string* menu_items::release_title() {
  clear_has_title();
  if (title_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    return NULL;
  } else {
    ::std::string* temp = title_;
    title_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
    return temp;
  }
}
inline void menu_items::set_allocated_title(::std::string* title) {
  if (title_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    delete title_;
  }
  if (title) {
    set_has_title();
    title_ = title;
  } else {
    clear_has_title();
    title_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }
  // @@protoc_insertion_point(field_set_allocated:common_datas.menu_items.title)
}

// -------------------------------------------------------------------

// menu_items_ask

// optional .common_datas.item_api_type enum_type = 1;
inline bool menu_items_ask::has_enum_type() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void menu_items_ask::set_has_enum_type() {
  _has_bits_[0] |= 0x00000001u;
}
inline void menu_items_ask::clear_has_enum_type() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void menu_items_ask::clear_enum_type() {
  enum_type_ = 1;
  clear_has_enum_type();
}
inline ::common_datas::item_api_type menu_items_ask::enum_type() const {
  // @@protoc_insertion_point(field_get:common_datas.menu_items_ask.enum_type)
  return static_cast< ::common_datas::item_api_type >(enum_type_);
}
inline void menu_items_ask::set_enum_type(::common_datas::item_api_type value) {
  assert(::common_datas::item_api_type_IsValid(value));
  set_has_enum_type();
  enum_type_ = value;
  // @@protoc_insertion_point(field_set:common_datas.menu_items_ask.enum_type)
}

// optional bytes os_version = 2;
inline bool menu_items_ask::has_os_version() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void menu_items_ask::set_has_os_version() {
  _has_bits_[0] |= 0x00000002u;
}
inline void menu_items_ask::clear_has_os_version() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void menu_items_ask::clear_os_version() {
  if (os_version_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    os_version_->clear();
  }
  clear_has_os_version();
}
inline const ::std::string& menu_items_ask::os_version() const {
  // @@protoc_insertion_point(field_get:common_datas.menu_items_ask.os_version)
  return *os_version_;
}
inline void menu_items_ask::set_os_version(const ::std::string& value) {
  set_has_os_version();
  if (os_version_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    os_version_ = new ::std::string;
  }
  os_version_->assign(value);
  // @@protoc_insertion_point(field_set:common_datas.menu_items_ask.os_version)
}
inline void menu_items_ask::set_os_version(const char* value) {
  set_has_os_version();
  if (os_version_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    os_version_ = new ::std::string;
  }
  os_version_->assign(value);
  // @@protoc_insertion_point(field_set_char:common_datas.menu_items_ask.os_version)
}
inline void menu_items_ask::set_os_version(const void* value, size_t size) {
  set_has_os_version();
  if (os_version_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    os_version_ = new ::std::string;
  }
  os_version_->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:common_datas.menu_items_ask.os_version)
}
inline ::std::string* menu_items_ask::mutable_os_version() {
  set_has_os_version();
  if (os_version_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    os_version_ = new ::std::string;
  }
  // @@protoc_insertion_point(field_mutable:common_datas.menu_items_ask.os_version)
  return os_version_;
}
inline ::std::string* menu_items_ask::release_os_version() {
  clear_has_os_version();
  if (os_version_ == &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    return NULL;
  } else {
    ::std::string* temp = os_version_;
    os_version_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
    return temp;
  }
}
inline void menu_items_ask::set_allocated_os_version(::std::string* os_version) {
  if (os_version_ != &::google::protobuf::internal::GetEmptyStringAlreadyInited()) {
    delete os_version_;
  }
  if (os_version) {
    set_has_os_version();
    os_version_ = os_version;
  } else {
    clear_has_os_version();
    os_version_ = const_cast< ::std::string*>(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }
  // @@protoc_insertion_point(field_set_allocated:common_datas.menu_items_ask.os_version)
}

// optional .common.common_ask_header ask_header = 3;
inline bool menu_items_ask::has_ask_header() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void menu_items_ask::set_has_ask_header() {
  _has_bits_[0] |= 0x00000004u;
}
inline void menu_items_ask::clear_has_ask_header() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void menu_items_ask::clear_ask_header() {
  if (ask_header_ != NULL) ask_header_->::common::common_ask_header::Clear();
  clear_has_ask_header();
}
inline const ::common::common_ask_header& menu_items_ask::ask_header() const {
  // @@protoc_insertion_point(field_get:common_datas.menu_items_ask.ask_header)
  return ask_header_ != NULL ? *ask_header_ : *default_instance_->ask_header_;
}
inline ::common::common_ask_header* menu_items_ask::mutable_ask_header() {
  set_has_ask_header();
  if (ask_header_ == NULL) ask_header_ = new ::common::common_ask_header;
  // @@protoc_insertion_point(field_mutable:common_datas.menu_items_ask.ask_header)
  return ask_header_;
}
inline ::common::common_ask_header* menu_items_ask::release_ask_header() {
  clear_has_ask_header();
  ::common::common_ask_header* temp = ask_header_;
  ask_header_ = NULL;
  return temp;
}
inline void menu_items_ask::set_allocated_ask_header(::common::common_ask_header* ask_header) {
  delete ask_header_;
  ask_header_ = ask_header;
  if (ask_header) {
    set_has_ask_header();
  } else {
    clear_has_ask_header();
  }
  // @@protoc_insertion_point(field_set_allocated:common_datas.menu_items_ask.ask_header)
}

// -------------------------------------------------------------------

// menu_items_ans

// repeated .common_datas.menu_items item = 1;
inline int menu_items_ans::item_size() const {
  return item_.size();
}
inline void menu_items_ans::clear_item() {
  item_.Clear();
}
inline const ::common_datas::menu_items& menu_items_ans::item(int index) const {
  // @@protoc_insertion_point(field_get:common_datas.menu_items_ans.item)
  return item_.Get(index);
}
inline ::common_datas::menu_items* menu_items_ans::mutable_item(int index) {
  // @@protoc_insertion_point(field_mutable:common_datas.menu_items_ans.item)
  return item_.Mutable(index);
}
inline ::common_datas::menu_items* menu_items_ans::add_item() {
  // @@protoc_insertion_point(field_add:common_datas.menu_items_ans.item)
  return item_.Add();
}
inline const ::google::protobuf::RepeatedPtrField< ::common_datas::menu_items >&
menu_items_ans::item() const {
  // @@protoc_insertion_point(field_list:common_datas.menu_items_ans.item)
  return item_;
}
inline ::google::protobuf::RepeatedPtrField< ::common_datas::menu_items >*
menu_items_ans::mutable_item() {
  // @@protoc_insertion_point(field_mutable_list:common_datas.menu_items_ans.item)
  return &item_;
}

// optional .common.result_info result = 2;
inline bool menu_items_ans::has_result() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void menu_items_ans::set_has_result() {
  _has_bits_[0] |= 0x00000002u;
}
inline void menu_items_ans::clear_has_result() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void menu_items_ans::clear_result() {
  if (result_ != NULL) result_->::common::result_info::Clear();
  clear_has_result();
}
inline const ::common::result_info& menu_items_ans::result() const {
  // @@protoc_insertion_point(field_get:common_datas.menu_items_ans.result)
  return result_ != NULL ? *result_ : *default_instance_->result_;
}
inline ::common::result_info* menu_items_ans::mutable_result() {
  set_has_result();
  if (result_ == NULL) result_ = new ::common::result_info;
  // @@protoc_insertion_point(field_mutable:common_datas.menu_items_ans.result)
  return result_;
}
inline ::common::result_info* menu_items_ans::release_result() {
  clear_has_result();
  ::common::result_info* temp = result_;
  result_ = NULL;
  return temp;
}
inline void menu_items_ans::set_allocated_result(::common::result_info* result) {
  delete result_;
  result_ = result;
  if (result) {
    set_has_result();
  } else {
    clear_has_result();
  }
  // @@protoc_insertion_point(field_set_allocated:common_datas.menu_items_ans.result)
}


// @@protoc_insertion_point(namespace_scope)

}  // namespace common_datas

#ifndef SWIG
namespace google {
namespace protobuf {

template <> struct is_proto_enum< ::common_datas::item_api_type> : ::google::protobuf::internal::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::common_datas::item_api_type>() {
  return ::common_datas::item_api_type_descriptor();
}

}  // namespace google
}  // namespace protobuf
#endif  // SWIG

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_common_5fdatas_2eproto__INCLUDED
