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
![Syetem design diagram](/stock-service-diagram.jpg "flow diagram")

## Detail  Design
#### 1. Stock Crawl Serivice
* use python scrapy crawl stock price
* define the table field(price,quantity,market value,pe,date,pb)
* db use mysql

#### 2. Data Parse Serivice
* java project query stock info in mysql db
* visualize stock info with front end technology
* make stack price info item as a message and put it into rabbitmq

#### 3. Data Parse Serivice
* java project query stock info in mysql db
* visualize stock info with front end technology
* make stack price info item as a message and put it into rabbitmq

#### 4. Stock Analysis Serivice
* train model with test data 
* consume message and predict the future price


