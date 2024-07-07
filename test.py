from googletrans import Translator
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import urllib.parse


def rgba_to_rgb(hex_color):
    # Assuming a white background, so the background RGB is (255, 255, 255)
    background_r, background_g, background_b = 255, 255, 255

    # Extract RGBA from hex
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    a = int(hex_color[7:9], 16) / 255.0  # Convert to a scale of 0 pto 1

    # Calculate new RGB by blending the original color with the background
    new_r = round((1 - a) * background_r + a * r)
    new_g = round((1 - a) * background_g + a * g)
    new_b = round((1 - a) * background_b + a * b)

    # Convert RGB back to hex
    return f"#{new_r:02X}{new_g:02X}{new_b:02X}"


def transform_string(input_string):
    replacements = [(":", ""), ("@", ""), ("®", ""), ("®", ""), ("'s", "")]
    for old, new in replacements:
        input_string = input_string.replace(old, new)
    transformed_string = input_string.lower().replace(' ', '-')
    return transformed_string


def transform_string_no_space(input_string):
    replacements = [("\n", ""), (' ', ""), ("\t", "")]
    for old, new in replacements:
        input_string = input_string.replace(old, new)
    return input_string


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


# Mở file ở chế độ ghi (write mode)
# with open('pythontest\\ha1.txt', 'w') as file:
#    for i in range(19):
#        # Tính chữ cái tương ứng
#         char = chr(ord('a') + i)
#         # Nếu không phải là lần lặp cuối cùng, thêm '\n'
#         if i < 18:
#             file.write(char + '\n')
#         else:
#             file.write(char)


def convert_urls(urls):
    new_urls = []
    for url in urls:
        parts = url.split('/')
        app_id = parts[4]
        new_url = f"https://steamdb.info/app/{app_id}/"
        new_urls.append(new_url)
    return new_urls


def convert_urls_to_us(urls):
    new_urls = []
    for url in urls:
        parts = url.split('/')
        app_id = parts[4]
        app_name = parts[5]
        new_url = f"https://store.steampowered.com/app/{
            app_id}/{app_name}/?cc=us"
        new_urls.append(new_url)
    return new_urls


def convert_github_url(urls):
    new_urls = []
    for url in urls:
        parts = url.split('/')
        app_id = parts[3]
        app_name = parts[4]
        new_url = f"htmlpreview.github.io/?https://github.com/{
            app_id}/{app_name}"
        new_urls.append(new_url)
    return new_urls


f = "pythontest\\ha.txt"
f1 = "pythontest\\ha1.txt"

colors = [
    "#a86cb64d",
]
input_string = [
    "Diablo® IV",
]
lines_list = read_file_to_list(f)
lines_list1 = read_file_to_list(f1)

# print(lines_list)

# for color in colors:
#     converted = rgba_to_rgb(color)
#     print(f"{color} -> {converted}")

# for i in lines_list:
#     result = transform_string(i)
#     lines_list[i] = result

# list = transform_string("Zenless Zone Zero")

# for index in range(len(lines_list)):
#     result = transform_string(lines_list[index])
#     lines_list[index] = result

# print(list)
# print(lines_list1)

# folder_path = 'img\\article\\ha'


# # Mở file trong chế độ ghi (write mode)
# with open(folder_path, 'w') as file:
#     # Duyệt qua từng phần tử trong danh sách
#     for item in lines_list:
#         # Ghi phần tử vào file, mỗi phần tử trên một dòng
#         file.write(f"{item}\n")


# for i in range(1, 20):
#     create_file = open(f'pythontest\\{i}.txt', 'w')

# _, _, files = next(os.walk("img\\article\\ha"))
# file_count = len(files)
# print(file_count)


# if len(lines_list) != file_count:
#     print("Số lượng tên file mới không khớp với số lượng file trong thư mục.")
# else:
#     files = os.listdir(folder_path)
#     files.sort()  # Sắp xếp danh sách file theo thứ tự chữ cái
#     # Lặp qua từng file trong thư mục và đổi tên
#     for i, file_name in enumerate(files):
#         old_path = os.path.join(folder_path, file_name)
#         # Lấy phần mở rộng của file cũ
#         extension = os.path.splitext(file_name)[1]
#         # Tạo đường dẫn mới với tên mới và phần mở rộng cũ
#         new_path = os.path.join(folder_path, lines_list[i] + extension)
#         os.rename(old_path, new_path)


file_link = "pythontest\\name\\converted_link_to_us.txt"
link_list = read_file_to_list(file_link)


def get_content_from_url(link_list, selector, value, data, path):
    with open('pythontest\\name\\content\\' + f"{path}", 'w', encoding='utf-8') as file:
        file.write('')
    for url_link in link_list:
        response = requests.get(url_link)
        if response.status_code == 200:
            # Phân tích cú pháp HTML của trang web
            soup = BeautifulSoup(response.content, 'html.parser')
            # Lấy nội dung của phần tử theo id, class, hoặc tag
            if (data == '0'):
                element = soup.find('div', {f"{selector}": f"{value}"})
                if element:
                    # Lấy nội dung text của phần tử
                    content = element.get_text().strip()
                    with open('pythontest\\name\\content\\' + f"{path}", 'a', encoding='utf-8') as file:
                        file.write(content + '\n')
                        print("Đã ghi " + f"{content}")
                    # Ghi nội dung vào file txt
                else:
                    with open('pythontest\\name\\content\\' + f"{path}", 'a', encoding='utf-8') as file:
                        file.write('\n')
                        print("Đã ghi \"\"")
            else:
                element = soup.find('div', {f"{data}": True})
                if element:
                    if element.has_attr('aria-label'):
                        element_child = element.find(
                            'div', {f"{selector}": f"{value}"})
                        content = element_child.get_text()
                        with open('pythontest\\name\\content\\' + f"{path}", 'a', encoding='utf-8') as file:
                            file.write(content + '\n')
                            print("Đã ghi " + f"{content}")
                    else:
                        content = element.get_text().strip()
                        with open('pythontest\\name\\content\\' + f"{path}", 'a', encoding='utf-8') as file:
                            file.write(content + '\n')
                            print("Đã ghi " + f"{content}")
                else:
                    print("Không tìm thấy phần tử có thuộc tính data-price-final")
        else:
            print(f"Yêu cầu không thành công, mã trạng thái: {
                  response.status_code}")


selector_value_list = read_file_to_list("pythontest\\name\\selector_value.txt")
selectorValue = []

# for i in range(0, len(selector_value_list), 4):
#     selectorValue.append((selector_value_list[i], selector_value_list[i+1], selector_value_list[i+2], selector_value_list[i+3]))

# for selector, value, data, path in selectorValue:
#     get_content_from_url(link_list, selector, value, data, path)


# original_urls  = read_file_to_list("pythontest\\name\\link_list.txt")
# converted_urls = convert_urls(original_urls)
# for url in converted_urls:
#      with open('pythontest\\name\\converted_link.txt', 'a', encoding='utf-8') as file:
#          file.write(url + '\n')

# original_urls  = read_file_to_list("pythontest\\name\\link_list.txt")
# converted_urls = convert_urls_to_us(original_urls)
# clear_file("pythontest\\name\\converted_link_to_us.txt")
# for url in converted_urls:
#      with open('pythontest\\name\\converted_link_to_us.txt', 'a', encoding='utf-8') as file:
#          file.write(url + '\n')


def get_all_href_web(url, element_name, selector, selector_name):
    response = requests.get(url)
    driver_path = "chromedriver/chromedriver.exe"

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    time.sleep(5)
    html_content = driver.page_source
    driver.quit()

    if response.status_code == 200:
        # Kiểm tra nội dung của phản hồi để đảm bảo đó là HTML
        # Tạo đối tượng BeautifulSoup để phân tích cú pháp HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Tìm tất cả các thẻ 'a' bên trong thẻ 'div' hoặc bất kỳ thẻ cha nào khác
        content = soup.find_all(
            f"{element_name}", {f"{selector}": f"{selector_name}"})
        # content = soup.find('div')
        link = []
        for content in content:
            a_tags = content.find('a', href=True)
            # Lấy tất cả các đường liên kết từ các thẻ 'a'
            href = a_tags.get('href')
            full_url = urllib.parse.urljoin(url, href)
            link.append(full_url)

        # Ghi các đường liên kết vào một tệp txt
        with open('pythontest\\tranform_github_link.txt', 'a') as file:
            for link in link:
                file.write(link + '\n')
        print('Đã lưu các đường liên kết vào tệp links.txt')
    else:
        print(f'Yêu cầu HTTP thất bại với mã trạng thái: {
              response.status_code}')


# element_name = "div"
# selector = "class"
# selector_name = "search-title"
# clear_file('pythontest\\tranform_github_link.txt')

# for pages in range(11,21):
#     url = "https://github.com/search?q=sign+in+language%3ACSS&type=repositories&l=CSS&p=" + f"{pages}"
#     get_all_href_web(url,element_name, selector, selector_name)

# url = "https://stackoverflow.com/questions/8933863/how-to-find-tags-with-only-certain-attributes-beautifulsoup"
# get_all_href_web(url,element_name, selector, selector_name)


# original_urls  = read_file_to_list("pythontest\\tranform_github_link.txt")
# converted_urls = convert_github_url(original_urls)

# clear_file("pythontest\\output\\output_github_link.txt")
# for url in converted_urls:
#      with open('pythontest\\output\\output_github_link.txt', 'a', encoding='utf-8') as file:
#          file.write(url + '\n')

# url_convered_github = read_file_to_list('pythontest\\tranform_github_link.txt')
# for url in url_convered_github[81:100]:
#     webbrowser.open_new_tab(url)
#     # print(url)


# def change_dns_windows(interface, new_dns):
#     # Set primary DNS server
#     os.system(f"netsh interface ip set dns name=\"{interface}\" source=static addr={new_dns[0]}")

#     # Add secondary DNS server
#     for dns in new_dns[1:]:
#         os.system(f"netsh interface ip add dns name=\"{interface}\" addr={dns} index=2")

#     print(f"DNS settings have been changed to: {', '.join(new_dns)} for interface {interface}")

# Example usage
# interface_name = "Ethernet"
# google_server = ["8.8.8.8", "8.8.4.4"]
# cloudflare_server = ["1.1.1.1", "1.0.0.1"]
# change_dns_windows(interface_name, cloudflare_server)


# def change_dns_ipv6(interface, new_dns):
#     # Set primary DNS server
#     os.system(f"netsh interface ipv6 set dns name=\"{interface}\" source=static addr={new_dns[0]} primary")

#     # Add secondary DNS server
#     for dns in new_dns[1:]:
#         os.system(f"netsh interface ipv6 add dns name=\"{interface}\" addr={dns} index=2")

#     print(f"DNS settings have been changed to: {', '.join(new_dns)} for interface {interface}")

# # # Example usage
# interface_name = "Ethernet"
# google_server = ["2001:4860:4860::8888", "2001:4860:4860::8844"]
# cloudflare_server = ["2606:4700:4700::1111", "2606:4700:4700::1001"]
# change_dns_ipv6(interface_name, google_server)

# def testt(interface, new_dns):
#     ha = f"netsh interface ipv6 set dns name=\"{interface}\" source=static addr={new_dns[0]} primary"
#     for dns in new_dns[1:]:
#         ha += f"\nnetsh interface ipv6 add dnsservers \"{interface}\" {dns} index=2"
#     return ha
# print(testt(interface_name, google_server))


def get_file_names(directory):
    file_names = []
    # Lặp qua tất cả các tập tin trong thư mục được chỉ định
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = file_path.replace('/', '\\')
            file_names.append(file_path)
    return file_names


def write_to_file(file_names, output_file):
    with open(output_file, 'w') as f:
        for file_name in file_names:
            f.write(file_name + '\n')

# directory = 'img/article/section-new-releases/comming-soon'
# output_file = 'pythontest/output_file_name.txt'

# file_names = get_file_names(directory)
# write_to_file(file_names, output_file)

# directory = 'img/article/section-trending'
# output_file = 'pythontest/name/content/content_img.txt'


# write_to_file(get_file_names(directory), output_file)


def edit_html_file(html_path, txt_path, element_name, selector, selector_name):
    # Đọc nội dung file HTML
    with open(f"{html_path}", 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Đọc nội dung file TXT
    text_content = read_file_to_list(txt_path)
    # Tạo đối tượng BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm tất cả các thẻ img

    # Sửa thuộc tính src của các thẻ img
    if (f"{element_name}" == 'img'):
        content = soup.find_all(
            f"{element_name}", {f"{selector}": f"{selector_name}"})
        index = 0
        while index < 24:
            src = content[index].get('src')
            if src and 'img/article/section-trending/' in src:
                content[index]['src'] = src + text_content[index]
                index = index + 1
    elif (f"{element_name}" == 'span'):
        content = soup.find_all(
            f"{element_name}", {f"{selector}": f"{selector_name}"})
        index = 0
        while index < 24:
            content[index].string = text_content[index]
            index = index + 1
    else:
        content = soup.find_all(
            f"{element_name}", {f"{selector}": f"{selector_name}"})
        index = 0
        while index < 24:
            span = content[index].find('span')
            if span:
                span.string = text_content[index]
                index = index + 1

    # Ghi lại nội dung đã chỉnh sửa vào file HTML
    # with open(f"{html_path}", 'w', encoding='utf-8') as file:
    #     file.write(str(soup))

    # print("Đã hoàn thành việc chỉnh sửa và lưu vào" + f"{html_path}")


# file_html_path = "test_trending.html"
# directory = 'pythontest/name/content'
# file_txt_list = get_file_names(directory)
# print(file_txt_list)

# selector_value_list = read_file_to_list("pythontest\\name\\edit_html.txt")
# selectorValue = []

# for i in range(0, len(selector_value_list), 3):
#     selectorValue.append((selector_value_list[i], selector_value_list[i+1], selector_value_list[i+2]))

# indexx = 0
# while indexx < 5:
#     element_name = selectorValue[indexx][0]
#     selector = selectorValue[indexx][1]
#     selector_name = selectorValue[indexx][2]
#     txt_path = file_txt_list[indexx]
#     edit_html_file(file_html_path, txt_path, element_name, selector, selector_name)
#     indexx = indexx + 1


def check_and_add_class(html_path, element_name, selector, selector_name):
    # Đọc nội dung file HTML
    with open(f"{html_path}", 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Tạo đối tượng BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup.find_all(f"{element_name}", {f"{selector}": f"{selector_name}"}):
        # Kiểm tra nếu phần tử không có nội dung (bao gồm cả các khoảng trắng)
        if not element.text.strip():
            # Thêm class "ngl-hide"
            if 'class' in element.attrs:
                element['class'].append('ngl-hide')
            else:
                element['class'] = ['ngl-hide']
    with open(f"{html_path}", 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print("Đã hoàn thành việc chỉnh sửa" +
          f"{selector_name}" + "và lưu vào" + f"{html_path}")


# file_html_path = "test_trending.html"
# element_name = "span"
# selector = "class"
# selector_name = ["__discount", "__base-price"]

# for selector_name in selector_name:
#     check_and_add_class(file_html_path, element_name, selector, selector_name)
    # print(selector_name)


# Hàm để dịch nội dung của các thẻ

def translate_html_content(html_content, src_lang='en', dest_lang='vi'):
    # Khởi tạo BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Khởi tạo Translator
    translator = Translator()

    # Duyệt qua tất cả các thẻ và dịch nội dung
    for element in soup.find_all(text=True):
        if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            # Dịch nội dung văn bản
            # element = element.strip()
            print(element.strip())
            # translated_text = translator.translate(
            #     element, src=src_lang, dest=dest_lang).text

            # element.replace_with(translated_text)

    return str(soup)


# # Đọc nội dung HTML từ file
# input_file_path = 'pythontest/save.html'
# with open(input_file_path, 'r', encoding='utf-8') as file:
#     html_content = file.read()

# # Dịch nội dung HTML
# translated_html_content = translate_html_content(html_content)

# # Ghi nội dung đã dịch vào file mới
# output_file_path = 'pythontest/output/translate.html'
# clear_file(output_file_path)
# with open(output_file_path, 'w', encoding='utf-8') as file:
#     file.write(translated_html_content)

# print(f'File đã được dịch và lưu tại: {output_file_path}')
