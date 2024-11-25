#include<bits/stdc++.h>
using namespace std;

bool isChar(char ch) {
    return ch >= 'A' && ch <= 'Z' || ch >= 'a' && ch <= 'z';
}

bool isDigit(char ch) {
    return ch >= '0' && ch <= '9';
}

bool isEmpty(string str) {
    return str.length() == 0;
}

bool isOperator(char ch) {
    switch (ch) {
    case '+':
    case '-':
    case '*':
    case '/':
    case '%':
        return true;
    }
    return false;
}

int main() {
    stack<char> st;
    stack<char> paren;
    string eq;
    cin >> eq;

    if (isEmpty(eq)) {
        cout << "Mathematical equation was not given\n";
        return 0;
    }
    char firstChar = eq[0];
    if (!isChar(firstChar) && !isDigit(firstChar)) {
        cout << "1 Invalid equation!\n";
        return 0;
    }

    char lastChar = eq[eq.length() - 1];
    if (!isChar(lastChar) && !isDigit(lastChar) && lastChar != ')') {
        cout << "2 Invalid equation!\n";
        return 0;
    }

    for (char ch : eq) {
        if (isChar(ch) || isDigit(ch)) {
            if (!st.empty()) {
                st.pop();
            }
        } else if (isOperator(ch)) {
            if (st.empty()) {
                st.push(ch);
            } else {
                cout << "3 Invalid equation\n";
                return 0;
            }
        } else if (ch == '(') {
            paren.push(ch);
        } else if (ch == ')') {
            if (paren.top() == '(') {
                paren.pop();
            } else {
                cout << "4 Invalid parentheses\n";
                return 0;
            }
        } else {
            cout << "5 Invalid equation!\n";
            return 0;
        }
    }

    if (st.empty() && paren.empty()) {
        cout << "Valid equation: " << eq << endl;
    } else {
        cout << "6 Invalid equation\n";
    }
    return 0;
}
