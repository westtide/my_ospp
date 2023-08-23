import json
import paramiko
import getpass

# 测试pc1与pc2的连通性
def connect_test(pc1, pc2):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # getpass.getpass() 用于隐藏输入的密码
        getpassword = getpass.getpass(f"请输入 {pc1.ip} 的密码: ")
        # 默认端口号为22
        ssh.connect(hostname=pc1.ip, port=22, username=pc1.user, password=getpassword)
        ssh.close()
        print(f"{pc1.ip} 与 {pc2.ip} 连通性测试成功")
    except Exception as e:
        print(f"{pc1.ip} 与 {pc2.ip} 连通性测试失败")
        print(e)

with open('config/config.json') as f:
    data = json.load(f)

# 选择测试模式
selected_mode = input("请选择测试模式 (host_test 或 communication_test): ")

# host_test模式: 3台主机
if selected_mode == 'host_test':
    mode = selected_mode
    config = data[mode]  # 获取选定模式的配置
    local = {'ip': '', 'user': ''}  # 本机
    pc1 = {'ip': '', 'user': ''}    # pc1
    pc2 = {'ip': '', 'user': ''}    # pc2
    
    if not data[mode]["local"]["ip"]:
        local['ip'] = input("请输入本机IP, 或者直接编辑config.json文件: ")
    if not data[mode]["local"]["user"]:
        local['user']= input("请输入本机用户名, 或者直接编辑config.json文件: ")

    if not data[mode]["pc1"]["ip"]:
        pc1['ip'] = input("请输入pc1 IP, 或者直接编辑config.json文件:")
    if not data[mode]["pc1"]["user"]:
        pc1['user'] = input("请输入pc1 用户名, 或者直接编辑config.json文件: ")
    
    if not data[mode]["pc2"]["ip"]:
        pc2['ip'] = input("请输入pc2 IP, 或者直接编辑config.json文件: ")
    if not data[mode]["pc2"]["user"]:
        pc2['user'] = input("请输入pc2 用户名, 或者直接编辑config.json文件: ")

    try:
        connect_test(local, pc1)
        connect_test(local, pc2)
        connect_test(pc1, pc2)
    except Exception as e:
        print(e)
else:
    print("无效的模式选择")

# communication_test模式: 2台主机
if selected_mode == 'communication_test':
    mode = selected_mode
    config = data[mode]  # 获取选定模式的配置
    local = {'ip': '', 'user': ''}
    remote = {'ip': '', 'user': ''}
    if not data[mode]["local"]["ip"]:
        local['ip'] = input("请输入本机IP, 或者直接编辑config.json文件: ")
    if not data[mode]["local"]["user"]:
        local['user']= input("请输入本机用户名, 或者直接编辑config.json文件: ")
    
    if not data[mode]["remote"]["ip"]:
        remote['ip'] = input("请输入远程主机IP, 或者直接编辑config.json文件: ")
    if not data[mode]["remote"]["user"]:
        remote['user'] = input("请输入远程主机用户名, 或者直接编辑config.json文件: ")
    
    try:
        connect_test(local, remote)
    except Exception as e:
        print(e)
