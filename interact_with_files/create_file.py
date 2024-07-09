def create_file (path, num):
    with open(f"{path}", "w") as file:
        for number in range(1, num):
            file.write(f"{number}\n")

file_path = "input/create_file_path.txt"
create_file(file_path, 101)