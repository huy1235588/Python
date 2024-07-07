
import fitz  

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

answers_path = "input/dapan.txt"
answers = read_file_to_list(answers_path)

pdf_document = "input/practice test 3.pdf"
doc = fitz.open(pdf_document)

print(answers)

def highlight_text(page, text, color=(1, 1, 0)):
    text_instances = page.search_for(text)
    for inst in text_instances:
        highlight = page.add_highlight_annot(inst)
        highlight.set_colors(stroke=color)
        highlight.update()


for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    for ans in answers:
        # question = f"{q_num}."
        options = ["A", "B", "C", "D"]
        for option in options:
            if option == ans:
                option_text = f"{option})"
                highlight_text(page, option_text)



doc.save("highlighted_test.pdf")

print("Highlighting complete. The file is saved")