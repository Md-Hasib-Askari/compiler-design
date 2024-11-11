#include <bits/stdc++.h>
using namespace std;

bool isAlpha(char ch) {
    return ch >= 65 && ch <= 90 || ch >= 97 && ch <= 122;
}

bool isDigit(char ch) {
    return ch >= 48 && ch <= 57;
}

int main() {
    string var;
    cin >> var;

    // check first character
    if (!isAlpha(var[0]) && var[0] != 95) cout << "Variable name must start with alphabet or underscore!\n";

    bool flag = 1;
    for (char ch : var) {
            flag = !isAlpha(ch) && !isDigit(ch) && ch != 95;
    }

    if (!flag) cout << "Only alphanumeric characters or underscore can be used!\n";
    else cout << "variable name: " << var << endl;
}
