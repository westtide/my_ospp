import subprocess
import logging

def run_command(command, parameter, log_file):
    try:
        subprocess.run([command, parameter], check = True)
        logging.info('run command \'%s\' successfully', command, extra={'logfile': log_file})
    except subprocess.CalledProcessError:
        print("'{command parameter}' 命令执行失败，请检查命令是否正确。")
        exit(1)