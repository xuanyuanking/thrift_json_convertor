#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Module Description:
        Convertor between json and thrift struct, write by metaprogramming and maily 
    depends on thriftpy, it will boost the program speed in operation handler and no
    need to see the detail of thrift type which httpserver shouldn`t know.

    Authors: Li Yuanjian (liyuanjian@baidu.com)
    Date   : 2015-11-30 16:35:29

    Implement Notes:
               
        1. _tspec details ：

            _tspec struct in ut example       

            {
                'add_more': (False, (12, <class 'test_thrift.in_meta'>)), 
                'num': (False, 10), 
                'name': (False, 11), 
                'in_list': (False, (15, (12, <class 'test_thrift.list_test'>))), 
                'desc': (False, 11)
            }

            type  : dict
            key   : fields name
            value : tuple of fields details, ($required/optional, $type)

            所以此处只要确认fields details中的type字段为tuple进入递归即可, 
            基础类型不应该进入下一轮递归

        2. json_thrift_convertor() thrift_json_convertor() both in recurese, test 
           in ut can run in 1ms.
"""
from thriftpy.thrift import TType
import logging as LOG

class UnknowInputFieldsError(Exception):
    pass

class Thrift2JsonParseError(Exception):
    pass

def json_thrift_convertor(src_json, dest_struct, ignore_unknow_key=False):
    """
        @src_json:    dict loads from user pass json body
        @dest_struct: final thrift type after parse
        @ignore_unknow_key: default False, if one key in src_json but not
            in thrift proto define, throw an exception(False) or just 
            ignore(True)
    """
    try:
        for (k, v) in src_json.items():
            # 此处需要进行field检查,确认对应的field`s在thrift结构的proto定义中,
            # 此处如果不加检查,其实__setattr__依然可以给目的结构加入不存在的key
            if not dest_struct._tspec.has_key(k):
                if not ignore_unknow_key:
                    LOG.error("user`s fields(%s) not exist in thrift proto" % k)
                    raise UnknowInputFieldsError(
                        "Check input, field(%s) not exist in thrift proto" % k)
                else:
                    LOG.warn("user input fields(%s) not exist in thrift proto" % k)
            if type(v) is dict:
                # assert dest_struct._tspec[k][1][0] not base_type
                if dest_struct._tspec[k][1][0] == TType.MAP:
                    # logic for simple map and struct map,
                    if type(dest_struct._tspec[k][1][1][1]) is not tuple:
                        # simple map support
                        dest_struct.__setattr__(k, v)
                        continue
                    else:
                        # map of struct support
                        map_tmp = dict()
                        for (map_k, map_v) in v.items():
                            tmp = dest_struct._tspec[k][1][1][1][1]()
                            json_thrift_convertor(map_v, tmp)
                            map_tmp[map_k] = tmp
                        dest_struct.__setattr__(k, map_tmp)
                        continue
                else:
                    tmp = dest_struct._tspec[k][1][1]()
                    json_thrift_convertor(v, tmp)
                    dest_struct.__setattr__(k, tmp)
            elif type(v) is list:
                # list type
                # assert dest_struct._tpsec[k][1][0] is list
                list_ret = []
                for item in v:
                    tmp = item
                    if type(dest_struct._tspec[k][1][1]) is tuple:
                        # assert dest_struct._tspec[k][1][1][0] not base_type
                        #tmp = dest_struct._tspec[k][1][1][1]()
                        #json_thrift_convertor(item, tmp)
                        tmp = dest_struct._tspec[k][1][1][1]()
                        if type(dest_struct._tspec[k][1][1][0] == TType.I32) and type(item) is str:
                            # specify for enum in list, convert string to enum type
                            tmp = getattr(dest_struct._tspec[k][1][1][1], '_NAMES_TO_VALUES')[item]
                        else:
                            json_thrift_convertor(item, tmp)
                    list_ret.append(tmp)
                dest_struct.__setattr__(k, list_ret)
            else:
                if type(dest_struct._tspec[k][1]) is tuple and \
                    dest_struct._tspec[k][1][0] == TType.I32:
                    # specify for enum
                    dest_struct.__setattr__(k, getattr(dest_struct._tspec[k][1][1], 
                        '_NAMES_TO_VALUES')[v])
                else:
                    dest_struct.__setattr__(k, v)
    except UnknowInputFieldsError as e:
        raise e
    except Exception as e:
        LOG.error("Convert from src_json(%s) to dest_struct(%s) FAIL" % (src_json, dest_struct))
        from common.exceptions import Json2ThriftParseError
        raise Json2ThriftParseError("Parse input json(%s) ERROR, please check input" % src_json)

def thrift_json_convertor(src_struct, dest_dict):
    """
        @src_struct: thrift type 
        @dest_dict : destination dict, parse from src_struct
    """
    try:
        for (k, v) in src_struct.__dict__.items():
            # if there`s an optional None value, just pass
            if v is None: continue
            if type(src_struct._tspec[k][1]) is tuple:
                if src_struct._tspec[k][1][0] != TType.LIST:
                    # container type or struct
                    tmp = dict()
                    if src_struct._tspec[k][1][0] == 13 and type(src_struct._tspec[k][1][1][1]) is tuple:
                        # specific logic for struct map
                        for (map_k, map_v) in v.items():
                            tmp_map = dict()
                            thrift_json_convertor(v[map_k], tmp_map)
                            tmp[map_k] = tmp_map
                        dest_dict[k] = tmp
                        continue
                    if hasattr(v, "__dict__"):
                        thrift_json_convertor(v, tmp)
                    elif src_struct._tspec[k][1][0] == TType.I32:
                        # specified for enum, change it to readble string
                        tmp = getattr(src_struct._tspec[k][1][1], '_VALUES_TO_NAMES')[v]
                    else:
                        # simple type, just set
                        tmp = v
                    dest_dict[k] = tmp
                else:
                    # list type
                    tmp = v
                    if type(src_struct._tspec[k][1][1]) is tuple:
                        # list type of struct\container type
                        tmp = list()
                        for item in v:
                            item_tmp = dict()
                            thrift_json_convertor(item, item_tmp)
                            tmp.append(item_tmp)
                    dest_dict[k] = tmp
            else:
                dest_dict[k] = v
    except Exception as e:
        LOG.error("Convert from src_struct(%s) to dest_dict(%s) FAIL" % (src_struct, dest_dict))
        raise Thrift2JsonParseError("Response generate except, please report this to us")
