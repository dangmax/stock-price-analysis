from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.linear_model import  LinearRegression
from sklearn import  preprocessing

from stock_analyse.models import Stock

# iris = datasets.load_iris()
# iris_x = iris.data
# iris_y = iris.target

# print iris_x.shape
# print iris_x.ndim
# print iris_y.shape
# print iris_y.ndim
# print '10 line',iris_y
# print '2 line',iris_x[:2,:]
# print '1 line',iris_x[:1,:]
# iris_x = preprocessing.scale(iris_x)
# iris_y = preprocessing.scale(iris_y)
# print 'new 10 line',iris_y
# x_train,x_test,y_train,y_test = train_test_split(iris_x,iris_y,random_state=4)
# # print 'train data:',y_train.shape
# # print 'test data:',y_test.shape
#
# knn = KNeighborsClassifier()
# # knn = LinearRegression()
# knn.fit(x_train,y_train)
# print 'score: ',knn.score(x_test,y_test)
# print 'coef:',knn.coef_
# print 'intercept:',knn.intercept_

# print knn.predict(x_test)
# print y_test


result = Stock.objects.filter(stock_id='000568')
print result.count()