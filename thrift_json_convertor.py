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

# test for not have optional fields
#source = '{"name": "abc", "num": 128, "desc": "for_lyj_test", "add_more": {"more": "more"}}'

# test for not exist fields(in_list not in meta)
#source = '{"name": "abc", "num": 128, "desc": "for_lyj_test", "add_more": {"more": "more"}, "in_list": [{"l_name": "l_name1"}, {"l_name": "l_name2"}, {"l_name": "l_name3"}]}'

# normal test senarior
source = '{"name": "abc", "num": 128, "desc": "for_lyj_test", "simple_list": [1,2,3,4], "add_more": {"more": "more"}, "in_list": [{"l_name": "l_name1"}, {"l_name": "l_name2"}, {"l_name": "l_name3"}], "error_type": "SUCCESS"}'

source_struct = json.loads(source)

type_dict = {
    "add_more" : "in_meta",
    "in_list" : "list_test"
}
"""
_tspec struct in this example

{'add_more': (False, (12, <class 'test_thrift.in_meta'>)), 'num': (False, 10), 'name': (False, 11), 'in_list': (False, (15, (12, <class 'test_thrift.list_test'>))), 'desc': (False, 11)}

_tspec结构细节：
    type  : dict
    key   : fields name
    value : tuple of fields details, ($required/optional, $type)
    所以此处只要确认fields details中的type字段为tuple进入递归即可, 基础类型不应该进入下一轮递归
"""

def json_thrift_convertor(source_struct, destination):
    for (k, v) in source_struct.items():
        #print k,v,type(v)
        #print (destination._tspec)
        # 此处需要进行field检查,确认对应的field`s在thrift结构的proto定义中,
        # 此处如果不加检查,其实__setattr__已然可以给目的结构加入不存在的key
        if not destination._tspec.has_key(k):
            raise thriftpy.parser.exc.ThriftGrammerError("Check input, field(%s) not exist in thrift proto" % k)
        if type(v) is dict:
            #tmp = test_thrift.__getattribute__(type_dict[k])()
            # assert destination._tspec[k][1][0] not base_type
            tmp = destination._tspec[k][1][1]()
            json_thrift_convertor(v, tmp)
            destination.__setattr__(k, tmp)
        elif type(v) is list:
            # list type
            # assert destination._tpsec[k][1][0] is list
            list_ret = []
            for item in v:
                #tmp = test_thrift.__getattribute__(type_dict[k])()
                tmp = item
                #if destination._tspec[k][1][1][0] in (12, 13, 14, 15):
                if type(destination._tspec[k][1][1]) is tuple:
                    # assert destination._tspec[k][1][1][0] not base_type
                    tmp = destination._tspec[k][1][1][1]()
                    json_thrift_convertor(item, tmp)
                list_ret.append(tmp)
            destination.__setattr__(k, list_ret)
        else:
            destination.__setattr__(k, v)

def thrift_json_convertor(thrift_struct, dest_dict):
    for (k, v) in thrift_struct.__dict__.items():
        print k,v,type(v)
    import pdb
    pdb.set_trace()

json_thrift_convertor(source_struct, destination)
print source
print destination

print destination.error_type == test_thrift.error_type_enum.SUCCESS

dest_dict = dict()
thrift_json_convertor(destination, dest_dict)
