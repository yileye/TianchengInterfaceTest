
:: 请将要编译生成的文件赋值给 protobuf_file =

set protobuf_file=common_datas.proto IOMS_main_frame.proto QDP_basic_info.proto common.proto AFP_main_frame.proto AFP_reptile_control.proto QDP_main_frame.proto interfaces.proto UPS_login.proto UBAS_PageView.proto UBAS_niiwoo.proto FunctionID.proto ODP_main_frame.proto UBAS_QDP.proto CCS_IMP.proto QDP_IMP.proto DW_Location.proto UPS_niiwoo.proto ODP_bid_analysis.proto ODP_user_portrayal.proto


protoc.exe %protobuf_file% --cpp_out=src/cpp

protoc.exe %protobuf_file% --java_out=src/java

protoc.exe %protobuf_file% --python_out=src/python

pause
