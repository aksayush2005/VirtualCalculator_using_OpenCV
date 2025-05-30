#importing essential libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

#import seaborn as sns
import sklearn
from tensorflow.keras.datasets import mnist
#importing the MNIST datset
(x_train, y_train),(x_test, y_test)=mnist.load_data()
#Reshaping the arrays and converting them into pandas dataframe
x_train=x_train.reshape(60000,784)
y_train=y_train.reshape(60000,1)
x_test=x_test.reshape(10000,784)
y_test=y_test.reshape(10000,1)
x_train_df=pd.DataFrame(x_train)
x_test_df=pd.DataFrame(x_test)
y_train_df=pd.DataFrame(y_train)
y_test_df=pd.DataFrame(y_test)
#Scaling using Standard Scaler
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
x_train=scaler.fit_transform(x_train_df)
x_test=scaler.transform(x_test_df)
#Applying KNN model using sklearn
from sklearn.neighbors import KNeighborsClassifier
model=KNeighborsClassifier()
params={"n_neighbors":[2,3,4,5]}
#Using GridSearchCV for hyperparamter tuning
from sklearn.model_selection import GridSearchCV
cv=GridSearchCV(model,params,cv=5)
cv.fit(x_train,y_train)
joblib.dump(cv, 'knn_mnist.pkl')
