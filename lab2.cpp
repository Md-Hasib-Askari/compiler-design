#include <bits/stdc++.h>
using namespace std;

int main() {
    stack<char> paren;
    bool valid = true;

    string inp;
    cout << "Enter any operation:" << endl;
    getline(cin, inp);

    for (char ch : inp) {
        if (ch == '(' || ch == '{' || ch == '[') {
            paren.push(ch);
        } else if (ch == ')' || ch == '}' || ch == ']') {
            if (paren.empty()) {
                valid = false;
                break;
            }
            char top = paren.top();
            if ((ch == ')' && top == '(') ||
                (ch == '}' && top == '{') ||
                (ch == ']' && top == '[')) {
                paren.pop();
            } else {
                valid = false;
                break;
            }
        }
    }

    if (!paren.empty()) valid = false;

    if (valid)
        cout << "Your expression is valid: " << inp << endl;
    else
        cout << "Invalid expression: " << inp << endl;

    return 0;
}
