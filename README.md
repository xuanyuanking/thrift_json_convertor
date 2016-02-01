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
Demo of json_thrift_convertor
src_json:
``` c++
{
    "test_simple_map": {
        "a": 1,
        "b": 2
    },
    "name": "abc",
    "add_more": {
        "more": "more"
    },
    "error_type": "SUCCESS",
    "in_list": [
        {
            "l_name": "l_name1"
        },
        {
            "l_name": "l_name2"
        },
        {
            "l_name": "l_name3"
        }
    ],
    "test_struct_map": {
        "a": {
            "value": "abc"
        },
        "b": {
            "value": "abc1"
        }
    },
    "num": 128,
    "simple_list": [
        1,
        2,
        3,
        4
    ],
    "desc": "for_lyj_test"
}
```
dest_struct:
``` c++
meta(test_simple_map={u'a': 1, u'b': 2}, name=u'abc', add_more=in_meta(in_list=None, more=u'more'), error_type=1, in_list=[list_test(l_name=u'l_name1'), list_test(l_name=u'l_name2'), list_test(l_name=u'l_name3')], test_struct_map={u'a': test_map_value(value=u'abc'), u'b': test_map_value(value=u'abc1')}, num=128, simple_list=[1, 2, 3, 4], desc=u'for_lyj_test')
```

Demo of thrift_json_convertor 
stc_struct is dest_struct below
dest json dict is:
``` c++
{
    "test_simple_map": {
        "a": 1,
        "b": 2
    },
    "name": "abc",
    "add_more": {
        "more": "more"
    },
    "error_type": "SUCCESS",
    "in_list": [
        {
            "l_name": "l_name1"
        },
        {
            "l_name": "l_name2"
        },
        {
            "l_name": "l_name3"
        },
        {
            "l_name": "l_name4"
        }
    ],
    "test_struct_map": {
        "a": {
            "value": "abc"
        },
        "b": {
            "value": "abc1"
        }
    },
    "num": 128,
    "simple_list": [
        1,
        2,
        3,
        4
    ],
    "desc": "for_lyj_test"
}
```
