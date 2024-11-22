import configparser
import os
import pathlib
import shutil
from time import sleep

import pandas as pd

from log_handler import custom_logger

log = custom_logger()
pd.set_option('mode.chained_assignment', None)


def create_folder(directory_path):
    """
    function to create folder
    :param directory_path: path of the directory including directory name
    :return:
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    except OSError:
        log.error('Error: Creating directory. ' + directory_path)


def file_downloaded_is_complete(directory_path, new_file_name):
    """
    Method to verify if the file download into a user provided directory is completed
    :param directory_path:
    :param new_file_name:
    :return: None if download is completed
    """
    f_name = None
    try:
        file_ends = "crdownload"
        while "crdownload" in file_ends:
            for f_name in os.listdir(directory_path):
                if os.path.isfile(os.path.join(directory_path, f_name)):
                    if f_name.endswith(".crdownload"):
                        file_ends = "crdownload"
                    else:
                        file_ends = "None"
                        shutil.move(os.path.join(directory_path, f_name),
                                    os.path.join(directory_path, new_file_name))
    except FileNotFoundError:
        sleep(10)
        shutil.move(os.path.join(directory_path, f_name),
                    os.path.join(directory_path, new_file_name))


def load_config_file(file_path, section, key):
    """
    function to read values from config file
    :param file_path: configuration file path
    :param section: string
    :param key: string
    :return: string value corresponding to section header and key
    """
    value = None
    try:
        config = configparser.RawConfigParser()
        config.read(file_path)
        value = config.get(section, key)
    except IOError as e:
        log.error("IO error while reading from properties file".format(e))
    return value


def get_file_paths_from_dirs(high_level_dir_path, file_extension):
    """
    Method to get all the pdf file
    :param high_level_dir_path:
    :param file_extension:
    :return:
    """
    try:
        out_df = pd.DataFrame()
        file_paths = list(pathlib.Path(high_level_dir_path).glob('**/*.{}'.format(file_extension)))
        i = 0
        for fn in file_paths:
            arr = fn.name.split("_")
            out_df.loc[i, 'Request No'] = arr[0]
            i = i + 1
        out_df.to_excel('output.xlsx', index=False)
    except FileExistsError:
        return None


def get_path(filename):
    """
    method to get the absolute file path of the file name
    :param filename:
    :return:
    """
    p = pathlib.Path(filename)
    return os.path.join(os.getcwd(), "resources", p.name)


def get_file_path_from_dir(dir_name, partial_file_name):
    """
    method to get the file path from partial file name
    :param dir_name: folder name under current working directory
    :param partial_file_name: either a partial file name or list of extensions
    :return: absolute file path including file extension
    """
    import glob
    try:
        file_path = []
        location = os.path.join(os.getcwd(), dir_name, "*{}*".format(partial_file_name))
        for name in glob.glob(location):
            file_path.append(name)
            return file_path[0]
    except FileExistsError:
        return ""


def check_and_delete_dir(dir_path):
    """
    method to check and delete directory
    :param dir_path:
    :return:
    """
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    :param num:
    :return: size of file
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    method to return the file size
    :param file_path:
    :return: file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def rename_file_extension(file_path, new_extn):
    """
    method to rename the file extension
    :param file_path: absolute file path
    :param new_extn: file extension
    :return: None
    """
    base = os.path.splitext(file_path)[0]
    os.rename(file_path, base + new_extn)
