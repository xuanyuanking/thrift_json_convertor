/*
  thrift struct for unit test, include nested struct, list of struct
  list of simple type and enum type
 */

struct list_test {
  1: optional string l_name
}

struct in_meta {
  1: required string more,
  2: optional list<list_test> in_list
}

enum error_type_enum {
  SUCCESS = 1,
  FAIL    = 2
}

struct test_map_value {
  1: optional string value
}

struct meta {
  1: optional string name,
  2: optional i64    num,
  3: optional string desc,
  4: optional in_meta add_more,
  5: optional list<list_test> in_list,
  6: optional list<i64> simple_list,
  7: optional error_type_enum error_type,
  8: optional map<string, i32> test_simple_map,
  9: optional map<string, test_map_value> test_struct_map
}