#include <iostream>
#include <map>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}

std::string compress(std::string text) {
    char firstChar = text[0];
    int count = 1;
    std::string result = "";
    if(text.size()==1){
        result=firstChar+std::to_string(1);
        return result;
    }
    for (int i = 1; i < text.size(); ++i) {
        if(text[i]==' '&&i+1==text.size()){
            result+=text[i];
        }

        if (text[i] == firstChar && text[i] != ' ') {
            count++;
            if (i == text.size() - 1) {
                result += firstChar + std::to_string(count);
                std::cout << result << std::endl;
            }
        }
        if (text[i] != firstChar) {

            if (firstChar != ' ') {
                result += firstChar + std::to_string(count);
                std::cout << result << std::endl;
                firstChar = text[i];
            } else {
                result += ' ';
            }

            firstChar = text[i];
            count = 1;
            if (i + 1 == text.size()) {
                std::cout << "Son karakter" << std::endl;
                if (text[i] == ' ') {

                    result += ' ';
                } else {
                    result += firstChar + std::to_string(count);
                    std::cout << result << std::endl;
                }
            }
        }
    }
    return result;
}

