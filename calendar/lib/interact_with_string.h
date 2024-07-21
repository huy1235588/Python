#include <string>
#include <sstream>

// hàm để loại bỏ các khoảng trắng ở đầu và cuối của một chuỗi
std::string strip(const std::string &str)
{
    // Tìm vị trí ký tự không phải khoảng trắng đầu tiên
    size_t start = str.find_first_not_of(" \t\n\r\f\v");
    size_t end = str.find_last_not_of(" \t\n\r\f\v");

    if (start == std::string::npos || end == std::string::npos)
    {
        // Nếu không tìm thấy ký tự không phải khoảng trắng, trả về chuỗi rỗng
        return "";
    }

    // Tìm vị trí ký tự không phải khoảng trắng cuối cùng

    // Trả về chuỗi con từ start đến end
    return str.substr(start, end - start + 1);
}

// Hàm để tách chuỗi
std::string split(const std::string &str, const char delimiter, int position)
{
    std::stringstream ss(str);
    std::string item;

    int count = 0;

    while (std::getline(ss, item, delimiter))
    {
        if (count == position)
        {
            item = strip(item);
            return item;
        }
        count++;
    }

    return str;
}