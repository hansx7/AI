#include <iostream>
#include <fstream>
#include <cstdio>
#include <iomanip>
#include <string.h>
#include <stdio.h>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <set> 

using namespace std;

struct emotion {
	string es;
	int ne, nw, ve;        //文本个数、单词总数和不重复单词总数
	string ewords[10000];
};

int num, txt1, txt2;                       //分别是不同的单词总数，训练集、验证集和测试集句子数 
int ori[1500][15000];                            //原始的单词统计矩阵。其中第0行表示每个单词在多少个文本中出现过（算idf用），第0列表示每句话有多少个单词（算tf用）
int nwe[6][15000];        //每个单词在不同标签中出现次数
string words[15000];                             //按照出现顺序记录每一个单词
string label[1500];                              //记录训练集中每个文本的label和验证集的答案 
int k, cnt, emod;
emotion em[6];

int search(char *p)                              //在出现过的单词中搜索，如果是旧单词就返回位置，否则返回-1表示是新单词
{
	for (int i = 1; i <= num; i++)
	{
		if (words[i] == p) return i; 
	}
	return -1;
}
int search2(char *p)
{
	for (int i = 0; i < em[emod].nw; i++)
	{
		if (em[emod].ewords[i] == p) return i;
	}
	return -1;
}

int emorder(string emo)
{
	if (emo == "anger") return 0;
	else if (emo == "disgust") return 1;
	else if (emo == "fear") return 2;
	else if (emo == "joy") return 3;
	else if (emo == "sad") return 4;
	else if (emo == "surprise") return 5;
}

int main()
{
	ifstream trainin("train_set.csv");
	ifstream validationin("validation_set.csv");
	ifstream testin("test_set.csv");
	ofstream res("res.csv");

	if (!trainin)
	{
		cout << "404!\n";
		return 0;
	}

	em[0].es = "anger";
	em[1].es = "disgust";
	em[2].es = "fear";
	em[3].es = "joy";
	em[4].es = "sad";
	em[5].es = "surprise";
	for (int i = 0; i<6; i++)
		em[i].ne = em[i].nw = em[i].ve = 0;
	memset(nwe, 0, sizeof(nwe));

	char s[500];
	num = txt1 = txt2 = 0;
	memset(ori, 0, sizeof(ori));
	trainin.getline(s, 500);
	while (!trainin.eof())                      
	{
		trainin.getline(s, 500);
		txt1++;
		string ss = s;
		int comma = ss.find(",", 0);
		if (comma < string::npos)
		{
			label[txt1] = ss.substr(comma + 1, ss.length() - comma - 1);
			emod = emorder(label[txt1]);
			em[emod].ne++;
			s[comma] = '\0';
		}
		const char *d = " ";
		char *p;
		p = strtok(s, d);
		while (p)                                //这个while循环用来分词
		{
			int pos = search(p);                 //判断是新词还是旧词并做不同处理
			em[emod].nw++;
			if (pos>0)     //这是一个旧单词
			{
				nwe[emod][pos]++;  //原位置加一即可
			}
			else
			{
				num++;     //新单词要新开位置
				nwe[emod][num]++;
				words[num] = p;
			}
			if (search2(p)<0)
			{                      //标签中的新单词要记录下来
				em[emod].ewords[em[emod].ve] = p;
				em[emod].ve++;
			}
			p = strtok(NULL, d);                 //分出下一个单词，81行和58行一起分词
		}
	}
	txt1--;                                      //每次都会多统计一个文本，所以做完之后要减一

	cnt = 0;
	validationin.getline(s, 500);
	while (!validationin.eof())         
	{
		validationin.getline(s, 500);
		txt2++;
		const char *d = " ";
		char *p;
		p = strtok(s, d);
		double pe[6];
		int num2 = 0;
		for (int i = 0; i<6; i++)
		{
			pe[i] = em[i].ne*1.0 / txt1;
			num2 += em[i].ve;
		}
		while (p)                                //这个while循环用来分词
		{
			string ss = p;
			int comma = ss.find(",", 0);
			if (comma < string::npos)
			{
				label[txt2] = ss.substr(comma + 1, ss.length() - comma - 1);
				p[comma] = '\0';
			}
			for (emod = 0; emod<6; emod++)
			{  //按照公式统计每个单词在各个标签下的先验概率
				int pos = search(p);
				if (pos<0) pos = 0;
				pe[emod] *= ((nwe[emod][pos] + 1)*1.0 / (em[emod].nw + num2));
			}
			p = strtok(NULL, d);
		}
		string lb;
		double maxx = 0;
		for (int i = 0; i<6; i++)
		{
			if (pe[i]>maxx)
			{
				maxx = pe[i];
				lb = em[i].es;
			}
		}
		if (lb == label[txt2]) cnt++;
	}
	txt2--;
	cout << cnt*1.0 / txt2 << endl;


	cnt = 0;
	testin.getline(s, 500);
	while (!testin.eof())          
	{
		testin.getline(s, 500);
		const char *d = " ,";
		char *p;
		p = strtok(s, d);
		double pe[6];
		int num2 = 0;
		for (int i = 0; i<6; i++)
		{
			pe[i] = em[i].ne*1.0 / txt1;
			num2 += em[i].ve;
		}
		while (p)                         
		{
			if (isdigit(p[0]) || p[0] == '?')
			{
				p = strtok(NULL, d);
				continue;
			}
			string ss = p;
			int comma = ss.find(",", 0);
			if (comma < string::npos)
			{
				label[txt2] = ss.substr(comma + 1, ss.length() - comma - 1);
				p[comma] = '\0';
			}
			for (emod = 0; emod<6; emod++)
			{
				int pos = search(p);
				if (pos<0) pos = 0;
				pe[emod] *= ((nwe[emod][pos] + 1)*1.0 / (em[emod].nw + num2));
			}
			p = strtok(NULL, d);
		}
		string lb;
		double maxx = 0;
		for (int i = 0; i<6; i++)
		{
			if (pe[i]>maxx)
			{
				maxx = pe[i];
				lb = em[i].es;
			}
		}
		res << lb << endl;
	}

	return 0;
}
