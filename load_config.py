from datetime import datetime
import json
import paramiko
import getpass
import logging

#生成时间戳，用于文件命名
def generate_timestamp_string():
    now = datetime.now()
    timestamp_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    return timestamp_string

timestamp = generate_timestamp_string()

log_file = f'./log/load_config_{timestamp}.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)
logging.info('load_config.py start')

# 测试pc1与pc2的连通性
def connect_test(pc1, pc2):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # getpass.getpass() 用于隐藏输入的密码

        getpassword = getpass.getpass(f"请输入 {pc2['ip']} 的密码: ")
        logging.info('请输入 %s 的密码:',{pc2['ip']} , extra={'logfile': log_file})
        # 默认端口号为22
        ssh.connect(hostname=pc2['ip'], port=22, username=pc2['user'], password=getpassword)
        logging.info('%s 与 %s 连通性测试成功', {pc1['ip']}, {pc2['ip']}, extra={'logfile': log_file})
        print(f"{pc1['ip']} 与 {pc2['ip']} 连通性测试成功")
        ssh.close()
    except paramiko.AuthenticationException:
        logging.error('%s 与 %s 连通性测试失败：认证失败', pc1['ip'], pc2['ip'], extra={'logfile': log_file})
        print(f"{pc1['ip']} 与 {pc2['ip']} 连通性测试失败：0 认证失败")
    except paramiko.SSHException as e:
        logging.error('%s 与 %s 连通性测试失败：%s', pc1['ip'], pc2['ip'], str(e), extra={'logfile': log_file})
        print(f"{pc1['ip']} 与 {pc2['ip']} 连通性测试失败：1 {str(e)}")
    except Exception as e:
        logging.error('%s 与 %s 连通性测试失败：%s', pc1['ip'], pc2['ip'], str(e), extra={'logfile': log_file})
        print(f"{pc1['ip']} 与 {pc2['ip']} 连通性测试失败：2 {str(e)}")
    finally:
        ssh.close()

# host_test模式: 3台主机
def host_test_body(data) :

    local = {'ip': '', 'user': ''}  # 本机
    pc1 = {'ip': '', 'user': ''}    # pc1
    pc2 = {'ip': '', 'user': ''}    # pc2
    
    if not data["host_test"]["local"]["ip"]:
        logging.info('本机IP缺失', extra={'logfile': log_file})
        local['ip'] = input("请输入本机IP, 或者直接编辑config.json文件: ")
    if not data["host_test"]["local"]["user"]:
        logging.info('本机用户名缺失', extra={'logfile': log_file})
        local['user']= input("请输入本机用户名, 或者直接编辑config.json文件: ")

    if not data["host_test"]["pc1"]["ip"]:
        logging.info('pc1 IP缺失', extra={'logfile': log_file})
        pc1['ip'] = input("请输入pc1 IP, 或者直接编辑config.json文件:")
    if not data["host_test"]["pc1"]["user"]:
        logging.info('pc1 用户名缺失', extra={'logfile': log_file})
        pc1['user'] = input("请输入pc1 用户名, 或者直接编辑config.json文件: ")
    
    if not data["host_test"]["pc2"]["ip"]:
        logging.info('pc2 IP缺失', extra={'logfile': log_file})
        pc2['ip'] = input("请输入pc2 IP, 或者直接编辑config.json文件: ")
    if not data["host_test"]["pc2"]["user"]:
        logging.info('pc2 用户名缺失', extra={'logfile': log_file})
        pc2['user'] = input("请输入pc2 用户名, 或者直接编辑config.json文件: ")

    try:
        connect_test(local, pc1)
        logging.info('本机与pc1连通性测试成功', extra={'logfile': log_file})
    except Exception as e:
        logging.info('本机与pc1连通性测试失败', extra={'logfile': log_file})
        print("本机与pc1连通性测试失败")
    try:
        connect_test(local, pc2)
        logging.info('本机与pc2连通性测试成功', extra={'logfile': log_file})
    except Exception as e:
        logging.info('本机与pc2连通性测试失败', extra={'logfile': log_file})
        print("本机与pc2连通性测试失败")  
    try:
        connect_test(pc1, pc2)
        logging.info('pc1与pc2连通性测试成功', extra={'logfile': log_file})
    except Exception as e:
        logging.info('pc1与pc2连通性测试失败', extra={'logfile': log_file})
        print("pc1与pc2连通性测试失败")
    else:
        logging.info('无效的模式选择', extra={'logfile': log_file})
        print("无效的模式选择")

# communication_test模式: 2台主机 
def communication_test_body(data):

    local = data['communication_test']['local']
    remote = data['communication_test']['remote']
    if not data["communication_test"]["local"]["ip"]:
        logging.info('本机IP缺失', extra={'logfile': log_file})
        local['ip'] = input("请输入本机IP, 或者直接编辑config.json文件: ")
    if not data["communication_test"]["local"]["user"]:
        logging.info('本机用户名缺失', extra={'logfile': log_file})
        local['user']= input("请输入本机用户名, 或者直接编辑config.json文件: ")
    if not data["communication_test"]["remote"]["ip"]:
        logging.info('远程主机IP缺失', extra={'logfile': log_file})
        remote['ip'] = input("请输入远程主机IP, 或者直接编辑config.json文件: ")
    if not data["communication_test"]["remote"]["user"]:
        logging.info('远程主机用户名缺失', extra={'logfile': log_file})
        remote['user'] = input("请输入远程主机用户名, 或者直接编辑config.json文件: ")
    print("本机IP: ", local['ip'])
    print("本机用户名: ", local['user'])
    print("远程主机IP: ", remote['ip'])
    print("远程主机用户名: ", remote['user'])
    connect_test(local, remote)
    logging.info('本机与远程主机连通性测试成功', extra={'logfile': log_file})
    #except Exception as e:
    #    logging.info('本机与远程主机连通性测试失败', extra={'logfile': log_file})
    #    print("本机与远程主机连通性测试失败")
