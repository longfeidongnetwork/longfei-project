import os
import shutil
import wave

import pymysql

from quality_inspection.settings import absolute_path


# 数据库连接
def connect_mysql():
    """
    前期为了方便写sql有缺点，后期使用orm查询方式
    :return: con
    """
    con = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Mysql@123",
        database="quality_inspection",
        charset="utf8"
    )
    return con


# 创建文件夹方法
def mkdir_directory(path):
    """
    创建目录
    :param path:
    :return: boolean
    """
    # 去除首尾空格
    path = path.strip()
    # 判断目录是否存在
    folder = os.path.exists(path)
    if not folder:
        # 如果不存在，则创建新目录
        os.makedirs(path)
        return True
    else:
        print("目录已存在")
        return False


# 修改文件夹方法
def update_directory(src, dst):
    """
    修改目录名
    :param src:
    :param dst:
    :return: boolean
    """
    try:
        print(src, dst)
        src_path = absolute_path + src
        dst_path = absolute_path + dst
        os.rename(src_path, dst_path)
    except Exception as e:
        print(e)
        return False
    return True


# 删除文件夹
def delete_directory(value):
    """
    删除目录
    :param value:
    :return: boolean
    """
    try:
        path = os.path.join(absolute_path, value)
        print(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
    except Exception as e:
        print(e)
        return False
    return True


# 字节转换
def conversion_size(size):
    """
    将字节转换
    :param size:
    :return:
    """
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    tb = gb * 1024
    if size >= tb:
        return "%.1fT" % float(size / tb)
    if size >= gb:
        return "%.1fG" % float(size / gb)
    if size >= mb:
        return "%.2fM" % float(size / mb)
    if size >= kb:
        return "%.0fK" % float(size / kb)


# 时长计算
def calculate_duration(object):
    """
    计算音频的时长，格式化为秒
    :param object:
    :return:wav_length
    """
    with wave.open(object, 'rb') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        # wav_length = frames / float(rate)
        wav_length = round(frames / float(rate), )
        print(object, "音频长度：", wav_length, "秒")
    return wav_length


# 遍历目录下所有文件
def get_file(directory, path):
    """
    获取该目录下的所有文件
    :param directory: 目录名
    :param path: 目录名上一层路径
    :return:file_list
    """
    path = os.path.join(path, directory)
    file_list = []
    for file_path, dir_names, file_names in os.walk(path):
        for file in file_names:
            file_name = os.path.join(file_path, file)
            file_list.append(file_name)
    return file_list


def seek_files(name, path):
    """
    根据文件名找到文件全路径
    :param name: 文件名
    :param path: 文件目录
    :return: file_list 文件全路径
    """
    for root, dirs, files in os.walk(path):
        file_list = []
        for file in files:
            if name in file:
                file_name = os.path.join(root, file)
                file_list.append(file_name)
    return file_list


