


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


def convert_urls(url):
    codes = read_file_to_list("txt/codes.txt")
    new_urls = []
    for code in codes:
        new_url = url + code
        new_urls.append(new_url)
    return new_urls


url = "" #Link URl here

list_link = convert_urls(url)

with open ("txt/new_link.txt", "w") as file:
    for link in list_link:
        file.write(link + "\n")