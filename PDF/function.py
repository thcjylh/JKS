import os
from PyPDF2 import PdfFileMerger
import time
import shutil


def list_dir(files_path):  # 获取路径下所有文件名
    files_dir = []
    for file_name in os.listdir(files_path):
        file_dir = files_path + file_name
        if os.path.isfile(file_dir):
            files_dir.append(file_dir)
    return files_dir


def file_is_pdf(file_list):  # 留下文件夹内某一类型的文件
    file_type = '.pdf'  # 留下文件的类型
    for i in range(0, len(file_list)):
        file_path = file_list[i]
        if os.path.splitext(file_path)[1] != file_type:
            os.renames(file_path, os.path.dirname(file_path) + '/Temp/' + os.path.basename(file_path))
    return


def rename_as_create_time(file_list):  # 获取文件的创建时间
    for i in range(0, len(file_list)):
        file_path = file_list[i]
        create_time = str.format('{:.5f}', os.path.getctime(file_path))[-12:]
        os.rename(file_path, os.path.dirname(file_path) + '/' + create_time + os.path.splitext(file_path)[1])
    return


def backup_pdf(file_list, n_time):
    new_path = ''
    if len(file_list) > 0:
        new_path = os.path.dirname(file_list[0]) + '/backup/' + n_time + '/'
        os.makedirs(new_path)
    for i in range(0, len(file_list)):
        file_path = file_list[i]
        shutil.copyfile(file_path, new_path + os.path.basename(file_path))
    return


def merge_pdf(file_list, out_file):  # 结合PDF
    if len(file_list) > 0:
        pdf_merge = PdfFileMerger()
        for pdf in file_list:
            pdf_merge.append(pdf)
        pdf_merge.write(out_file)
        pdf_merge.close()
        for i in range(0, len(file_list)):
            os.remove(file_list[i])
    return


def main(path):
    now_time = 'merge ' + time.strftime('%y-%m-%d %H%M%S', time.localtime())
    file_is_pdf(list_dir(path))
    temp = list_dir(path)
    backup_pdf(temp, now_time)
    rename_as_create_time(temp)
    temp = list_dir(path)
    merge_pdf(temp, path + '/' + now_time + '.pdf')
