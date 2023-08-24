import benchmark_test
import clean_data
import clean_log
from get_sysctl_ulimit_res import *
from load_config import *
import regex_prefix
import set_parameters
import json

with open('config/config.json') as f:
    data = json.load(f)

# 选择测试模式
selected_mode = input("请选择测试模式 (host_test 或 communication_test): ")

if selected_mode == 'host_test':
    host_test_body(data)

if selected_mode == 'communication_test':
    communication_test_body(data)