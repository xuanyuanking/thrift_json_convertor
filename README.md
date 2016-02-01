# thrift_json_convertor
First of all, thriftpy is a brillent lib for pythonic thrift client\server!
In my project, there`s a requirement is convert json with thrif struct, while thriftpy or stantdard thrif python lib only include thrift json proto.
So here I write a convertor for standard json to thrift struct convert and also convert back for thriftpy.

## standard json -> thrift struct
Mainly use thriftpy module`s _tpec Variable to check and get each type define in thrift file.
Specify logical for list of structs and list of simple type, this is now a recurse version, so the deeps of struct should now very high, if needed can change it to a non-recurse version 

## thrift struct -> standard json
Use meta programming to convert thrift struct to standard json string

## example
See the description in test_convertor.py 
``` c++
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
```
