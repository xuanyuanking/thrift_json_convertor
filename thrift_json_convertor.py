# -*- coding: utf-8 -*-
"""
    This module implements the convertor between thrift struct and json use thriftpy.

    :copyright: (c) 2015 by liyuanjian.
    :license: BSD, see LICE

    Author : XuanYuan(xyliyuanjian@gmail.com)
    Time   : 2015-12-02 13:35:17

"""
import json
import thriftpy

test_thrift = thriftpy.load("test.thrift", module_name="test_thrift")

destination = test_thrift.meta()

#source = '{"name": "abc", "num": 128, "desc": "for_lyj_test", "add_more": {"more": "more"}}'
source = '{"name": "abc", "num": 128, "desc": "for_lyj_test", "add_more": {"more": "more"}, "in_list": [{"l_name": "l_name1"}, {"l_name": "l_name2"}, {"l_name": "l_name3"}]}'

source_struct = json.loads(source)

type_dict = {
    "add_more" : "in_meta",
    "in_list" : "list_test"
}

def json_convert(source_struct, destination):
    for (k, v) in source_struct.items():
        print k,v,type(v)
        print (destination._tspec)
        if not destination._tspec.has_key(k):
            raise thriftpy.parser.exc.ThriftGrammerError("Check input, field(%s) not exist in thrift proto" % k)
        if type(v) is dict:
            tmp = test_thrift.__getattribute__(type_dict[k])()
            json_convert(v, tmp)
            destination.__setattr__(k, tmp)
        elif type(v) is list:
            # list type
            list_ret = []
            for item in v:
                tmp = test_thrift.__getattribute__(type_dict[k])()
                json_convert(item, tmp)
                list_ret.append(tmp)
            destination.__setattr__(k, list_ret)
        else:
            destination.__setattr__(k, v)

json_convert(source_struct, destination)
import pdb
pdb.set_trace()
print destination
