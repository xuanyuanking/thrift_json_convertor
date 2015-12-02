# thrift_json_convertor
First of all, thriftpy is a brillent lib for pythonic thrift client\server!
In my project, there`s a requirement is convert json with thrif struct, while thriftpy or stantdard thrif python lib only include thrift json proto.
So here I write a convertor for standard json to thrift struct convert and also convert back for thriftpy.

## standard json -> thrift struct
Mainly use thriftpy module`s _tpec Variable to check and get each type define in thrift file.
Specify logical for list of structs and list of simple type, this is now a recurse version, so the deeps of struct should now very high, if needed can change it to a non-recurse version 
