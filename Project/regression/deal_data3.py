import numpy as np
import datetime

#归一化
def normalization(x):
    return (x-x.min())/(x.max()-x.min())

def process(x, day):
    
    #来自TA提供的网站
    holiday = ['2011/1/17','2011/2/21','2011/4/15','2011/5/30','2011/7/4','2011/9/5','2011/10/10',
               '2011/11/11','2011/11/24','2011/12/26','2012/1/2','2012/1/16','2012/2/20','2012/4/16',
               '2012/5/28','2012/7/4','2012/9/3','2012/10/8','2012/11/12','2012/11/22','2012/12/25']
    
    #删除count大于5000的列-->噪声
    select = []
    for i in range(x.shape[0]):
        if x[i,-1:].astype(float) < 5000:
            select.append(x[i])
    x = np.array(select)
    #增加六列 第一列为年份， 第二列为季度， 第三列为月份， 第四列为日期， 第五列为周几， 第六列为是否是假期
    global extend_attr
    extend_attr = np.zeros((x.shape[0],6),dtype=float)
    for i in range(x.shape[0]):
        if x[i,0] in holiday:
            extend_attr[i,5] = 1
    for i in range(x.shape[0]):
        date = datetime.datetime.strptime(x[i,0],"%Y/%m/%d")
        extend_attr[i,4] = date.strftime('%w')
        y,m,d = x[i,0].split('/')
        if y == "2011":
            extend_attr[i,0] = 0
        elif y == '2012':
            extend_attr[i,0] = 1
        if int(m) >= 1 and int(m) <= 3:
            extend_attr[i,1] = 0
        elif int(m) >= 4 and int(m) <= 6:
            extend_attr[i,1] = 1
        elif int(m) >= 7 and int(m) <= 9:
            extend_attr[i,1] = 2
        elif int(m) >= 10 and int(m) <= 12:
            extend_attr[i,1] = 3
        
        extend_attr[i,2] = float(m)
        extend_attr[i,3] = float(d)
    x = np.c_[extend_attr,np.delete(x,0,axis=1)]
    
    #处理噪声
    global clear_x
    clear_x = []
    for i in range(x.shape[0]):
        if "?" not in x[i,:] and "" not in x[i,:]:
            clear_x.append(x[i,:])
    clear_x = np.array(clear_x, dtype=float)

    #特征：
    #dteday 不合法日期
    #hr ?
    #weather ?
    #temp ?
    #atemp ? ''
    #hum ?
    #windspeed ?
    
    return clear_x
    
        
def read_data(filename,type_of_file):
    dataset = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=(range(1,9)), dtype=np.str)
    
    if type_of_file == 'test':
        dataset[:,-1:] = np.zeros((dataset.shape[0],1)) #y全部置为1
    
    holiday = np.loadtxt('holiday.csv', dtype=np.str)
    weekend = np.loadtxt('weekends.csv', dtype=np.str)
    day = np.concatenate([holiday,weekend], axis=0)
    dataset = process(dataset, day)
    
    '''
    for i in range(dataset.shape[1]):
        dataset[:,i] = normalization(dataset[:,i])
    
    '''
    
    return dataset

dataset1 = read_data('train.csv','train')
dataset2 = read_data('test.csv','test')

np.savetxt('train1.csv', dataset1, delimiter=',', fmt='%g')
np.savetxt('test1.csv', dataset2, delimiter=',', fmt='%g')