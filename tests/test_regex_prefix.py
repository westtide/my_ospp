import re
import json
import pytest
import logging
import get_sysctl_ulimit_res

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



def parse_diff_file(file_path):
    dic = {}
    cla1 = ""
    cla2 = ""
    latest = {}

    with open(file_path, "r") as file:
        for line in file:
            if line.strip():
                if re.match(r"\*\*(.*?)\*\*", line) and not line.startswith("***"):
                    cla1 = line[2:-3]
                    dic[cla1] = {}
                    latest = dic[cla1]

                if re.match(r"\*\*\*(.*?)\*\*\*", line) and line.startswith("***"):
                    cla2 = line[3:-4]
                    dic[cla1][cla2] = {}
                    latest = dic[cla1][cla2]

                if not line.startswith("**"):
                    parts = line.strip().split(" ")
                    config_item = parts[0]
                    define = parts[-1]
                    value = " ".join(parts[1:-1]).strip()
                    latest[config_item] = {"value": value, "define": define}

    return dic

def save_json(data, file_path):
    json_string = json.dumps(data, indent=4, ensure_ascii=False)
    with open(file_path, "w") as json_file:
        json_file.write(json_string)

# 编写测试用例
def test_parse_diff_file():
    expected_data = {
        "class1": {
            "class2": {
                "config_item1": {"value": "value1", "define": "define1"},
                "config_item2": {"value": "value2", "define": "define2"}
            }
        }
    }
    actual_data = parse_diff_file("data/diff-res.txt")
    assert actual_data == expected_data

def test_save_json(tmp_path):
    data = {
        "class1": {
            "class2": {
                "config_item1": {"value": "value1", "define": "define1"},
                "config_item2": {"value": "value2", "define": "define2"}
            }
        }
    }
    file_path = tmp_path / "test.json"
    save_json(data, file_path)
    assert file_path.exists()

# 运行测试用例
pytest
