from googletrans import LANGUAGES
from translate import Translator

import os
from os import listdir
from os.path import isfile, join

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium.webdriver.remote.webelement

import time


def translate_by_gg_translate(text):
    url = "https://translate.google.com/?hl=vi&sl=en&tl=vi&op=translate"
    # Đường dẫn tới ChromeDriver
    chromedriver_path = 'chromedriver/chromedriver.exe'
    service = webdriver.chrome.service.Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    input_text = driver.find_element(By.CLASS_NAME, "er8xn")
    print(text)
    input_text.send_keys(text)

    # Wait for google is transling
    time.sleep(2)

    translated_text = ""

    span_list = driver.find_elements(By.CLASS_NAME, "ryNqvb")
    for span in span_list:
        # translated_text.append(span.text)
        translated_text = translated_text + span.text + "\n"

    driver.quit()
    return translated_text


# Translator
# translator_mymemory = Translator(to_lang="vi", provider='mymemory')
# translator_microsoft = Translator(to_lang="vi", provider='microsoft')
# translator_deepl = Translator(to_lang="vi", provider='deepl')
# translator_libre = Translator(to_lang="vi", provider='libre')


def change_extension(file_path, new_extension):
    base_name, _ = os.path.splitext(file_path)
    new_file_path = base_name + "." + new_extension
    os.rename(file_path, new_file_path)


def read_file_to_list(file_path):
    # Tạo danh sách rỗng để lưu trữ các dòng từ tệp tin
    lines = []

    # Mở tệp tin với chế độ đọc (read mode)
    with open(file_path, 'r', encoding='utf-8') as file:
        # Đọc từng dòng trong tệp tin và thêm vào danh sách
        for line in file:
            # Loại bỏ ký tự xuống dòng (\n) ở cuối mỗi dòng
            lines.append(line.strip())

    return lines


def clear_file(file_path):
    with open(f"{file_path}", 'w', encoding='utf-8') as file:
        file.write('')


def get_text_from_list(list):
    new_list = []
    for index, item in enumerate(list):
        if ((index + 2) % 4) == 0:
            new_list.append(item.strip())

    return new_list


def get_extensions_files(path_folder_input, extensions):
    # Get all file name in folder input
    folder_input = os.listdir(path_folder_input)
    srt_files = [file for file in folder_input if file.endswith(
        '.' + f"{extensions}")]
    return srt_files


# Change file extention
# for file in folder_input:
#     change_extension(path_folder_input + file, "txt")


# def process_srt_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     with open(file_path, 'w', encoding='utf-8') as file:
#         # Đọc từng dòng trong tệp tin và thêm vào danh sách
#         for index, text in enumerate(lines):
#             if ((index + 2) % 4) == 0:
#                 # Loại bỏ ký tự xuống dòng (\n) ở cuối mỗi dòng
#                 translated = translator_mymemory.translate(text)
#                 # print(translated.strip())
#                 file.write(translated)
#             else:
#                 # print(text.strip())
#                 file.write(text)


def get_5000_word(index_current, text_file):
    word_count = 0
    for index, text in enumerate(list_text_need_translate):
        # print(index)
        words_in_text = len(text)
        # Check if add word_in_text > 5000 then break
        if word_count + words_in_text + 1 >= 5000:
            index_current = index
            return index_current, text_file

        if index >= index_current:
            text_file = text_file + text + "\n"
            word_count = word_count + words_in_text + 1

    return -1, text_file


# Path to the folder input
path_folder_input = "e:/Project/Python/translate/input/"
folder_input = get_extensions_files(path_folder_input, "srt")

file_text = read_file_to_list(path_folder_input + folder_input[6])

list_text_need_translate = get_text_from_list(file_text)

index_current = 0

test_txt_path = "e:/Project/Python/translate/output/test.txt"
clear_file(test_txt_path)

while index_current != -1:
    text_file = ""
    index_current, text_file = get_5000_word(index_current, text_file)
    translated_text = translate_by_gg_translate(text_file)
    print(translated_text)
    # with open(test_txt_path, 'a') as file:
    #     file.write(translated_text)


# index_current1 = 0
# text_file1 = ""
# index_current1, text_file1 = get_5000_word(index_current1, text_file1)
# with open("e:/Project/Python/translate/output/test.txt", 'w') as file:
#     file.write(text_file1.strip())


# for text in list_text_need_translate:
#     translation_mymemory = translator_mymemory.translate(text)
#     # translation_microsoft = translator_microsoft.translate(text)
#     # translation_libre = translator_libre.translate(text)
#     # translation_deepl = translator_deepl.translate(text)
#     print(translation_mymemory)
