#include<bits/stdc++.h>
using namespace std;
int main()
{
	ifstream f("train_set2.csv");
	char s[500];
	f.getline(s,500);
	while (!f.eof())
	{
		f>>s;
		cout<<s<<endl;
	}
	return 0;
}
