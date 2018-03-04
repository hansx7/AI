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

int num, txt, cnt;                               //�ֱ��ǲ�ͬ�ĵ�������������������Ԫ���ֵ�ĸ���
int ori[1500][15000];                            //ԭʼ�ĵ���ͳ�ƾ������е�0�б�ʾÿ�������ڶ��ٸ��ı��г��ֹ�����idf�ã�����0�б�ʾÿ�仰�ж��ٸ����ʣ���tf�ã�
double TF[1500][15000], TFIDF[1500][15000];      //TF�����TFIDF����
string words[15000];                             //���ճ���˳���¼ÿһ������
triad sm, t1, t2, tsum;                          //�ֱ���onehot�������Ԫ�飬�����������Ԫ��ͽ����Ԫ��


int search(char *p)                              //�ڳ��ֹ��ĵ���������������Ǿɵ��ʾͷ���λ�ã����򷵻�-1��ʾ���µ���
{
	for (int i = 1; i <= num; i++)
	{
		if (words[i] == p) return i;
	}
	return -1;
}

void AplusB()
{
	for (int i = 0; i<t1.nums; i++)              //���t1�е�һ��Ԫ����t2�г��ֹ�����ֱ�Ӽ���ȥ
	{
		bool found = false;
		for (int j = 0; j<t2.nums; j++)
			if (t1.t[i][0] == t2.t[j][0] && t1.t[i][1] == t2.t[j][1])
			{
				t2.t[j][2] += t1.t[i][2];
				found = true;
				break;
			}
		if (!found)                              //������t2�¿�һ����Ԫ������t1�����Ԫ��
		{
			t2.t[t2.nums][0] = t1.t[i][0];
			t2.t[t2.nums][1] = t1.t[i][1];
			t2.t[t2.nums][2] = t1.t[i][2];
			t2.nums++;
		}
	}
	for (int i = 0; i<t2.nums - 1; i++)          //����t2����Ϊ����ľ��ǽ����ʹ�ð����������д�֮��˳�����
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
	while (!fin.eof())                           //52�к�54����һ��һ�У���һ��һ�䣬�����ļ��ķ���
	{
		fin.getline(s, 500);
		txt++;
		const char *d = "	 ";
		char *p;
		p = strtok(s, d);
		while (p)                                //���whileѭ�������ִ�
		{
			string ss = p;
			if (isdigit(p[0]) || ss.find(":", 0) < string::npos)
			{
				p = strtok(NULL, d);
				continue;
			}                                    //ȥ�����ֺͱ�ʾ��еĴ�
			int pos = search(p);                 //�ж����´ʻ��Ǿɴʲ�����ͬ����
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
			p = strtok(NULL, d);                 //�ֳ���һ�����ʣ�81�к�58��һ��ִ�
		}
	}
	txt--;                                       //ÿ�ζ����ͳ��һ���ı�����������֮��Ҫ��һ

	for (int i = 1; i <= txt; i++)
	{
		for (int j = 1; j < num; j++)
			if (ori[i][j] > 0)                   //���onehot�������ori�������1���ʾ���ֹ������1���������0
				onehot << 1 << " ";
			else
				onehot << 0 << " ";
		if (ori[i][num] > 0)
			onehot << 1 << endl;
		else
			onehot << 0 << endl;
	}

	for (int i = 1; i <= txt; i++)               //���˫��ѭ�����TF����������������ں��滹��������Ҫ��
	{
		for (int j = 1; j < num; j++)
		{
			TF[i][j] = ori[i][j] * 1.0 / ori[i][0];
			tf << fixed << setprecision(4) << TF[i][j] << " ";
		}
		TF[i][num] = ori[i][num] * 1.0 / ori[i][0];
		tf << fixed << setprecision(4) << TF[i][num] << endl;
	}

	for (int i = 1; i <= txt; i++)               //���˫��ѭ�����TFIDF����
	{
		for (int j = 1; j < num; j++)
		{
			TFIDF[i][j] = TF[i][j] * log(txt * 1.0 / (ori[0][j] + 1)) / log(2);
			tfidf << fixed << setprecision(4) << TFIDF[i][j] << " ";
		}
		TFIDF[i][num] = TF[i][num] * log(txt * 1.0 / (ori[0][num] + 1)) / log(2);
		tfidf << fixed << setprecision(4) << TFIDF[i][num] << endl;
	}

	for (int i = 1; i <= txt; i++)               //��ori����ó�smatrix
	{
		for (int j = 1; j <= num; j++)
		{
			if (ori[i][j] > 0)
			{
				sm.t[cnt][0] = i - 1;            //i��j����һ����Ϊ��1��ʼͳ�ƣ���0�к����ô���18�е�ע��
				sm.t[cnt][1] = j - 1;
				sm.t[cnt][2] = 1;
				cnt++;
			}
		}
	}
	smatrix << "[" << txt << "]" << endl << "[" << num << "]" << endl << "[" << cnt << "]" << endl;
	for (int i = 0; i < cnt; i++)
		smatrix << "[" << sm.t[i][0] << ", " << sm.t[i][1] << ", " << sm.t[i][2] << "]" << endl;

	t1in >> t1.rows >> t1.cols >> t1.nums;       //�����������Ԫ�����ӷ�
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
