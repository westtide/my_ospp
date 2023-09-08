import datetime
import pytest
import logging
import subprocess
import difflib
import get_parameters as my_module

#生成时间戳，用于文件命名
def generate_timestamp_string():
    now = datetime.now()
    timestamp_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    return timestamp_string

timestamp = generate_timestamp_string()

log_file = f'./log/test-{timestamp}.log'
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)
logging.info('This is a log message')

def run_command_and_save_result(command, file_name):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            logging.error(f'failed: run command \'{command}\'')
            raise Exception(f"命令执行出错：{stderr.decode()}")
        with open(file_name, "w") as output_file:
            output_file.write(stdout.decode())
        logging.info(f'run command \'{command}\' and save result to file \'{file_name}\'')
    except Exception as e:
        logging.error(str(e))
        raise

def compare_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        text1 = f1.readlines()
        text2 = f2.readlines()
    diff = difflib.Differ()
    diff_result = diff.compare(text1, text2)
    return '\n'.join(diff_result)

@pytest.fixture
def setup_logging():
    logging.basicConfig(level=logging.INFO)

def test_run_command_and_save_result(setup_logging, tmp_path):
    file_name = tmp_path / "test_file.txt"
    command = "echo 'Hello, world!'"
    my_module.run_command_and_save_result(command, file_name)
    assert file_name.exists()

def test_compare_files(tmp_path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("line1\nline2\n")
    file2.write_text("line1\nline3\n")
    diff_result = my_module.compare_files(file1, file2)
    assert "- line2\n?       ^\n+ line3\n?       ^" in diff_result


