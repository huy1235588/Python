def create_file(path, num):
    for number in range(1, num):
        with open(f"{path}" + "ha" + f"{number}" + ".txt", "w") as file:
            file.write(f"{number}\n")


file_path = "e:\Project\Python\interact_with_files\output/"
create_file(file_path, 100)
