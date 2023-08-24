 my_ospp git:(main) tree
.
├── benchmark_test.py                                      # 用于性能测试
├── clean_data.py                                          # 清理 ./data/ 下的数据
├── clean_log.py                                           # 清理 ./log/ 下的日志
├── config                                                 # 配置文件夹
│   ├── config.json                                        # 选择测试的模式、记录对应模式下的 IP 与 User
│   ├── prefix.json                                        # 解析参数时使用到的前缀
│   └── sysyctl_paraments.json                             # 用于匹配和查询的参数详情           
├── data
│   ├── differ-2023-08-24-10-14-42.txt                     # 比较参数差异
│   ├── diff-res.txt                                      
│   ├── statistical-2023-08-24-10-14-42.txt                # 统计差异：一致项、缺失项、不同值的项
│   ├── sysctl@CentOSStream.txt                            # CentOS 的 sysctl 参数
│   ├── sysctl@openEuler.txt                               # OpenEuler 的 sysctl 参数
│   ├── sysctl@Unknown.txt                                 # Unknown 系统的 sysctl 参数
│   ├── ulimit@CentOSStream.txt                            # CentOS 的 ulimit 参数
│   └── ulimit@Unknown.txt                                 # Unknown 的 ulimit 参数
├── get_sysctl_ulimit_res.py                               # 获取参数、对比参数、统计参数的 Python 程序
├── LICENSE  
├── load_config.py                                         # 载入测试模式 config.json 配置文件
├── log                                                    # 每一个 Python 程序都会记录对应的 log
│   ├── get_sysctl_ulimit_2023-08-24-10-14-42.log
│   ├── load_config_2023-08-24-10-03-57.log
│   ├── load_config_2023-08-24-10-04-09.log
│   ├── load_config_2023-08-24-10-12-51.log
│   ├── load_config_2023-08-24-10-13-02.log
│   └── load_config_2023-08-24-10-14-45.log
├── main.py                                                # 从这里开始
├── OSPP data                                              # 日后会删除的文件夹
│   ├── systemctl@centos.txt
│   └── systemctl@openeuler.txt
├── __pycache__                                            # 缓存
│   ├── benchmark_test.cpython-39.pyc
│   ├── clean_data.cpython-39.pyc
│   ├── clean_log.cpython-39.pyc
│   ├── get_sysctl_ulimit_res.cpython-39.pyc
│   ├── load_config.cpython-39.pyc
│   ├── regex_prefix.cpython-39.pyc
│   └── set_parameters.cpython-39.pyc
├── README.md                                              # 读我
├── regex_prefix.py                                        # 使用 prefix.json 进行正则匹配或者查询
├── regex_test.txt                                         # 临时的测试文件
├── set_parameters.py                                      # 载入系统参数
└── tests                                                  # 单元回归测试
    ├── test_get_sysctl_ulimit_Res.py    
    └── test_regex_prefix.py

6 directories, 39 files
