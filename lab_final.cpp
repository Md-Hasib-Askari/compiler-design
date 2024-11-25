#include<bits/stdc++.h>
using namespace std;

bool isChar(char ch) {
    return ch >= 'A' && ch <= 'Z' || ch >= 'a' && ch <= 'z';
}

bool isDigit(char ch) {
    return ch >= '0' && ch <= '9';
}

int main() {
    string varName;
    cin >> varName;

    // checking if empty
    if (varName.length() == 0) {
        cout << "Invalid variable name\n";
        return 0;
    }

    // checking first character
    if (!isChar(varName[0]) && varName[0] != '_') {
        cout << "Variable must start with an alphabet or underscore\n";
        return 0;
    }

    bool flag = true;
    for (char ch : varName) {
        if (!isChar(ch) && !isDigit(ch) && ch != '_') {
            flag = false;
            cout << "Invalid variable name\n";
            return 0;
        }
    }

    if (flag) {
        cout << "Valid variable name: " << varName << endl;
    }
}
