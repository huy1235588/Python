#include <fstream>
#include <iostream>
#include <string>
#include "interact_with_string.h"

std::string read_file_json(const char *path_file, const std::string &key)
{
    std::ifstream file(path_file);

    if (!file.is_open())
    {
        std::cerr << "Không thể mở file JSON!" << std::endl;
        return "";
    }

    std::string line;
    int lineNumber = 0;

    while (getline(file, line))
    {
        std::string keyWithColon = "\"" + key + "\":";
        size_t keyPos = line.find(keyWithColon);

        if (keyPos != std::string::npos)
        {
            size_t valueStart = keyPos + keyWithColon.length();
            size_t valueEnd = line.find_first_of(",}", valueStart);
            line = line.substr(valueStart, valueEnd - valueStart);
            if (line.find('\"') != std::string::npos)
            {
                std::string result;
                for (char c : line)
                {
                    if (c != '"')
                    {
                        result += c;
                    }
                }
                line = result;
            }
            file.close();
            return strip(line);
        }
        ++lineNumber;
    }

    file.close();
    return "";
}

void write_file_json(const char *path_file, const std::string &key, const std::string &value)
{
    // Đọc file
    std::ifstream file(path_file);
    if (!file.is_open())
    {
        std::cerr << "Error: Không thể mở file để đọc!" << std::endl;
        return;
    }

    std::string string_result;

    std::string line;
    int lineNumber = 0;

    // Lấy dữ liệu từng dòng
    while (getline(file, line))
    {
        std::string keyTemp = '"' + key + '"';
        size_t keyPos = line.find(keyTemp);

        // Thay dổi value
        if (keyPos != std::string::npos)
        {
            keyPos += keyTemp.length(); // Di chuyển đến vị trí sau key

            size_t valueStart = line.find('"', keyPos) + 1;
            size_t valueEnd = line.find('"', valueStart);

            std::string valueTest = line.substr(valueStart, valueEnd - valueStart);

            if (valueStart != std::string::npos && valueEnd != std::string::npos)
            {
                line.replace(valueStart, valueEnd - valueStart, value);
            }
        }
        string_result += line + "\n";
        ++lineNumber;
    }

    std::ofstream fileOut(path_file);
    if (!fileOut.is_open())
    {
        std::cout << "Error: Không thể mở file để ghi!" << std::endl;
        return;
    }
    fileOut << string_result << std::endl;
    // std::cout << string_result << std::endl;
    file.close();
}