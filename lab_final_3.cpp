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
    vector<char> op;
    vector<char> alpha;
    vector<char> num;
    vector<char> other;

    string inp;
    cin >> inp;

    for (char ch : inp) {
        if (isChar(ch)) alpha.push_back(ch);
        else if (isDigit(ch)) num.push_back(ch);
        else if (isOperator(ch)) op.push_back(ch);
        else other.push_back(ch);
    }

    // Operators
    cout << "Operators: ";
    for (char ch : op) {
        cout << ch << " ";
    }
    cout << endl;

    // Alphabets
    cout << "Alphabets: ";
    for (char ch : alpha) {
        cout << ch << " ";
    }
    cout << endl;

    // Numeric
    cout << "Numeric: ";
    for (char ch : num) {
        cout << ch << " ";
    }
    cout << endl;

    // Other
    cout << "Others: ";
    for (char ch : other) {
        cout << ch << " ";
    }
    cout << endl;

    return 0;
}
