from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import  train_test_split
x_data=[]
y_data=[]
f = open('stock_hist_info.csv')
f.readline()
for line in f:
    x_feature =[]
    line = line.strip().strip("\"")
    #print "input line:",line
    fields = line.split(";")
    #print "id:",fields[0]
    #print "amount:",fields[3]
    #print "close:",fields[4]
    #print
    #features 1 close-open/open  2 high-low/low 3 vr 4 tor 5 vol 6 ma5-close 7 close-open 8 ma5-ma10 9 ma5-open
    #print 'close:',fields[4]
    #print 'type:',type(float(fields[4]))
    close = float(fields[4])
    open  = float(fields[7])
    high  = float(fields[5])
    low   = float(fields[6])
    vr    = float(fields[13])
    tor   = float(fields[12])
    ma5   = float(fields[11])
    ma10  = float(fields[9])
    close_change_rate=(close-open)/open
    low_change_rate  =(high-low)/low
    vol   = int(fields[8])
    ma5_close = ma5-close
    close_open = close-open
    ma5_ma10  = ma5 - ma10
    x_feature.append(close_change_rate)
    x_feature.append(low_change_rate)
    x_feature.append(vr)
    x_feature.append(tor)
    x_feature.append(vol)
    x_feature.append(ma5_close)
    x_feature.append(close_open)
    x_feature.append(ma5_ma10)
    x_data.append(x_feature)
    #get label y
    if   ma5_ma10<=0 and close_open>0 and ma5_close>=0:
          # print 'eq 1 x:',x_feature
          y_data.append(1)
    elif ma5_ma10>=0 and close_open<0 and ma5_close>=0:
          # print 'eq -1 x:',x_feature
          y_data.append(-1)
    else:
          y_data.append(0)
#print 'x_data shape',len(x_data)
#print 'y_data shape',len(y_data)
#print 'x_data:',x_data
#print 'y_data:',y_data
num_1=0
num_F1=0
for y_flag in y_data:
   if y_flag==1:
       num_1+=1
   elif y_flag==-1:
       num_F1+=1
print 'eq 1 num: ',num_1
print 'eq -1 num: ',num_F1
#linear svc
clf = LinearSVC() #score: 0.7480   little
x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=0.3)
clf.fit(x_train,y_train)
print 'score: ',clf.score(x_test,y_test)

#svc
# clf = svm.SVC()   #score: 0.7450     use
# x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=0.3)
# clf.fit(x_train,y_train)
# print 'score: ',clf.score(x_test,y_test)

#knn
# knn = KNeighborsClassifier()  #score :0.7135
# x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=0.3)
# knn.fit(x_train,y_train)
# predicts = list(knn.predict(x_test))
# print 'predicts: ',predicts
# print 'real: ',y_test
# count = 0
# for i in range(len(predicts)):
#     if predicts[i]==y_test[i]:
#         count+=1
# print 'total test count: ',len(y_test)
# print 'same num:',count
# print 'real value: ',y_test
#print('clf.coef_: ',clf.coef_)
#print('clf.intercept_: ',clf.intercept_)
#probility=knn.predict_proba(iris_x_test)  knn
# print 'real: ','-1'*5,'1'*2
# print 'predict: ',knn.predict([\
# [-0.0029985007496251236, 0.009056603773584847, 1.38, 1.29, 2826, -0.1800000000000015, -0.03999999999999915, 0.0, -0.22000000000000064],\
# [-0.02247191011235947, 0.030092592592592497, 1.27, 1.6, 3492, -0.11000000000000121, -0.29999999999999893, 0.0, -0.41000000000000014],\
# [-0.006433166547533942, 0.014430014430014508, 1.09, 0.07, 309, 0.08000000000000007, -0.08999999999999986, 0.0, -0.009999999999999787],\
# [-0.03903903903903896, 0.0471698113207546, 0.58, 3.47, 14823, 0.5700000000000003, -0.6499999999999986, 0.0, -0.0799999999999983],\
# [-0.0014285714285713982, 0.005734767025089611, 0.46, 0.06, 276, -0.019999999999999574, -0.019999999999999574, 0.0, -0.03999999999999915],\
# [0.11538461538461539, 0.13458528951486703, 6.6, 3.29, 9352, -0.39000000000000057, 1.5, 0.0, 1.1099999999999994],\
# [0.0071428571428571175, 0.012160228898426318, 0.35, 0.43, 1233, 0.009999999999999787, 0.09999999999999964, 0.0, 0.10999999999999943],\
# ])
#
# print 'predict: ',knn.predict_proba([\
# [-0.0029985007496251236, 0.009056603773584847, 1.38, 1.29, 2826, -0.1800000000000015, -0.03999999999999915, 0.0, -0.22000000000000064],\
# [-0.02247191011235947, 0.030092592592592497, 1.27, 1.6, 3492, -0.11000000000000121, -0.29999999999999893, 0.0, -0.41000000000000014],\
# [-0.006433166547533942, 0.014430014430014508, 1.09, 0.07, 309, 0.08000000000000007, -0.08999999999999986, 0.0, -0.009999999999999787],\
# [-0.03903903903903896, 0.0471698113207546, 0.58, 3.47, 14823, 0.5700000000000003, -0.6499999999999986, 0.0, -0.0799999999999983],\
# [-0.0014285714285713982, 0.005734767025089611, 0.46, 0.06, 276, -0.019999999999999574, -0.019999999999999574, 0.0, -0.03999999999999915],\
# [0.11538461538461539, 0.13458528951486703, 6.6, 3.29, 9352, -0.39000000000000057, 1.5, 0.0, 1.1099999999999994],\
# [0.0071428571428571175, 0.012160228898426318, 0.35, 0.43, 1233, 0.009999999999999787, 0.09999999999999964, 0.0, 0.10999999999999943],\
# ])
# print 'score: ',knn.score(x_test,y_test)
print 'end!'