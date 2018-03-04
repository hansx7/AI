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

int num, txt1, txt2, txt3;    //�ֱ��ǲ�ͬ�ĵ���������ѵ��������֤���Ͳ��Լ������� 
int ori[1500][15000];     //ԭʼ�ĵ���ͳ�ƾ���
						  //���е�0�б�ʾÿ�������ڶ��ٸ��ı��г��ֹ�����idf�ã�����0�б�ʾÿ�仰�ж��ٸ����ʣ���tf�ã�
int OH[1500][15000];             //onehot���� 
double TF[1500][15000], TFIDF[1500][15000];    //TF�����TFIDF����
string words[15000];       //���ճ���˳���¼ÿһ������
string label[1500];     //��¼ѵ������ÿ���ı���label����֤���Ĵ� 
int k, cnt;
emotion em[6];
dist d[1500];                                    //��¼���� 

int search(char *p)                              //�ڳ��ֹ��ĵ���������������Ǿɵ��ʾͷ���λ�ã����򷵻�-1��ʾ���µ���
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
	while (!trainin.eof())       //һ��һ�ж���ѵ����
	{
		trainin.getline(s, 500);
		txt1++;
		const char *d = " ";
		char *p;
		p = strtok(s, d);
		while (p)                                //���whileѭ�������ִ�
		{
			string ss = p;
			int comma = ss.find(",", 0);
			if (comma < string::npos)
			{
				label[txt1] = ss.substr(comma + 1, ss.length() - comma - 1);
				p[comma] = '\0';
			}
			int pos = search(p);         //�ж����´ʻ��Ǿɴʲ�����ͬ����
			ori[txt1][0]++;
			if (pos > 0)    //�ɵ���ֱ���ҵ�λ�ã�ͳ��ori
			{
				ori[txt1][pos]++;
				if (ori[txt1][pos] == 1) ori[0][pos]++;
			}
			else    //�µ������¿�һ��λ�ã�ͳ��ori��¼��words
			{
				num++;
				ori[txt1][num]++;
				ori[0][num]++;
				words[num] = p;
			}
			p = strtok(NULL, d);       //�ֳ���һ�����ʣ�81�к�58��һ��ִ�
		}

	}
	txt1--;                                      //ÿ�ζ����ͳ��һ���ı�����������֮��Ҫ��һ

	validationin.getline(s, 500);
	while (!validationin.eof())
	{
		validationin.getline(s, 500);
		txt2++;
		const char *d = " ";
		char *p;
		p = strtok(s, d);
		while (p)                       //���whileѭ�������ִ�
		{
			string ss = p;
			int comma = ss.find(",", 0);
			if (comma < string::npos)
			{
				label[txt2] = ss.substr(comma + 1, ss.length() - comma - 1);
				p[comma] = '\0';
			}
			int pos = search(p);      //�ж����´ʻ��Ǿɴʲ�����ͬ����
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
	
	for (int i = 1; i <= txt1 + txt2; i++)               //���˫��ѭ�����onehot����
		for (int j = 1; j <= num; j++)
			if (ori[i][j] > 0) OH[i][j] = 1;
			else OH[i][j] = 0;
	for (int i = 1; i <= txt1 + txt2; i++)               //���˫��ѭ�����onehot����
	{for (int j = 1; j <= num; j++)
			res << OH[i][j] <<",";
		res<<endl;
	}	
	for (int i = 1; i <= txt1 + txt2; i++)               //���˫��ѭ�����TF����
		for (int j = 1; j <= num; j++)
			TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
	for (int i = 1; i <= txt1 + txt2; i++)               //���˫��ѭ�����TFIDF����
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
			for (int j = 1; j <= txt1; j++) //���ѵ��������֤��ÿһ������֮��ľ���
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
			sort(d + 1, d + txt1, cmp); //�����еľ�������
			for (int j = 0; j < 6; j++)
				em[j].count = 0;
			for (int j = 1; j <= k; j++)  //ȡ��ǰk����ѵ���ı�
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
						maxx = em[j].count;  //�ҵ�����
						lb = em[j].es;   //���±�ǩ
					}
				}
				if (lb == label[i]) cnt++;  //���ճ����������ǩ���Ǵ�
				//res << lb << "," << label[i] << endl;
		}
		cout << k << " " << cnt*1.0 / txt2 << endl; //ͳ����ȷ��
		if (cnt > maxc)
		{
			maxc = cnt;
			maxk = k;
		}
	}
	k = maxk;  //��kȡ������ȷ�ʵ�k
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
	for (int i = 1; i <= txt1 + txt2 + txt3; i++)               //���˫��ѭ�����TF����
		for (int j = 1; j <= num; j++)
			TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
	for (int i = 1; i <= txt1 + txt2 + txt3; i++)               //���˫��ѭ�����TFIDF����
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
