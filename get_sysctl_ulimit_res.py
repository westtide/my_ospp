import subprocess
import re
import difflib
import random
import string
from datetime import datetime
import logging

#生成时间戳，用于文件命名
def generate_timestamp_string():
    now = datetime.now()
    timestamp_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    return timestamp_string

timestamp = generate_timestamp_string()

log_file = f'./log/get_sysctl_ulimit_{timestamp}.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)
logging.info('This is a log message')

#获取 linux 版本，CentOS Steam 或者 OpenEuler
def get_linux_version():
    linux_version = "Unknown"
    try:
        with open("/etc/os-release", "r") as file:
            for line in file:
                if line.startswith("NAME="):
                    linux_version = line.strip().split("=")[1].strip('"').replace(" ", "")
                    logging.info('获取系统版本为 %s', linux_version, extra={'logfile': log_file})
                    break
    except FileNotFoundError:
        logging.error('failed: \'cat /etc/os-release\' ', extra={'logfile': log_file})
        print("未找到 /etc/os-release 文件，请检查文件是否存在。")
    
    return linux_version

#bash: "syscyl -a" 存储在sysctl@$linux-version$中
def run_sysctl_command_and_save_result(file_name):
    bash_command = "sysctl -a"
    with open(file_name, "w") as output_file:
        process = subprocess.Popen(bash_command, shell=True, stdout=output_file, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        logging.info('run command \'%s\'', bash_command, extra={'logfile': log_file})
        if process.returncode != 0:
            print(f"命令执行出错：{stderr.decode()}")
            logging.error('failed: run command \'%s\' ', bash_command, extra={'logfile': log_file})

#bash: "ulimit -a" 存储在ulimit@$linux-version$中
def run_ulimit_command_and_save_result(file_name):
    bash_command = "ulimit -a"
    with open(file_name, "w") as output_file:
        process = subprocess.Popen(bash_command, shell=True, stdout=output_file, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        logging.info('run command \'%s\'', bash_command, extra={'logfile': log_file})
        if process.returncode != 0:
            print(f"命令执行出错：{stderr.decode()}")
            logging.error('failed: run command \'%s\' ', bash_command, extra={'logfile': log_file})


#Example or Test：用于查找 net.ipv4 开头的项目,并输出
def find_net_ipv4_items(file_path):
    net_ipv4_items = []
    pattern = r'^net\.ipv4\..*'

    with open(file_path, "r") as file:
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                net_ipv4_items.append(line.strip())
    print("开头为\"net.ipv4\"的项目,共有 " + str(len(net_ipv4_items)) + " 项")
    for item in net_ipv4_items:
        print(item)

#使用 difflib 比较两个文件,返回 result
def compare_sysctl_configs(file1, file2):
    with open("./data/"+file1) as f1, open("./data/"+file2) as f2:
        logging.info('compare file1 = \'%s\', file2 = \'%s\'',"./data/"+file1,"./data/"+file2, extra={'logfile': log_file})
        text1 = f1.readlines()
        text2 = f2.readlines()
        logging.info('text1 in \'%s\', text2 in \'%s\'',"./data/"+file1, "./data/"+file2,extra={'logfile': log_file})
    diff=difflib.Differ()
    diff_result = diff.compare(text1, text2)
    logging.info('compare file1 and file2 by difflib successfully', extra={'logfile': log_file})   
    return '\n'.join(diff_result)

#保存比较结果diff_result到文件save_difflib_res
def save_diff_comparison_to_file(diff_result, save_difflib_res):
    try:
        with open("./data/"+save_difflib_res, 'w') as file:
            file.write(diff_result)
        logging.info('save diff_result to file \'%s\' successfully', "./data/"+save_difflib_res, extra={'logfile': log_file})
        print(f"比较结果已成功保存到文件: ./data/{save_difflib_res}")
    except IOError:
        logging.error('failed: save diff_result to file \'%s\' ', "./data/"+save_difflib_res, extra={'logfile': log_file})
        print("保存文件时出现错误，请检查路径和文件权限。")


sys_version = get_linux_version()
sysctl_res_file_name = "sysctl@" + sys_version + ".txt"
ulimit_res_file_name = "ulimit@" + sys_version + ".txt"
save_difflib_res = f"differ-{timestamp}.txt"
save_statistical_res = f"statistical-{timestamp}.txt"

logging.info("sysctl_res_file_name = \'%s\',ulimit_res_file_name = \'%s\',save_difflib_res = \'%s\',save_statistical_res = \'%s\' ",
             sysctl_res_file_name,ulimit_res_file_name,save_difflib_res,save_statistical_res,
             extra={'logfile': log_file})

# 执行sysctl -a命令并保存结果到sysctl@xxx.txt文件中
run_sysctl_command_and_save_result("./data/"+sysctl_res_file_name)
logging.info('run_sysctl_command_and_save_result successfully, save in \'%s\'',"./data/"+sysctl_res_file_name, extra={'logfile': log_file})
# 执行ulimit -a命令并保存结果到ulimit@xxx.txt文件中
run_ulimit_command_and_save_result("./data/"+ulimit_res_file_name)
logging.info('run_ulimit_command_and_save_result successfully, save in \'%s\'',"./data/"+ulimit_res_file_name, extra={'logfile': log_file})

# 使用difflib的比较结果
file1 = sysctl_res_file_name
if sys_version == "CentOSStream":
    command = "scp west2@172.22.60.29:~/my_ospp/sysctl@openEuler.txt ./data/ "
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"执行命令出错：{e}")
    file2 = "sysctl@openEuler.txt"
else:
        command = "scp west1@172.22.60.34:~/my_ospp/sysctl@CentOSStream.txt ./data/ "
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"执行命令出错：{e}")
        file2 = "sysctl@CentOSStream.txt"
diff_result = compare_sysctl_configs(file1, file2)

# 保存difflib比较结果到文件
save_diff_comparison_to_file(diff_result, save_difflib_res)

# 保存比较结果到文件
def save_result_to_file(file2lack_dict, file2add_dict, file2modify_dict, file1, file2, file2lack, file2add, file2modify):
    result_str = ""
    result_str += "file1: " + file1 + ", file2: " + file2 + " 统计结果为：\n"
    result_str += "file2 缺失的行有: " + str(len(file2lack)) + "行\n"
    result_str += "file2 增加的行有: " + str(len(file2add)) + "行\n"
    result_str += "file2 修改的行有: " + str(len(file2modify)) + "行\n"
    result_str += "====================================================================\n"
    result_str += "file2 缺失的行有：\n"
    for k, v in file2lack_dict.items():
        result_str += k + " " + v + "\n"
    result_str += "====================================================================\n"
    result_str += "file2 增加的行有：\n"
    for k, v in file2add_dict.items():
        result_str += k + " " + v + "\n"
    result_str += "====================================================================\n"
    result_str += "file2 修改的行有：\n"
    for k, v in file2modify_dict.items():
        result_str += k + " " + v + "\n"

    try:
        with open("./data/"+save_statistical_res, "w") as file:
            file.write(result_str)
        print("统计结果已成功保存到文件: "+save_statistical_res)
    except IOError:
        print("保存文件时出现错误，请检查路径和文件权限。")



# 统计比较结果:列表格式
file2lack = []
file2modify = []
file2add = []

# 读取比较结果文件
with open("./data/"+save_difflib_res) as f:
    lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith('-'):
            if lines[i + 2].startswith('-') or lines[i + 2].startswith(' '):
                file2lack.append(line.strip())
            elif lines[i + 2].startswith('+'):
                file2modify.append(line.strip())
            elif lines[i + 2].startswith('?'):
                if lines[i + 4].startswith('+') and lines[i + 6].startswith('?'):
                    #!#
                    file2modify.append(line.strip())
        elif line.startswith('+'):
            file2add.append(line.strip())

# 统计比较结果:字典格式
file2lack_dict = {line.strip('-+ \n').split('=', 1)[0]: line.strip('-+ \n').split('=', 1)[1].strip() for line in file2lack}
file2add_dict = {line.strip('-+ \n').split('=', 1)[0]: line.strip('-+ \n').split('=', 1)[1].strip() for line in file2add}
file2modify_dict = {line.strip('-+ \n').split('=', 1)[0]: line.strip('-+ \n').split('=', 1)[1].strip() for line in file2modify}

# 打印统计结果
print("file1: " + file1 + ", file2: " + file2 + " 统计结果为：")
print("file2 缺失的行有: " + str(len(file2lack)) + "行")
print("file2 增加的行有: " + str(len(file2add)) + "行")
print("file2 修改的行有: " + str(len(file2modify)) + "行")


# 在原来的代码末尾，添加调用保存结果到文件的函数
save_result_to_file(file2lack_dict, file2add_dict, file2modify_dict, file1, file2, file2lack, file2add, file2modify)
