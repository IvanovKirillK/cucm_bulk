# cucm_bulk
bulk csv producer

## Requirements

### input data file structure:

name,internal_number,dect_number,ftmn_number,phone_model,inbound_number,outbound_number,old_site_prefix,new_site_prefix


### input metadata file structure:

site_description="/МосОбл"

dn_partition='Pt_Internal'

dp_prefix='DP_Center_50_MosObl_EP_'

pt_prefix='PT_Center_50_MosObl_PSTN_AON_'

otput_filename_prefix='KRG_'

### input user_diretory file structure:

old_prefix_int_number,ad_username




## Flow

1. check input files exist
1. check input file structure
1. user input for step selection:
	1. prepare dummy phone upload diveded by phone model
	1. prepare user_update and line_appearence
	1. prepare rd and rdp
	1. prepare translation and transformation patterns
	1. prepare pickup groups

action log for further investigation.

### Config parser

import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")
var_a = config.get("myvars", "var_a")
var_b = config.get("myvars", "var_b")
var_c = config.get("myvars", "var_c")