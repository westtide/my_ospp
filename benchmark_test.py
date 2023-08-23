import subprocess

command = "-a"
package1 = "ulimit"
try:
    subprocess.run([package1, command], check = True)
except subprocess.CalledProcessError:
    print("'{package1 command}' 命令执行失败，请检查命令是否正确。")
    exit(1)