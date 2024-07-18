def create_file(path, num):
    for number in range(1, num):
        with open(f"{path}" + "ha" + f"{number}" + ".zip", "w") as file:
            file.write(f"{number}\n")


file_path = "C:/ProgramData/Apache24/htdocs/downloads/"
create_file(file_path, 100)
