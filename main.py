# This is the script to process submissions for CS 121 class and run moss on it
import os, zipfile, glob, pathlib, shutil
from pathlib import Path
from zipfile import ZipFile
from tqdm import tqdm
original_all_submission_dir = "/Users/qihongchen/Desktop/submissions/"


def unzip_submissions():
    for zip_file_name in os.listdir(original_all_submission_dir):
        if not zipfile.is_zipfile(original_all_submission_dir + zip_file_name):
            continue

        result_folder_name = zip_file_name.split('.')[0].strip()
        result_folder_name_list = result_folder_name.split("_")
        result_folder_name = "".join(result_folder_name_list[:2])
        result_unzipped_folder = unzipped_submissions_dir + result_folder_name + '/'
        os.mkdir(result_unzipped_folder)
        zip_file_dir = original_all_submission_dir + zip_file_name
        with ZipFile(zip_file_dir, 'r') as zip_obj:
            for file in zip_obj.namelist():
                zip_obj.extract(file, result_unzipped_folder)


def preprocess_submissions():
    for unzipped_submission_name in tqdm(os.listdir(unzipped_submissions_dir)):
        if not os.path.isdir(unzipped_submissions_dir + unzipped_submission_name + '/'):
            continue
        final_result_folder_name = preprocess_submissions_dir + str(unzipped_submission_name) + '/'
        os.mkdir(final_result_folder_name)
        for py_file_dir in pathlib.Path(unzipped_submissions_dir + unzipped_submission_name + '/').glob('**/*.py'):
            if not str(py_file_dir).endswith('.py') or "__MACOSX" in str(py_file_dir):
                continue
            print("from ", py_file_dir, " to ", final_result_folder_name)
            shutil.copy(py_file_dir, final_result_folder_name)

def run_moss():
    os.system("perl moss.pl -d {}".format(preprocess_submissions_dir) + '/*/*.py')


if __name__ == '__main__':
    unzipped_submissions_dir = "/Users/qihongchen/Desktop/unzipped_submissions/"
    os.mkdir(unzipped_submissions_dir)
    unzip_submissions()
    preprocess_submissions_dir = "/Users/qihongchen/Desktop/preprocess_submissions/"
    os.mkdir(preprocess_submissions_dir)
    preprocess_submissions()
    run_moss()
