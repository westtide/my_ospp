import re
import json
dic = {}
cla1 = ""
cla2 = ""
latest = {}
with open ("data/diff-res.txt", "r") as file:
    for line in file:
        if line.strip():
            if re.match(r"\*\*(.*?)\*\*" , line) and not line.startswith("***") :
                print("1类: " + line[2:-3])
                cla1 = line[2:-3]
                dic[cla1] = {}
                latest = dic[cla1]

            if re.match(r"\*\*\*(.*?)\*\*\*", line) and line.startswith("***"):
                print("  2类: " +line[3:-4])
                cla2 = line[3:-4]
                dic[cla1][cla2] = {}
                latest = dic[cla1][cla2]

            if not line.startswith("**"):
                parts = line.strip().split(" ")
                config_item = parts[0]
                define = parts[-1]
                value = " ".join(parts[1:-1]).strip()
                print("    3类: " + config_item  + " " + value + " " + define)
                latest[config_item]= {"value":value, "define":define} 


# 将字典转换为 JSON 字符串
json_string = json.dumps(dic, indent=4, ensure_ascii=False)  

with open("config/sysyctl_paraments.json", "w") as json_file:
    json_file.write(json_string)