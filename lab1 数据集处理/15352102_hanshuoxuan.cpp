#include <iostream>
#include <fstream>
#include <cstdio>
#include <iomanip>
#include <string.h>
#include <stdio.h>
#include <cstring>
#include <cmath>

using namespace std;

struct triad {
	int nums, cols, rows;
	int t[15000][3];
};

int num, txt, cnt;                               //分别是不同的单词总数，句子数和三元组的值的个数
int ori[1500][15000];                            //原始的单词统计矩阵。其中第0行表示每个单词在多少个文本中出现过（算idf用），第0列表示每句话有多少个单词（算tf用）
double TF[1500][15000], TFIDF[1500][15000];      //TF矩阵和TFIDF矩阵
string words[15000];                             //按照出现顺序记录每一个单词
triad sm, t1, t2, tsum;                          //分别是onehot矩阵的三元组，两个输入的三元组和结果三元组


int search(char *p)                              //在出现过的单词中搜索，如果是旧单词就返回位置，否则返回-1表示是新单词
{
	for (int i = 1; i <= num; i++)
	{
		if (words[i] == p) return i;
	}
	return -1;
}

void AplusB()
{
	for (int i = 0; i<t1.nums; i++)              //如果t1中的一个元素在t2中出现过，就直接加上去
	{
		bool found = false;
		for (int j = 0; j<t2.nums; j++)
			if (t1.t[i][0] == t2.t[j][0] && t1.t[i][1] == t2.t[j][1])
			{
				t2.t[j][2] += t1.t[i][2];
				found = true;
				break;
			}
		if (!found)                              //否则，在t2新开一个单元用来存t1的这个元素
		{
			t2.t[t2.nums][0] = t1.t[i][0];
			t2.t[t2.nums][1] = t1.t[i][1];
			t2.t[t2.nums][2] = t1.t[i][2];
			t2.nums++;
		}
	}
	for (int i = 0; i<t2.nums - 1; i++)          //排序t2，因为它存的就是结果，使得按照行优先列次之的顺序输出
		for (int j = i + 1; j<t2.nums; j++)
			if (t2.t[i][0] > t2.t[j][0] || (t2.t[i][0] == t2.t[j][0] && t2.t[i][1]>t2.t[j][1]))
			{
				int tem;
				tem = t2.t[i][0]; t2.t[i][0] = t2.t[j][0]; t2.t[j][0] = tem;
				tem = t2.t[i][1]; t2.t[i][1] = t2.t[j][1]; t2.t[j][1] = tem;
				tem = t2.t[i][2]; t2.t[i][2] = t2.t[j][2]; t2.t[j][2] = tem;
			}
} 

int main()
{
	ifstream fin("text.txt");
	ifstream t1in("A.txt");
	ifstream t2in("B.txt");
	ofstream onehot("onehot.txt");
	ofstream tf("TF.txt");
	ofstream tfidf("TFIDF.txt");
	ofstream smatrix("smatrix.txt");
	ofstream tsum("sum.txt");

	if (!fin)    
	{
		cout << "404!\n";
		return 0;
	}
	char s[500];
	num = txt = cnt = 0;
	memset(ori, 0, sizeof(ori));
	while (!fin.eof())                           //52行和54行是一行一行，即一句一句，读入文件的方法
	{
		fin.getline(s, 500);
		txt++;
		const char *d = "	 ";
		char *p;
		p = strtok(s, d);
		while (p)                                //这个while循环用来分词
		{
			string ss = p;
			if (isdigit(p[0]) || ss.find(":", 0) < string::npos)
			{
				p = strtok(NULL, d);
				continue;
			}                                    //去除数字和表示情感的词
			int pos = search(p);                 //判断是新词还是旧词并做不同处理
			ori[txt][0]++;
			if (pos > 0)
			{
				ori[txt][pos]++;
				if (ori[txt][pos] == 1) ori[0][pos]++;
			}
			else
			{
				num++;
				ori[txt][num]++;
				ori[0][num]++;
				words[num] = p;
			}
			p = strtok(NULL, d);                 //分出下一个单词，81行和58行一起分词
		}
	}
	txt--;                                       //每次都会多统计一个文本，所以做完之后要减一

	for (int i = 1; i <= txt; i++)
	{
		for (int j = 1; j < num; j++)
			if (ori[i][j] > 0)                   //输出onehot矩阵，如果ori里面大于1则表示出现过，输出1，否则输出0
				onehot << 1 << " ";
			else
				onehot << 0 << " ";
		if (ori[i][num] > 0)
			onehot << 1 << endl;
		else
			onehot << 0 << endl;
	}

	for (int i = 1; i <= txt; i++)               //这个双重循环输出TF矩阵，由于这个矩阵在后面还有用所以要存
	{
		for (int j = 1; j < num; j++)
		{
			TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
			tf << fixed << setprecision(4) << TF[i][j] << " ";
		}
		TF[i][num] = ori[i][num] * 1.0 / ori[i][0];
		tf << fixed << setprecision(4) << TF[i][num] << endl;
	}

	for (int i = 1; i <= txt; i++)               //这个双重循环输出TFIDF矩阵
	{
		for (int j = 1; j < num; j++)
		{
			TFIDF[i][j] = TF[i][j] * log(txt * 1.0 / (ori[0][j] + 1)) / log(2);
			tfidf << fixed << setprecision(4) << TFIDF[i][j] << " ";
		}
		TFIDF[i][num] = TF[i][num] * log(txt * 1.0 / (ori[0][num] + 1)) / log(2);
		tfidf << fixed << setprecision(4) << TFIDF[i][num] << endl;
	}

	for (int i = 1; i <= txt; i++)               //由ori数组得出smatrix
	{
		for (int j = 1; j <= num; j++)
		{
			if (ori[i][j] > 0)
			{
				sm.t[cnt][0] = i - 1;            //i和j都减一是因为从1开始统计，第0行和列用处见18行的注释
				sm.t[cnt][1] = j - 1;
				sm.t[cnt][2] = 1;
				cnt++;
			}
		}
	}
	smatrix << "[" << txt << "]" << endl << "[" << num << "]" << endl << "[" << cnt << "]" << endl;
	for (int i = 0; i < cnt; i++)
		smatrix << "[" << sm.t[i][0] << ", " << sm.t[i][1] << ", " << sm.t[i][2] << "]" << endl;

	t1in >> t1.rows >> t1.cols >> t1.nums;       //下面就是做三元组矩阵加法
	t2in >> t2.rows >> t2.cols >> t2.nums;
	if (t1.rows != t2.rows || t1.cols != t2.cols)
	{
		tsum << "The sizes of the two matrix are not the same.\n";
		return 0;
	}
	for (int i = 0; i<t1.nums; i++)
		t1in >> t1.t[i][0] >> t1.t[i][1] >> t1.t[i][2];
	for (int i = 0; i<t2.nums; i++)
		t2in >> t2.t[i][0] >> t2.t[i][1] >> t2.t[i][2];
	AplusB();
	tsum << t2.rows << endl << t2.cols << endl << t2.nums << endl;
	for (int i = 0; i<t2.nums; i++)
		tsum << t2.t[i][0] << " " << t2.t[i][1] << " " << t2.t[i][2] << endl;
	return 0;
}
