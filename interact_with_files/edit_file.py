# Đọc dữ liệu từ file input.txt
with open('input/dapan.txt', 'r') as file:
    data = file.readlines()

# Xử lý dữ liệu để chuyển đổi định dạng
formatted_data = []
for line in data:
    key, value = line.strip().split()
    formatted_data.append(f'{key}: "{value}"')

# Ghi dữ liệu đã chuyển đổi vào file output.txt
with open('output/dapan.txt', 'w') as file:
    file.write(', '.join(formatted_data))

print("Đã chuyển đổi dữ liệu và ghi vào file output.txt")
