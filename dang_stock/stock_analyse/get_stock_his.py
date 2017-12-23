# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

#cons = ts.get_apis()
#df = ts.bar('000568',conn=cons,freq='D',start_date='20171010',end_date='20171013',ma=[5,10,20],factors=['vr','tor'])

# df = ts.get_hist_data('000568',start='2017-04-13',end='2017-10-13')
from stock_analyse.models import Stock


def query_stock_hist(name,start,end):
    print 'begin to get data!'
    df = ts.get_h_data(name,start=start,end=end)
    # print df
    for ix,row in df.iterrows():
        stock_id= name
        open    = row['open']
        close   = row['close']
        high    = row['high']
        low     = row['low']
        vlume = row['volume']
        amount = row['amount']
        pub_date =ix
        print 'ix:',pub_date,'close:',close
        stock = Stock(stock_id='000568',open=open,close=close,high=high,amount=amount,volum=vlume,low=low)
        stock.save()

    # df.index = pd.to_datetime(df.index)
    # print df
    # store in mysql
    # engine = create_engine('mysql://root:dang@127.0.0.1/stockinfo?charset=utf8')
    # df.to_sql('stock_hist',engine)

    # use matplotlib display stock info
    # pydate_array = df.index.to_pydatetime()
    # date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pydate_array)
    # plt.plot(date_only_array, df['close'], label='close')
    # plt.legend()
    # plt.xlabel('date')
    # plt.ylabel('close')
    # plt.title('LZLJ_close_price')
    # plt.show()




