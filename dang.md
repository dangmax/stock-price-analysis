# Stock-price-analysis-service

**Overview:**

- Crawl stock info(price,quantity) with API
- Deal with stock price and store in database
- Visualize data with front-end technology
- Use machine learning to predict  stock price trend.

## Requirements
* Java Platform (JDK) 8
* Python 2.7x
* Rabbitmq
* Docker
* Docker Compose 
* Mysql-7.0
* Spark

## Main Use Cases
#### 1. Crawl Stock Information
```
use java or python scrapy to crawl some stock information(contains price,market value,volume) in a period of time
```

#### 2. Visualize Stock Information
```
the parse service may deal with the crawled stock info and make it simple to display in the page
```

#### 3. Predict  Stock Price
```
the predict service may give a future stock price through the machine learning model 
```
## Design  Diagram
![Syetem design diagram](/stock-service-diagram1.jpg "flow diagram")

## Detail  Design
#### 1. Stock Crawl Serivice
* use Django to make a python-web application
(1) the index page is a html template (user can input stock_id,start_time,end_time).
(2) background service method may crawel stock history info according to the input.
* use python tushare api to crawl stock price
(1) use tushare.get_h_data() method to get stock history price
* define the model(close,open,high,low,volume,amount)
(1) in django models,define 'stock' model fields(stock_id,open,close,high,low,volume,amount,pub_date)
(2) composite_keys: stock_id & pub_date
* db use mysql to store stock history info
(1) parse tushare api returned data and construct 'stock' model 
(2) use django model save() method to store in mysql 

#### 2. Data Parse Serivice
* use django model to query stock info in mysql db
(1) use 'stock' model filter(0 method to query stock history info from db 
* visualize stock history info with echarts. 
(1) echarts is a open sourced js lib with baidu
(2) include echarts js in html template  and send the stock data 
(3) echarts can display the stock data in a k-line
![Syetem design diagram](/kline.jpg "kline diagram")

#### 3. Stock Analysis Serivice
* train model
* predict the future price

