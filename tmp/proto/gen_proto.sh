#!/bin/sh

current_path=`pwd`

parames="common.proto
         AFP_main_frame.proto
		 IOMS_main_frame.proto
         AFP_reptile_control.proto
         QDP_basic_info.proto
         UBAS_niiwoo.proto
         ODP_main_frame.proto
         UBAS_PageView.proto
         UPS_login.proto
         interfaces.proto
         FunctionID.proto
         UBAS_QDP.proto
         QDP_IMP.proto
         DW_Location.proto
         QDP_main_frame.proto
         UPS_niiwoo.proto
         ODP_bid_analysis.proto
		 ODP_user_portrayal.proto
         common_datas.proto"

input=$#


${current_path}/protoc ${parames} --cpp_out=src/cpp

${current_path}/protoc ${parames} --java_out=src/java

${current_path}/protoc ${parames} --python_out=src/python
