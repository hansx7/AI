#include <iostream>
#include <fstream>
#include <cstdio>
#include <iomanip>
#include <string.h>
#include <stdio.h>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <map>

using namespace std;

struct dist {
	double dis;
	int trnum;
};

struct emotion {
	string es;
	int count;
};

int num, txt1, txt2, txt3;    //分别是不同的单词总数，训练集、验证集和测试集句子数 
int ori[1500][15000];     //原始的单词统计矩阵
						  //其中第0行表示每个单词在多少个文本中出现过（算idf用），第0列表示每句话有多少个单词（算tf用）
int OH[1500][15000];             //onehot矩阵 
double TF[1500][15000], TFIDF[1500][15000];    //TF矩阵和TFIDF矩阵
string words[15000];       //按照出现顺序记录每一个单词
string label[1500];     //记录训练集中每个文本的label和验证集的答案 
int k, cnt;
emotion em[6];
dist d[1500];                                    //记录距离 

int search(char *p)                              //在出现过的单词中搜索，如果是旧单词就返回位置，否则返回-1表示是新单词
{
	for (int i = 1; i <= num; i++)
	{
		if (words[i] == p) return i;
	}
	return -1;
}

bool cmp(dist x, dist y)
{
	return x.dis < y.dis;
}

int main()
{
	ifstream trainin("train_set.csv");
	ifstream validationin("validation_set.csv");
	ifstream testin("test_set.csv");
	ofstream onehot("onehot.txt");
	ofstream res("res.csv");

	if (!trainin)
	{
		cout << "404!\n";
		return 0;
	}
	char s[500];
	num = txt1 = txt2 = txt3 = 0;
	memset(ori, 0, sizeof(ori));
	trainin.getline(s, 500);
	while (!trainin.eof())       //一行一行读入训练集
	{
		trainin.getline(s, 500);
		txt1++;
		const char *d = " ";
		char *p;
		p = strtok(s, d);
		while (p)                                //这个while循环用来分词
		{
			string ss = p;
			int comma = ss.find(",", 0);
			if (comma < string::npos)
			{
				label[txt1] = ss.substr(comma + 1, ss.length() - comma - 1);
				p[comma] = '\0';
			}
			int pos = search(p);         //判断是新词还是旧词并做不同处理
			ori[txt1][0]++;
			if (pos > 0)    //旧单词直接找到位置，统计ori
			{
				ori[txt1][pos]++;
				if (ori[txt1][pos] == 1) ori[0][pos]++;
			}
			else    //新单词则新开一个位置，统计ori并录入words
			{
				num++;
				ori[txt1][num]++;
				ori[0][num]++;
				words[num] = p;
			}
			p = strtok(NULL, d);       //分出下一个单词，81行和58行一起分词
		}

	}
	txt1--;                                      //每次都会多统计一个文本，所以做完之后要减一

	validationin.getline(s, 500);
	while (!validationin.eof())
	{
		validationin.getline(s, 500);
		txt2++;
		const char *d = " ";
		char *p;
		p = strtok(s, d);
		while (p)                       //这个while循环用来分词
		{
			string ss = p;
			int comma = ss.find(",", 0);
			if (comma < string::npos)
			{
				label[txt2] = ss.substr(comma + 1, ss.length() - comma - 1);
				p[comma] = '\0';
			}
			int pos = search(p);      //判断是新词还是旧词并做不同处理
			ori[txt1 + txt2][0]++;
			if (pos > 0)
			{
				ori[txt1 + txt2][pos]++;
				if (ori[txt1 + txt2][pos] == 1) ori[0][pos]++;
			}
			else
			{
				num++;
				ori[txt1 + txt2][num]++;
				ori[0][num]++;
				words[num] = p;
			}
			p = strtok(NULL, d);
		}
	}
	txt2--;
	
	for (int i = 1; i <= txt1 + txt2; i++)               //这个双重循环算出onehot矩阵
		for (int j = 1; j <= num; j++)
			if (ori[i][j] > 0) OH[i][j] = 1;
			else OH[i][j] = 0;
	for (int i = 1; i <= txt1 + txt2; i++)               //这个双重循环算出onehot矩阵
	{for (int j = 1; j <= num; j++)
			res << OH[i][j] <<",";
		res<<endl;
	}	
	for (int i = 1; i <= txt1 + txt2; i++)               //这个双重循环算出TF矩阵
		for (int j = 1; j <= num; j++)
			TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
	for (int i = 1; i <= txt1 + txt2; i++)               //这个双重循环算出TFIDF矩阵
		for (int j = 1; j <= num; j++)
			TFIDF[i][j] = TF[i][j] * log((txt1 + txt2) * 1.0 / (ori[0][j] + 1)) / log(2);
			
	k = 0;
	int maxk = 0, maxc = 0;
	em[0].es = "anger";
	em[1].es = "disgust";
	em[2].es = "fear";
	em[3].es = "joy";
	em[4].es = "sad";
	em[5].es = "surprise";
	while (k <= int(sqrt(txt1)))
	{
		k++;
		cnt = 0;
		for (int i = 1; i <= txt2; i++)
		{
			for (int j = 1; j <= txt1; j++)
				d[j].dis = 0;
			for (int j = 1; j <= txt1; j++) //算出训练集和验证集每一对向量之间的距离
			{
				double t = 0, ma = 0, mb = 0;
				for (int l = 1; l <= num; l++)
				{
					d[j].dis += abs(TFIDF[i + txt1][l] - TFIDF[j][l]);
//					ma += TF[i + txt1][l] * TF[i + txt1][l];
//					mb += TF[j][l] * TF[j][l];
//					t += TF[i + txt1][l] * TF[j][l];
				}
//				ma = sqrt(ma);
//				mb = sqrt(mb);
//				d[j].dis = t / ma / mb;
				//d[j].dis = sqrt(d[j].dis);
				d[j].trnum = j;
			}
			sort(d + 1, d + txt1, cmp); //对所有的距离排序
			for (int j = 0; j < 6; j++)
				em[j].count = 0;
			for (int j = 1; j <= k; j++)  //取出前k近的训练文本
				if (label[d[j].trnum] == "anger") em[0].count++;
				else if (label[d[j].trnum] == "disgust") em[1].count++;
				else if (label[d[j].trnum] == "fear") em[2].count++;
				else if (label[d[j].trnum] == "joy") em[3].count++;
				else if (label[d[j].trnum] == "sad") em[4].count++;
				else if (label[d[j].trnum] == "surprise") em[5].count++;
				int maxx = 0;
				string lb;
				for (int j = 0; j < 6; j++)
				{
					if (em[j].count >= maxx)
					{
						maxx = em[j].count;  //找到众数
						lb = em[j].es;   //记下标签
					}
				}
				if (lb == label[i]) cnt++;  //最终出来的这个标签就是答案
				//res << lb << "," << label[i] << endl;
		}
		cout << k << " " << cnt*1.0 / txt2 << endl; //统计正确率
		if (cnt > maxc)
		{
			maxc = cnt;
			maxk = k;
		}
	}
	k = maxk;  //让k取最大的正确率的k
	cout << k << endl;

	testin.getline(s, 500);
	while (!testin.eof())
	{
		testin.getline(s, 500);
		txt3++;
		const char *d = " ,";
		char *p;
		p = strtok(s, d);
		while (p)  
		{
			string ss = p;
			if (isdigit(ss[0]) || ss == "?")
			{
				p = strtok(NULL, d);
				continue;
			}
			int pos = search(p); 
			ori[txt1 + txt2 + txt3][0]++;
			if (pos > 0)
			{
				ori[txt1 + txt2 + txt3][pos]++;
				if (ori[txt1 + txt2 + txt3][pos] == 1) ori[0][pos]++;
			}
			else
			{
				num++;
				ori[txt1 + txt2 + txt3][num]++;
				ori[0][num]++;
				words[num] = p;
			}
			p = strtok(NULL, d);  
		}
	}
	for (int i = 1; i <= txt1 + txt2 + txt3; i++)
		for (int j = 1; j <= num; j++)
			if (ori[i][j] > 0) OH[i][j] = 1;
			else OH[i][j] = 0;
	for (int i = 1; i <= txt1 + txt2 + txt3; i++)               //这个双重循环算出TF矩阵
		for (int j = 1; j <= num; j++)
			TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
	for (int i = 1; i <= txt1 + txt2 + txt3; i++)               //这个双重循环算出TFIDF矩阵
		for (int j = 1; j <= num; j++)
			TFIDF[i][j] = TF[i][j] * log((txt1 + txt2 + txt3) * 1.0 / (ori[0][j] + 1)) / log(2);
	

	for (int i = 1; i <= txt3; i++)
	{
		for (int j = 1; j <= txt1 + txt2; j++)
			d[j].dis = 0;
		for (int j = 1; j <= txt1 + txt2; j++)
		{
			for (int l = 1; l <= num; l++)  
			{
				d[j].dis += abs(TFIDF[i + txt1 + txt2][l] - TFIDF[j][l]);
			}
			d[j].trnum = j;
		}
		sort(d + 1, d + txt1 + txt2, cmp);
		for (int j = 0; j < 6; j++)
			em[j].count = 0;
		for (int j = 1; j <= k; j++)
			if (label[d[j].trnum] == "anger") em[0].count++;
			else if (label[d[j].trnum] == "disgust") em[1].count++;
			else if (label[d[j].trnum] == "fear") em[2].count++;
			else if (label[d[j].trnum] == "joy") em[3].count++;
			else if (label[d[j].trnum] == "sad") em[4].count++;
			else if (label[d[j].trnum] == "surprise") em[5].count++;
			string lb;
			int maxx = 0;
			for (int j = 0; j < 6; j++)
			{
				if (em[j].count >= maxx)
				{
					maxx = em[j].count;
					lb = em[j].es;
				}
			}
			res << lb << endl;
	}
	return 0;
}
