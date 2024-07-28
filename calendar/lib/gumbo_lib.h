#include <string>      // xử lý chuỗi
#include <curl/curl.h> // thực hiện các yêu cầu HTTP
#include <gumbo.h>     // phân tích cú pháp HTML
#include <iostream>    // đầu ra và đầu vào cơ bản
#include <ctime>       // làm việc với time
#include <fstream>     // đọc/ghi tệp
#include <iomanip>     // định dạng đầu ra

// #include "interact_with_string.h"
#include "read_and_write_file_json.h"

// Function to write the response data to a string
size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *s)
{
    size_t newLength = size * nmemb;
    try
    {
        s->append((char *)contents, newLength);
    }
    catch (std::bad_alloc &e)
    {
        // Handle memory problem
        return 0;
    }
    return newLength;
}

// Function to get the HTML content of a webpage
std::string fetchHTML(const std::string &url)
{
    CURL *curl;
    CURLcode res;
    std::string htmlContent;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if (curl)
    {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &htmlContent);
        res = curl_easy_perform(curl);
        if (res != CURLE_OK)
        {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return htmlContent;
}

bool has_class(const GumboAttribute *class_attr, const char *class_name)
{
    if (!class_attr)
    {
        return false;
    }
    // Tách các class và kiểm tra từng class một
    const char *class_values = class_attr->value;
    const char *class_pos = strstr(class_values, class_name);
    while (class_pos)
    {
        // Kiểm tra các điều kiện để chắc chắn đây là một class name độc lập
        bool start_ok = (class_pos == class_values) || isspace(class_pos[-1]);
        bool end_ok = (class_pos[strlen(class_name)] == '\0') || isspace(class_pos[strlen(class_name)]);
        if (start_ok && end_ok)
        {
            return true;
        }
        // Tìm tiếp
        class_pos = strstr(class_pos + 1, class_name);
    }
    return false;
}

// Hàm đệ quy để tìm node có attributes
void search_for_attributes(const GumboNode *node, const char *attributes_name, const char *attributes_value, std::string &result)
{
    if (node->type != GUMBO_NODE_ELEMENT)
    {
        return;
    }

    GumboAttribute *class_attr = gumbo_get_attribute(&node->v.element.attributes, attributes_name);
    if (has_class(class_attr, attributes_value))
    {
        // Lấy nội dung text của node
        if (node->v.element.children.length > 0)
        {
            const GumboNode *text_node = static_cast<GumboNode *>(node->v.element.children.data[0]);
            if (text_node->type == GUMBO_NODE_TEXT)
            {
                result = text_node->v.text.text;
            }
        }
        return;
    }

    // Duyệt qua các con của node hiện tại
    const GumboVector *children = &node->v.element.children;
    for (unsigned int i = 0; i < children->length; ++i)
    {
        search_for_attributes(static_cast<GumboNode *>(children->data[i]), attributes_name, attributes_value, result);
    }
}

// Hàm đệ quy để tìm node có attribute thứ nth
void search_for_nth_attributes(const GumboNode *node, const char *attributes_name, const char *attributes_value, int &count, int nth, std::string &result)
{
    if (node->type != GUMBO_NODE_ELEMENT)
    {
        return;
    }

    GumboAttribute *class_attr = gumbo_get_attribute(&node->v.element.attributes, attributes_name);
    if (has_class(class_attr, attributes_value))
    {
        ++count;
        if (count == nth)
        {
            // Lấy nội dung text của node
            for (unsigned int i = 0; i < node->v.element.children.length; ++i)
            {
                const GumboNode *child = static_cast<GumboNode *>(node->v.element.children.data[i]);
                if (child->type == GUMBO_NODE_TEXT)
                {
                    result += child->v.text.text;
                }
                else if (child->type == GUMBO_NODE_ELEMENT)
                {
                    search_for_nth_attributes(child, attributes_name, attributes_value, count, nth, result);
                }
            }
            return;
        }
    }

    // Duyệt qua các con của node hiện tại
    const GumboVector *children = &node->v.element.children;
    for (unsigned int i = 0; i < children->length; ++i)
    {
        search_for_nth_attributes(static_cast<GumboNode *>(children->data[i]), attributes_name, attributes_value, count, nth, result);
    }
}

// Hàm chỉnh sửa file html
void replace_content_HTML(const std::string &filePath, const std::string &element, const std::string &attributes_name, const std::string &attributes_value, const std::string &newContent)
{
    std::ifstream fileIn(filePath);
    if (!fileIn)
    {
        std::cerr << "Error opening file for reading.\n";
        return;
    }

    std::string fileContent((std::istreambuf_iterator<char>(fileIn)), std::istreambuf_iterator<char>());
    fileIn.close();

    // Tìm và thay thế nội dung giữa <div id="content"> và </div>
    std::string oldContentStart = "<" + element + " " + attributes_name + "=\"" + attributes_value + "\">";
    std::string oldContentEnd = "</" + element + ">";
    size_t startPos = fileContent.find(oldContentStart);
    if (startPos == std::string::npos)
    {
        std::cerr << "Content ID not found.\n";
        return;
    }
    startPos += oldContentStart.length();
    size_t endPos = fileContent.find(oldContentEnd, startPos);
    if (endPos == std::string::npos)
    {
        std::cerr << "Content ID end not found.\n";
        return;
    }

    // Thay thế nội dung cũ bằng nội dung mới
    fileContent.replace(startPos, endPos - startPos, newContent);

    std::ofstream fileOut(filePath);
    if (!fileOut)
    {
        std::cerr << "Error opening file for writing.\n";
        return;
    }
    fileOut << fileContent;
    fileOut.close();
}

// Function to parse the current date and time from the Vietnam Online webpage
std::string parseVietnamDateTime(const std::string &html)
{
    GumboOutput *output = gumbo_parse(html.c_str());

    std::string dateTime;
    int count_nth = 0;

    search_for_nth_attributes(output->root, "class", "tb-cell", count_nth, 6, dateTime);

    gumbo_destroy_output(&kGumboDefaultOptions, output);
    return dateTime;
}

// Function to convert date string to tm struct
time_t convertToTimeT(const std::string &dateStr, const std::string &format)
{
    std::tm tm = {};
    std::istringstream ss(dateStr);
    ss >> std::get_time(&tm, format.c_str());
    std::time_t time = mktime(&tm);
    return time;
}

// Function to compare two dates
double compareDates(const time_t &time1, const time_t &time2)
{
    double difference = std::difftime(time2, time1) / (60 * 60 * 24);
    return difference;
}

// Function to check if the current phase is phase 2
void checkPhase(const std::string &url)
{
    std::string htmlContent = fetchHTML(url);
    GumboOutput *output = gumbo_parse(htmlContent.c_str());

    // Lấy phare hiện tại
    std::string current_phare_str;
    search_for_attributes(output->root, "id", "hl_1", current_phare_str);

    // Lấy date tại phare 2
    std::string phase2DateStr;
    int count = 0;
    search_for_nth_attributes(output->root, "width", "60%", count, 1, phase2DateStr);

    // Giải phóng
    gumbo_destroy_output(&kGumboDefaultOptions, output);

    // Lấy ký tự cuối cùng
    char current_phare = current_phare_str.back();

    // Check if current phare is 2
    if (current_phare == '1')
    {
        // Lấy thời gian hiện tại
        std::string currentDateTimeStr = parseVietnamDateTime(fetchHTML("https://www.vietnamonline.com/current-time.html"));

        // Chuyển chỗi thành tm
        std::time_t phase2Date = convertToTimeT(phase2DateStr, "%B %d, 20%y");
        std::time_t currentDateTime = convertToTimeT(currentDateTimeStr, "%A %d %B %Y");

        // So sánh 2 ngày
        double elapse_date = compareDates(phase2Date, currentDateTime);

        if (elapse_date >= 40)
        {
            // File json path
            const char *file_json = "json/ha.json";

            // Lấy varrient từ file json
            std::string varrient = read_file_json(file_json, "varrient");

            if (varrient == "true")
            {
                // Lấy timeStamp từ file json
                std::string timeStamp = read_file_json(file_json, "timestamp");

                // Chuyển timeStamp sang time_T
                std::time_t timeStampDate = convertToTimeT(timeStamp, "%m/%d/20%y");

                // So sánh TimeStampDate và currentDateTime
                elapse_date = compareDates(timeStampDate, currentDateTime);

                if (elapse_date == 2 && elapse_date == 4)
                {
                    std::cout << elapse_date << "\t" << varrient << std::endl;
                }
            }

            else
            {
                const char *filePathHTML = "d:/Project/Python/calendar/web/public/index.html";

                // Chuyển elapse_date từ double sang string
                std::string elapse_date_str = std::to_string(elapse_date);
                elapse_date_str = elapse_date_str.substr(0, elapse_date_str.find('.')); // Lấy phần trước dấu chấm

                phase2DateStr = split(phase2DateStr, '-', 0);

                // Chỉnh sửa file html
                replace_content_HTML(filePathHTML, "span", "id", "passed_day", elapse_date_str);
                replace_content_HTML(filePathHTML, "span", "id", "relative", phase2DateStr);

                // Mở file html
                // system("start http://192.168.1.13:3000");
                // system("e: && cd web && node server.js");
            }
        }
    }
}