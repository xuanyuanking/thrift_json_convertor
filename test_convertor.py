#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module Description:
    Class ConvertorTest
Authors: Li Yuanjian (liyuanjian@baidu.com)
Date:    2015-12-02 21:19:11

Convert json:
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
To thrift struct:
meta(test_simple_map={u'a': 1, u'b': 2}, name=u'abc', add_more=in_meta(in_list=None, more=u'more'), error_type=1, in_list=[list_test(l_name=u'l_name1'), list_test(l_name=u'l_name2'), list_test(l_name=u'l_name3')], test_struct_map={u'a': test_map_value(value=u'abc'), u'b': test_map_value(value=u'abc1')}, num=128, simple_list=[1, 2, 3, 4], desc=u'for_lyj_test')
.....
Convert thrift struct:

{'test_simple_map': {'a': 1, 'b': 2}, 'name': 'abc', 'add_more': {'more': 'more'}, 'error_type': 'SUCCESS', 'in_list': [{'l_name': 'l_name1'}, {'l_name': 'l_name2'}, {'l_name': 'l_name3'}, {'l_name': 'l_name4'}], 'test_struct_map': {'a': {'value': 'abc'}, 'b': {'value': 'abc1'}}, 'num': 128, 'simple_list': [1, 2, 3, 4], 'desc': 'for_lyj_test'}

To json:
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

"""

import sys
import unittest
import json
import thriftpy
from convertor import json_thrift_convertor, thrift_json_convertor
from convertor import UnknowInputFieldsError 

class Json2ThfirtConvertorTest(unittest.TestCase):
    """ Test class for Convertor"""
    def setUp(self):
        self._input_json = '{ \
            "name": "abc", \
            "num": 128, \
            "desc": "for_lyj_test", \
            "simple_list": [1,2,3,4], \
            "add_more": {"more": "more"}, \
            "in_list": [{"l_name": "l_name1"}, {"l_name": "l_name2"}, {"l_name": "l_name3"}], \
            "error_type": "SUCCESS", \
            "test_struct_map" : {\
                "a": {"value": "abc"}, \
                "b": {"value": "abc1"} \
            }, \
            "test_simple_map" : {"a": 1, "b": 2} \
        }'

        test_thrift        = thriftpy.load("test.thrift", module_name="test_thrift")
        self._json_struct   = json.loads(self._input_json)
        self._thrift_struct = test_thrift.meta()
        json_thrift_convertor(self._json_struct, self._thrift_struct)

    def test_normal_fields_json2thrift(self):
        """ Normal test for conver from json to thrift struct"""
        self.assertEqual(self._json_struct['name'], self._thrift_struct.name)
        self.assertEqual(self._json_struct['num'], self._thrift_struct.num)
        self.assertEqual(self._json_struct['desc'], self._thrift_struct.desc)

    def test_enum_fields_json2thrift(self):
        """ Enum fields test """
        self.assertEqual(self._thrift_struct.error_type, 1)

    def test_nested_fields_json2thrift(self):
        """ Nested fields test """
        self.assertEqual(self._thrift_struct.add_more.more, 
            self._json_struct['add_more']['more'])

    def test_list_with_struct_json2thrift(self):
        """ Test complex list with struct"""
        for i in xrange(0, len(self._json_struct["in_list"])):
            self.assertEqual(self._thrift_struct.in_list[i].l_name, 
                self._json_struct["in_list"][i]["l_name"])

    def test_list_with_basetype_json2thrift(self):
        """ Test list with basetype """
        for i in xrange(0, len(self._json_struct["simple_list"])):
            self.assertEqual(self._thrift_struct.simple_list[i], 
                self._json_struct["simple_list"][i])

    def test_noexist_fields_error_json2thrift(self):
        """ Test no exist fields """
        input_json = '{"name": "abc", "num": 128, "desc": "for_lyj_test", \
            "add_more": {"more": "more"}, \
            "not_exists_list": [{"l_name": "l_name1"}, \
            {"l_name": "l_name2"}, {"l_name": "l_name3"}]}'
        json_struct = json.loads(input_json)
        self.assertRaises(UnknowInputFieldsError, json_thrift_convertor,
            json_struct, self._thrift_struct)

    def test_map_of_basetype_json2thrift(self):
        """ Test map of basetype """
        for (k, v) in self._json_struct["test_simple_map"].items():
            self.assertEqual(self._thrift_struct.test_simple_map[k], v)

    def test_map_of_struct_json2thrift(self):
        """ Test map of basetype """
        for (k, v) in self._json_struct["test_struct_map"].items():
            self.assertEqual(self._thrift_struct.test_struct_map[k].value, 
                v["value"])
        print "\nConvert json:"
        print json.dumps(self._json_struct, indent=4)
        print "To thrift struct:"
        print self._thrift_struct

        
class Thrift2JsonConvertorTest(unittest.TestCase):
    """docstring for Thrift2JsonConvertorTest"""
    def setUp(self):
        test_thrift   = thriftpy.load("test.thrift", module_name="test_thrift")
        self._output_dict   = dict()
        self._thrift_struct = test_thrift.meta()
        self._thrift_struct.name = "abc"
        self._thrift_struct.num  = 128
        self._thrift_struct.desc = "for_lyj_test"
        self._thrift_struct.error_type = 1
        self._thrift_struct.simple_list = [1, 2, 3, 4]
        tmp_list = []
        for i in xrange(1,5):
            tmp = test_thrift.list_test()
            tmp.l_name = "l_name%d" % i
            tmp_list.append(tmp)
        self._thrift_struct.in_list = tmp_list
        tmp = test_thrift.in_meta()
        tmp.more = "more"
        self._thrift_struct.add_more = tmp
        
        tmp_map = dict()
        map_value = test_thrift.test_map_value()
        map_value.value = "abc"
        tmp_map["a"] = map_value
        map_value = test_thrift.test_map_value()
        map_value.value = "abc1"
        tmp_map["b"] = map_value
        self._thrift_struct.test_struct_map = tmp_map

        tmp_map = {"a": 1, "b": 2}
        self._thrift_struct.test_simple_map = tmp_map

        thrift_json_convertor(self._thrift_struct, self._output_dict)

    def test_normal_fields_thrift2json(self):
        """ Normal test for conver from json to thrift struct"""
        self.assertEqual(self._output_dict['name'], self._thrift_struct.name)
        self.assertEqual(self._output_dict['num'], self._thrift_struct.num)
        self.assertEqual(self._output_dict['desc'], self._thrift_struct.desc)

    def test_enum_fields_thrift2json(self):
        """ Enum fields test """
        self.assertEqual(self._thrift_struct.error_type, 1)

    def test_nested_fields_thrift2json(self):
        """ Nested fields test """
        self.assertEqual(self._thrift_struct.add_more.more, 
            self._output_dict['add_more']['more'])

    def test_list_with_struct_thrift2json(self):
        """ Test complex list with struct"""
        for i in xrange(0, len(self._output_dict["in_list"])):
            self.assertEqual(self._thrift_struct.in_list[i].l_name, 
                self._output_dict["in_list"][i]["l_name"])

    def test_list_with_basetype_thrift2json(self):
        """ Test list with basetype """
        for i in xrange(0, len(self._output_dict["simple_list"])):
            self.assertEqual(self._thrift_struct.simple_list[i], 
                self._output_dict["simple_list"][i])

    def test_map_with_basetype_thrift2json(self):
        """ Test map with basetype """
        for (k, v) in self._output_dict["test_simple_map"].items():
            self.assertEqual(self._thrift_struct.test_simple_map[k], v)
    
    def test_map_with_struct_thrift2json(self):
        """ Test map with struct """
        for (k, v) in self._output_dict["test_struct_map"].items():
            #print k,v, self._thrift_struct.test_struct_map[k]
            self.assertEqual(self._thrift_struct.test_struct_map[k].value, v["value"])

    def test_json_loads(self):
        """ Just test for _output_dict can dumps by json (it means all struct
            of thrift is successfully translate) """
        print "\nConvert thrift struct:"
        print self._output_dict
        print "To json:"
        print json.dumps(self._output_dict, indent=4)


if __name__ == '__main__':
    unittest.main()
