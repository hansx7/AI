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
	double dis, dis2;
};

int num, txt1, txt2, txt3;                       //�ֱ��ǲ�ͬ�ĵ���������ѵ��������֤���Ͳ��Լ������� 
int ori[1500][15000];                            //ԭʼ�ĵ���ͳ�ƾ������е�0�б�ʾÿ�������ڶ��ٸ��ı��г��ֹ�����idf�ã�����0�б�ʾÿ�仰�ж��ٸ����ʣ���tf�ã�
int OH[1500][15000];                             //onehot���� 
double TF[1500][15000], TFIDF[1500][15000];      //TF�����TFIDF����
string words[15000];                             //���ճ���˳���¼ÿһ������
string label[1500];                              //��¼ѵ������ÿ���ı���label����֤���Ĵ� 
int k, cnt;
double emotion[1500][6], ans[1500][6];
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
	return x.dis<y.dis;
}

int main()
{
	ifstream trainin("train_set.csv");
	ifstream validationin("validation_set.csv");
	ifstream testin("test_set.csv");
	ofstream trainout("train_set_copy.csv");
	ofstream validationout("validation_set_copy.csv");
	ofstream testout("test_set_copy.csv");
	ifstream trainin2("train_set_copy.csv");
	ifstream validationin2("validation_set_copy.csv");
	ifstream testin2("test_set_copy.csv");
	ofstream res("res.csv");

	if (!trainin)
	{
		cout << "404!\n";
		return 0;
	}
	char s[500];
	num = 0;
	txt1 = txt2 = txt3 = 1;
	memset(ori, 0, sizeof(ori));
	trainin.getline(s, 500);
	while (!trainin.eof())
	{
		trainin.getline(s, 500);
		for (int j = 0; j<strlen(s); j++)
			if (s[j] == ' ' || s[j] == ',') trainout << endl;
			else trainout << s[j];
			trainout << endl;
	}
	validationin.getline(s, 500);
	while (!validationin.eof())
	{
		validationin.getline(s, 500);
		for (int j = 0; j<strlen(s); j++)
			if (s[j] == ' ' || s[j] == ',') validationout << endl;
			else validationout << s[j];
			validationout << endl;
	}
	testin.getline(s, 500);
	while (!testin.eof())
	{
		testin.getline(s, 500);
		for (int j = 0; j<strlen(s); j++)
			if (s[j] == ' ' || s[j] == ',') testout << endl;
			else testout << s[j];
			testout << endl;
	}

	while (!trainin2.eof())      
	{
		trainin2.getline(s, 500);
		if (isdigit(s[0]))
		{
			emotion[txt1][0] = atof(s);
			for (int j = 1; j<6; j++)
			{
				trainin2.getline(s, 500);
				emotion[txt1][j] = atof(s);
			}
			txt1++;
		}
		else
		{
			int pos = search(s);                 //�ж����´ʻ��Ǿɴʲ�����ͬ����
			ori[txt1][0]++;
			if (pos > 0)
			{
				ori[txt1][pos]++;
				if (ori[txt1][pos] == 1) ori[0][pos]++;
			}
			else
			{
				num++;
				ori[txt1][num]++;
				ori[0][num]++;
				words[num] = s;
			}
		}
	}
	txt1--;                                      //ÿ�ζ����ͳ��һ���ı�����������֮��Ҫ��һ

	while (!validationin2.eof())    {                
		validationin2.getline(s, 500);
		if (isdigit(s[0]))
		{
			emotion[txt1 + txt2][0] = atof(s);
			for (int j = 1; j<6; j++)
			{
				validationin2.getline(s, 500);
				emotion[txt1 + txt2][j] = atof(s);
			}
			txt2++;
		}
		else
		{
			int pos = search(s);                 //�ж����´ʻ��Ǿɴʲ�����ͬ����
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
				words[num] = s;
			}
		}
	}
	txt2--;
	for (int i = 1; i <= txt1 + txt2; i++)
		for (int j = 1; j <= num; j++)
			if (ori[i][j]>0) OH[i][j] = 1;
			else OH[i][j] = 0;
			for (int i = 1; i <= txt1 + txt2; i++)               //���˫��ѭ�����TF����������������ں��滹��������Ҫ��
			{
				for (int j = 1; j <= num; j++)
					TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
			}
			for (int i = 1; i <= txt1 + txt2; i++)               //���˫��ѭ�����TFIDF����
			{
				for (int j = 1; j <= num; j++)
					TFIDF[i][j] = TF[i][j] * log((txt1 + txt2) * 1.0 / (ori[0][j] + 1)) / log(2);
			}

			k = txt1;
			memset(ans, 0, sizeof(ans));
			for (int i = 1; i <= txt2; i++)
			{
				for (int j = 1; j <= txt1; j++)
					d[j].dis = 0;
				for (int j = 1; j <= txt1; j++)
				{
					for (int l = 1; l <= num; l++)
					{
						d[j].dis += abs(TFIDF[i + txt1][l] - TFIDF[j][l]);
					}
					d[j].dis2 = 1.0 / d[j].dis;
				}
				double sum = 0;
				for (int j = 1; j <= k; j++)
				{
					for (int l = 0; l<6; l++)
					{
						sum += d[j].dis2*emotion[j][l];
						ans[i][l] += d[j].dis2*emotion[j][l];
					}
				}
				for (int j = 0; j<6; j++)
				{
					ans[i][j] = ans[i][j] * 1.0 / sum;
					res << ans[i][j] << ",";
				}
				res << "line" << endl;
			}

			while (!testin2.eof())
			{
				testin2.getline(s, 500);
				if (isdigit(s[0]))
				{
					emotion[txt1 + txt2 + txt3][0] = atof(s);
					for (int j = 1; j<6; j++)
					{
						testin2.getline(s, 500);
						emotion[txt1 + txt2 + txt3][j] = atof(s);
					}
					txt3++;
				}
				else
				{
					int pos = search(s);                 //�ж����´ʻ��Ǿɴʲ�����ͬ����
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
						words[num] = s;
					}
				}
			}
			txt3--;
			for (int i = 1; i <= txt1 + txt2 + txt3; i++)
				for (int j = 1; j <= num; j++)
					if (ori[i][j]>0) OH[i][j] = 1;
					else OH[i][j] = 0;
					for (int i = 1; i <= txt1 + txt2 + txt3; i++)               //���˫��ѭ�����TF����������������ں��滹��������Ҫ��
					{
						for (int j = 1; j <= num; j++)
							TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
					}
					for (int i = 1; i <= txt1 + txt2 + txt3; i++)               //���˫��ѭ�����TFIDF����
					{
						for (int j = 1; j <= num; j++)
							TFIDF[i][j] = TF[i][j] * log((txt1 + txt2) * 1.0 / (ori[0][j] + 1)) / log(2);
					}

					memset(ans, 0, sizeof(ans));
					for (int i = 1; i <= txt3; i++)
					{
						for (int j = 1; j <= txt1; j++)
							d[j].dis = 0;
						for (int j = 1; j <= txt1; j++)
						{
							for (int l = 1; l <= num; l++)
							{
								d[j].dis += abs(TFIDF[i + txt1 + txt2][l] - TFIDF[j][l]);
							}
							d[j].dis2 = 1.0 / d[j].dis;
						}
						double sum = 0;
						for (int j = 1; j <= k; j++)
						{
							for (int l = 0; l<6; l++)
							{
								sum += d[j].dis2*emotion[j][l];
								ans[i][l] += d[j].dis2*emotion[j][l];
							}
						}
						for (int j = 0; j<6; j++)
						{
							ans[i][j] = ans[i][j] * 1.0 / sum;
							res << ans[i][j] << ",";
						}
						res << endl;
					}
					return 0;
}
