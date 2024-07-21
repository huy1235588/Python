#include "lib/read_and_write_file_json.h"
#include <string>

int main()
{
    const char *file_json = "json/ha.json";
    write_file_json(file_json, "varrient", "false");

    // std::cout << ha << std::endl;
    // system("pause");
    return 0;
}