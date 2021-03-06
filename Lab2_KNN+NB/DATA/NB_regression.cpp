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

int num, txt1, txt2, txt3;                       //分别是不同的单词总数，训练集、验证集和测试集句子数 
int ori[1500][15000];                            //原始的单词统计矩阵。其中第0行表示每个单词在多少个文本中出现过（算idf用），第0列表示每句话有多少个单词（算tf用）
int OH[1500][15000];                             //onehot矩阵 
double TF[1500][15000], TFIDF[1500][15000];      //TF矩阵和TFIDF矩阵
string words[15000];                             //按照出现顺序记录每一个单词
string label[1500];                              //记录训练集中每个文本的label和验证集的答案 
double emotion[1500][6], ans[1500][6];
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

	while (!trainin2.eof())                           //52行和54行是一行一行，即一句一句，读入文件的方法
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
			int pos = search(s);                 //判断是新词还是旧词并做不同处理
			ori[txt1][0]++;
			if (pos > 0)
			{
				ori[txt1][pos]++;
				if (ori[txt1][pos] == 1) ori[0][pos]++;
			}
			else
			{
				num++;
				ori[txt1][num]++;   //统计ori
				ori[0][num]++;
				words[num] = s;
			}
		}
	}
	txt1--;                                      //每次都会多统计一个文本，所以做完之后要减一
	int num2 = num;
	while (!validationin2.eof())                      
	{
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
			int pos = search(s);                 //判断是新词还是旧词并做不同处理
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
		for (int j = 1; j <= num; j++)  //算出onehot
			if (ori[i][j]>0) OH[i][j] = 1;
			else OH[i][j] = 0;
	for (int i = 1; i <= txt1 + txt2; i++)               //这个双重循环算出TF矩阵
	{
		for (int j = 1; j <= num; j++)
		{
			TF[i][j] = (ori[i][j] + 1) * 1.0 / (ori[i][0] + num2);
		}   //加入拉普拉斯平滑
	}

			memset(ans, 0, sizeof(ans));
			for (int i = 1; i <= txt2; i++) //验证集
			{
				double pe[6], sum = 0;
				for (int j = 0; j<6; j++) //情感
				{
					pe[j] = 0;
					for (int k = 1; k <= num2; k++) //训练集
					{
						double temp = emotion[k][j];
						for (int l = 1; l <= num; l++)  //单词
							if (ori[i + txt1][l]>0) temp *= TF[k][l];
						pe[j] += temp;
					}
					sum += pe[j];
				}
				for (int j = 0; j<6; j++)
				{
					pe[j] = pe[j] / sum;
					res << pe[j] << ",";
				}
				res << "line" << endl;
			}

			while (!testin2.eof())
			{
				testin2.getline(s, 500);
				if (isdigit(s[0])) txt3++;
				if (s[0] == '?')
				{
					//testin2.getline(s, 500);
					continue;
				}
				int pos = search(s);               
				ori[txt1 + txt2 + txt3][0]++;
				if (pos > 0)
				{
					ori[txt1 + txt2 +txt3][pos]++;
					if (ori[txt1 + txt2 +txt3][pos] == 1) ori[0][pos]++;
				}
				else
				{
					num++;
					ori[txt1 + txt2 + txt3][num]++;
					ori[0][num]++;
					words[num] = s;
				}
			}
			txt3--;
			for (int i = 1; i <= txt1 + txt2 + txt3; i++)
				for (int j = 1; j <= num; j++)
					if (ori[i][j]>0) OH[i][j] = 1;
					else OH[i][j] = 0;
					for (int i = 1; i <= txt1 + txt2 +txt3; i++)               //这个双重循环输出TF矩阵，由于这个矩阵在后面还有用所以要存
					{
						for (int j = 1; j <= num; j++)
						{
							TF[i][j] = (ori[i][j] + 1) * 1.0 / (ori[i][0] + num2);
						}
					}

					memset(ans, 0, sizeof(ans));
					for (int i = 1; i <= txt3; i++)
					{
						double pe[6], sum = 0;
						for (int j = 0; j<6; j++)
						{
							pe[j] = 0;
							for (int k = 1; k <= num2; k++)
							{
								double temp = emotion[k][j];
								for (int l = 1; l <= num; l++)
									if (ori[i + txt1 + txt2][l]>0) temp *= TF[k][l];
								pe[j] += temp;
							}
							sum += pe[j];
						}
						for (int j = 0; j<6; j++)
						{
							pe[j] = pe[j] / sum;
							res << pe[j] << ",";
						}
						res << endl;
					}
			return 0;
}
