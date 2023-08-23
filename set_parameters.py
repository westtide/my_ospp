def matching_parameters(file_path):
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
