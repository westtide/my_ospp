import paramiko 
import
def connect_test(pc1, pc2):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # getpass.getpass() 用于隐藏输入的密码
        getpassword = getpass.getpass(f"请输入 {pc1.ip} 的密码: ")
        logging.info('请输入 %s 的密码:',{pc1.ip} , extra={'logfile': log_file})

        # 默认端口号为22
        ssh.connect(hostname=pc1.ip, port=22, username=pc1.user, password=getpassword)
        ssh.close()
        logging.info('%s 与 %s 连通性测试成功', {pc1.ip}, {pc2.ip}, extra={'logfile': log_file})
        print(f"{pc1.ip} 与 {pc2.ip} 连通性测试成功")
    except Exception as e:
        logging.error('%s 与 %s 连通性测试失败', {pc1.ip}, {pc2.ip}, extra={'logfile': log_file})
        print(f"{pc1.ip} 与 {pc2.ip} 连通性测试失败")
        print(e)
