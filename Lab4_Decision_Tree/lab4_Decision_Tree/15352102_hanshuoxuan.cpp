#include<bits/stdc++.h>
using namespace std;
int a[1000][10], b[1000], txt;
int main()
{
	ifstream fin("train.csv");
	txt=0;
	while (!fin.eof())
	{
		txt++;
		for (int i=0;i<9;i++)
		{
			fin>>a[txt][i];
			cout<<a[txt][i]<<" ";
		}
		fin>>b[txt];
		cout<<b[txt]<<endl;
	}
	return 0;
}
