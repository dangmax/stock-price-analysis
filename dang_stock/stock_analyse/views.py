# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.shortcuts import render_to_response
from stock_analyse.forms import StockForms
import tushare as ts
from stock_analyse.models import Stock
import math
from sklearn.linear_model import Ridge
from sklearn import svm
from sklearn.model_selection import train_test_split
import csv
from sklearn.externals import joblib
import pandas as pd

# query stock hist info & store in db
def query_hist(request):
    if request.method =='POST':
        form = StockForms(request.POST)
        if form.is_valid():
            data  = form.cleaned_data
            name  = data["Symbol"]
            start = data["start_date"]
            end   = data["end_date"]
            # print "name:",name,"start:",start,"end:",end
            stock_name = ts.get_realtime_quotes(name)['name'][0]
            # query in db
            data0 = []
            listma5 = []
            listma10 = []
            listma20 = []
            today = []
            result = Stock.objects.filter(stock_id=name).filter(pub_date__range=(start,end)).order_by('id')
            if result.count()!= 0:
                today_stock_info = Stock.objects.filter(stock_id=name).last()
                today.append(today_stock_info.vol)
                today.append(today_stock_info.high)
                today.append(today_stock_info.low)
                today.append(today_stock_info.open)
                today.append(today_stock_info.close)
                today.append(today_stock_info.tor)
                today.append(today_stock_info.vr)
                today.append(today_stock_info.ma5)
                today.append(today_stock_info.ma10)

                for res in result:
                    stockItem = []
                    stockItem.append(str(res.pub_date).encode(encoding='UTF-8'))
                    stockItem.append(res.open)
                    stockItem.append(res.close)
                    stockItem.append(res.low)
                    stockItem.append(res.high)
                    data0.append(stockItem)
                    listma5.append(res.ma5)
                    listma10.append(res.ma10)
                    listma20.append(res.ma20)

            else:
                print 'begin to crawl data!'
                cons = ts.get_apis()
                # df = ts.get_h_data(name, start=start, end=end)
                df = ts.bar(name, conn=cons, freq='D', start_date=start, ma=[5, 10, 20],factors=['vr', 'tor'])
                df = df.sort_index();
                today_stock_info = df[-1:]
                today.append(today_stock_info['vol'][0])
                today.append(today_stock_info['high'][0])
                today.append(today_stock_info['low'][0])
                today.append(today_stock_info['open'][0])
                today.append(today_stock_info['close'][0])
                today.append(today_stock_info['tor'][0])
                today.append(today_stock_info['vr'][0])
                today.append(today_stock_info['ma5'][0])
                today.append(today_stock_info['ma10'][0])
                for ix,row in df.iterrows():
                    stockItem = []
                    stock_id= name
                    open    = row['open']
                    close   = row['close']
                    high    = row['high']
                    low     = row['low']
                    vol     = row['vol']
                    amount  = row['amount']
                    tor     = row['tor']
                    vr      = row['vr']
                    ma5     = row['ma5']
                    ma10    = row['ma10']
                    ma20    = row['ma20']

                    if math.isnan(ma5) or math.isnan(ma10) or math.isnan(ma20) or math.isnan(tor) or math.isnan(vr):
                        continue

                    stock = Stock(stock_id=stock_id,open=open,close=close,high=high,amount=amount,vol=vol,low=low,pub_date=ix,
                                  tor=tor, vr=vr, ma5=ma5, ma10=ma10, ma20=ma20)
                    stock.save()
                    stockItem.append(str(stock.pub_date)[0:10])
                    stockItem.append(stock.open)
                    stockItem.append(stock.close)
                    stockItem.append(stock.low)
                    stockItem.append(stock.high)
                    stockItem.append(stock.amount)
                    stockItem.append(stock.vol)
                    stockItem.append(stock.tor)
                    stockItem.append(stock.vr)
                    stockItem.append(stock.ma5)
                    stockItem.append(stock.ma10)
                    data0.append(stockItem)
                    listma5.append(stock.ma5)
                    listma10.append(stock.ma10)
                #generate stock hist data csv
                #df.to_csv(name+'.csv',encoding='utf-8')
                #gen_csv(name,data0)
                #training model
                train_value_model(name,data0)
                train_cond_model(name, data0)
            #predict tomorrow
            close_predict = pre_price(name,today)
            cond = pre_cond(name, today)
            if cond==1:
                gaga = '涨'
            elif cond==-1:
                gaga = '跌'
            else:
                gaga = '平'
            return render_to_response('kline.html',{'data0':data0,'close_predict':close_predict,'cond':gaga,'stock_name':stock_name,
                                                    'listma5':listma5,'listma10':listma10,'listma20':listma20})
    if request.method == 'GET':
        form = StockForms()
        return render_to_response('index.html',{'form':form})

# predict tomorrow close price with model
def pre_price(name,today):
    #print 'today: ',today
    hl_pct = (today[1]-today[2])/today[2]*100.0
    ch_pct = (today[4]-today[3])/today[3]*100.0
    ma5_close_pct = (today[4]-today[7])/today[7]*100.0
    ma5_ma10_pct  = (today[7]/today[8])*100.0
    today_info = []
    today_info.append(today[0])
    today_info.append(hl_pct)
    today_info.append(ch_pct)
    today_info.append(today[4])
    today_info.append(today[5])
    today_info.append(today[6])
    today_info.append(ma5_close_pct)
    today_info.append(ma5_ma10_pct)
    today = []
    today.append(today_info)
    # print 'today: ',today
    #load model
    #print 'today: ', today
    clf = joblib.load('models/val_'+name+'_clf.pkl')
    close_predict = clf.predict(today)
    return close_predict

# predict tomorrow cond with model
def pre_cond(name,today):
    hl_pct = (today[1]-today[2])/today[2]*100.0
    ch_pct = (today[4]-today[3])/today[3]*100.0
    ma5_close_pct = (today[4]-today[7])/today[7]*100.0
    ma5_ma10_pct  = (today[7]/today[8])*100.0
    today_info = []
    today_info.append(today[0])
    today_info.append(hl_pct)
    today_info.append(ch_pct)
    today_info.append(today[4])
    today_info.append(today[5])
    today_info.append(today[6])
    today_info.append(ma5_close_pct)
    today_info.append(ma5_ma10_pct)
    today = []
    today.append(today_info)
    # print 'today: ',today
    #load model
    clf = joblib.load('models/cond_'+name+'_clf.pkl')
    cond = clf.predict(today)
    return cond

# def gen_csv(name,data0):
#     with open('data/'+name+".csv","wb") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['pub_date','open','close','low','high','amount','vol','tor','vr','ma5','ma10','ma20'])
#         writer.writerows(data0)

def train_value_model(name,data):
    # hist_name = 'data/'+name+'.csv'
    # f = pandas.read_csv(hist_name,sep='\,')
    # f = Stock.objects.filter(stock_id=name)
    f = pd.DataFrame(data,columns=['pub_date','open','close','low','high','amount','vol','tor','vr','ma5','ma10'])
    next_day_close = f["close"].iloc[:-1]
    #print next_day_close
    f = f.iloc[1:,1:]
    f['next_close'] = next_day_close.values  
    #Ridge regression
    clf = Ridge(alpha=1.0)
    x_data = f.iloc[:,:-1]
    x_data['hl_pct'] = (x_data['high']-x_data['low'])/x_data['low']*100.0
    x_data['ch_pct'] = (x_data['close']-x_data['open'])/x_data['open']*100.0
    x_data['ma5_close_pct'] = (x_data['close']-x_data['ma5'])/x_data['ma5']*100.0
    x_data['ma5_ma10_pct'] = (x_data['ma5']/x_data['ma10'])*100.0
    x_data = x_data[['vol','hl_pct','ch_pct','close','tor','vr','ma5_close_pct','ma5_ma10_pct']]
    y_data = f["next_close"]
    x_train,x_test,y_train,y_test =  train_test_split(x_data,y_data,test_size=0.3)
    clf.fit(x_train,y_train)
    y_test_predicts = clf.predict(x_test)
    mse = sum((y_test-y_test_predicts)**2)
    mse /=  len(y_test_predicts)
    print 'value mse: ',mse
    print 'value score: ',clf.score(x_test,y_test)
    joblib.dump(clf,'models/val_'+name+'_clf.pkl')

def train_cond_model(name, data):
    f = pd.DataFrame(data,
                     columns=['pub_date', 'open', 'close', 'low', 'high', 'amount', 'vol', 'tor', 'vr', 'ma5', 'ma10'])
    x_data = f.iloc[1:, 1:]
    f["next_cond"] = f["close"].iloc[:-1]-f["open"].iloc[:-1]
    next_cond =[]
    f= f.iloc[:-1]
    for i in range(f["next_cond"].size):
        if f["next_cond"][i]>0:
            next_cond.append(1)
        elif f["next_cond"][i]<0:
            next_cond.append(-1)
        else:
            next_cond.append(-1)
    f['next_cond'] = next_cond
    x_data['hl_pct'] = (x_data['high'] - x_data['low']) / x_data['low'] * 100.0
    x_data['ch_pct'] = (x_data['close'] - x_data['open']) / x_data['open'] * 100.0
    x_data['ma5_close_pct'] = (x_data['close'] - x_data['ma5']) / x_data['ma5'] * 100.0
    x_data['ma5_ma10_pct'] = (x_data['ma5'] / x_data['ma10']) * 100.0
    x_data = x_data[['vol', 'hl_pct', 'ch_pct', 'close', 'tor', 'vr', 'ma5_close_pct', 'ma5_ma10_pct']]
    y_data = f["next_cond"]
    # SVC  classification
    clf = svm.SVC()
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3)
    clf.fit(x_train, y_train)
    y_test_predicts = clf.predict(x_test)
    mse = sum((y_test - y_test_predicts) ** 2)
    mse /= len(y_test_predicts)
    print 'cond mse: ', mse
    print 'cond score: ', clf.score(x_test, y_test)
    joblib.dump(clf, 'models/cond_' + name + '_clf.pkl')
