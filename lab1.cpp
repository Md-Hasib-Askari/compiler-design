#include <bits/stdc++.h>

using namespace std;

int main() {
    string keywords[] = {"if", "for", "while", "do", "continue", "else", "switch"};
    string str;
    getline(cin, str);

    for (string kw : keywords) {
        auto pos = str.find(kw);
        if (pos != string::npos) cout << kw << " is a keyword" << endl;
    }
}
