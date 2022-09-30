# -*- coding: utf-8 -*-
"""Predictive_Analytics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CE1p0x4hmTGTS5tfkZrJfTdDTtvl3kXP

# Data Loading

Mengimport kaggle.json sebagai authorization untuk mendownload dataset menggunakan kaggle command line
"""

from google.colab import files
files.upload()

!rm -r ~/.kaggle
!mkdir ~/.kaggle
!mv ./kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets list

"""Download dataset menggunakan perintah ```!kaggle datasets download user_dataset/dataset -p /direktori_tujuan --unzip ```

link dataset : [kaggle](https://www.kaggle.com/datasets/rajyellow46/wine-quality)
"""

!kaggle datasets download rajyellow46/wine-quality -p /content/sample_data --unzip

"""import segala library yang dibutuhkan"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns
from sklearn.preprocessing import  OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import GridSearchCV

"""load dataset menggunakan pandas"""

DATASET_PATH = "/content/sample_data/winequalityN.csv"
wine = pd.read_csv(DATASET_PATH)
display(wine)

"""Output kode di atas memberikan informasi sebagai berikut:

* Ada 6497 baris dataset.
* Terdapat 13 kolom : type, fixed acidity, volatile acidity,	citric acid,	residual sugar,	chlorides,	free sulfur dioxide,	total sulfur dioxide,	density
pH,	sulphates,	alcohol,	quality

# Exploratory Data Analysis

## Deskripsi Variabel
"""

#Menampilkan Informasi
wine.info()

"""Dari output terlihat bahwa:

* Terdapat 12 kolom dengan tipe numerik, yaitu: fixed acidity, volatile acidity,	citric acid,	residual sugar,	chlorides,	free sulfur dioxide,	total sulfur dioxide,	density, pH,	sulphates,	alcohol,	quality.

* Terdapat 1 buah kolum dengan tipe object : type

---
* Count  adalah jumlah sampel pada data.
* Mean adalah nilai rata-rata.
* Std adalah standar deviasi.
* Min yaitu nilai minimum setiap kolom. 
* 25% adalah kuartil pertama. Kuartil adalah nilai yang menandai batas interval * dalam empat bagian sebaran yang sama. 
* 50% adalah kuartil kedua, atau biasa juga disebut median (nilai tengah).
* 75% adalah kuartil ketiga.
* Max adalah nilai maksimum.
"""

wine.describe()

"""## Menangani Missing Value

Mengecek jumlah data yang memiliki nilai null
"""

wine.isnull().sum()

"""Dari output diatas beberapa kolum memiliki nilai null, data yang memiliki nilai null sebaiknya di hapus karena merupakan data yang tidak valid dan dapat mengganggu saat proses training karna hanya menerima bilangan numerik."""

wine = wine.dropna()
wine.shape

"""Mengecek setelah penghapusan data yang memiliki null / missing value"""

wine.isnull().sum()

"""## Menangani Outliers

Didalam dataset terkadang terdapat data yang berada di luar lingkungan pengamatan yang kemunculannya sangat jarang dan berbeda dari data hasil pengamatan lainnya.

Melihat outlier pada tiap data numerik.
"""

sns.boxplot(x=wine['fixed acidity'])

sns.boxplot(x=wine['volatile acidity'])

sns.boxplot(x=wine['citric acid'])

sns.boxplot(x=wine['residual sugar'])

sns.boxplot(x=wine['chlorides'])

sns.boxplot(x=wine['free sulfur dioxide'])

sns.boxplot(x=wine['total sulfur dioxide'])

sns.boxplot(x=wine['density'])

sns.boxplot(x=wine['pH'])

sns.boxplot(x=wine['sulphates'])

sns.boxplot(x=wine['alcohol'])

sns.boxplot(x=wine['quality'])

"""Dari output diatas setiap data memiliki outlier nya masing-masing, data yang berada diluar pengamatan akan dihapus menggunakan metode IQR untuk mengidentifikasi outlier yang berada di luar Q1 dan Q3. Nilai apa pun yang berada di luar batas ini dianggap sebagai outlier. 

*note:* 
``` 
Q1 = Minimum (Sebelah kiri)
Q3 = Maximum (Sebelah kanan)
```

Persamaan mengidentifikasi :
```
Minimum = Q1 - 1.5 * IQR

Maximum = Q3 + 1.5 * IQR
```
"""

Q1 = wine.quantile(0.25)
Q3 = wine.quantile(0.75)
IQR=Q3-Q1
wine=wine[~((wine<(Q1-1.5*IQR))|(wine>(Q3+1.5*IQR))).any(axis=1)]
 
# Cek ukuran dataset setelah kita drop outliers
wine.shape

"""Setelah penghapusan outlier jumlah data menjadi ***4815***

## Univariate Analysis

proses analisis data dengan teknik Univariate EDA.

Membagi dua fitur yaitu numerikal dan categorical
"""

numerical_features = wine.columns[1:].values
categorical_features = ['type']

print(numerical_features)
print(categorical_features)

"""### Categorical Feature"""

feature = categorical_features[0]
count = wine[feature].value_counts()
percent = 100*wine[feature].value_counts(normalize=True)
df = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df)
count.plot(kind='bar', title=feature);

"""Dari output diatas terdapat dua kategori pada fitur ***type***, jumlah paling banyak berada di kategori white dengan persentase 86%

### Numerical feature
"""

wine.hist(bins=50, figsize=(20,15))
plt.show()

"""Dari pengamatan histogram diatas :

* Wine dengan quality 6 memiliki data yang cukup banyak sekitar 2500 jumlah data.

## Multivariate Analysis

Teknik multivariate analysis berfungsi untuk menunjukan hubungan anatara dua atau lebih variable pada data.

### Categorical Features
"""

cat_features = wine.select_dtypes(include='object').columns.to_list()
 
for col in cat_features:
  sns.catplot(x=col, y="quality", kind="bar", dodge=False, height = 4, aspect = 3,  data=wine, palette="Set3")
  plt.title("Rata-rata 'quality' Relatif terhadap - {}".format(col))

"""Dengan mengamati rata-rata quality relatif terhadap fitur kategori di atas, memperoleh insight :

* Pada fitur type rata-rata quality cenderung mirip, rentang berada di 5-6.

### Numerical Features
"""

# Mengamati hubungan antar fitur numerik dengan fungsi pairplot()
sns.pairplot(wine, diag_kind = 'kde')

plt.figure(figsize=(10, 8))
correlation_matrix = wine.corr().round(2)
 
sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

"""Dari pengamatan output diatas :
* Alcholol memiliki korelasi terhadap kualitas sebuah wine

* Selain itu, sulfur dioksida bebas dan sulfur dioksida total memiliki korelasi positif juga.

# Data Preparation

## Encoding

encoding fitur kategori menggunakan one-hot-encoding. Proses encoding dilakukan menggunakan get_dummies.
"""

wine = pd.concat([wine, pd.get_dummies(wine['type'], prefix='type')],axis=1)
wine.drop(['type'], axis=1, inplace=True)
wine.head()

"""## Reduksi dimensi

mereduksi dimensi menggunakan PCA (Principal Component Analysis)
"""

numerical_features=numerical_features[:len(numerical_features)-1].tolist()

wine[numerical_features]

from sklearn.decomposition import PCA
 
pca = PCA(n_components=3, random_state=128)
pca.fit(wine[numerical_features])
princ_comp = pca.transform(wine[numerical_features])
pca.explained_variance_ratio_.round(3)

from sklearn.decomposition import PCA
pca = PCA(n_components=1, random_state=123)
pca.fit(wine[numerical_features])
wine['dimension'] = pca.transform(wine.loc[:, tuple(numerical_features)]).flatten()
wine.drop(numerical_features, axis=1, inplace=True)

"""## Membagi dataset train dan test

Membagi dataset menjadi train dan test menggunakan train_test_split.

80% train

20% test
"""

from sklearn.model_selection import train_test_split
 
X = wine.drop(["quality"],axis =1)
y = wine["quality"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 128)

print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in test dataset: {len(X_test)}')

"""## Standarisasi

Melakukan standarisasi agar data memiliki skala yang relatif sama.

Standarisasi disini menggunakan `StandardScaler`
"""

numerical_features = X_train.columns[2:].values
scaler = StandardScaler()
scaler.fit(X_train[numerical_features])
X_train[numerical_features] = scaler.transform(X_train.loc[:, numerical_features])
X_train[numerical_features].head()

X_train[numerical_features].describe().round(4)

"""# Model Development

Pengembangan model menggunakan beberapa algoritma :
* KNN
* RandomForest
* Boosting
* Ridge Regression
* SVR
* Decision Tree

Dari beberapa model diatas saya menambahkan hyperparameter menggunakan *GridSearch*

## KNN
"""

models = pd.DataFrame(index=['train_mse', 'test_mse'], 
                      columns=['KNN', 'RandomForest', 'Boosting',"Ridge","SVR","Decision Tree"])

leaf_size = list(range(1,50))
n_neighbors = list(range(1,30))
p=[1,2]

hyperparameters = dict(leaf_size=leaf_size, n_neighbors=n_neighbors, p=p)

knn = KNeighborsRegressor()
gsc = GridSearchCV(knn, hyperparameters, cv=10)

knn_best_model = gsc.fit(X_train,y_train)
models.loc['train_mse','KNN'] = mean_squared_error(y_pred = knn_best_model.predict(X_train), y_true=y_train)

"""## Random Forest"""

params = {
    'bootstrap': [True],
    'max_depth': [80, 90, 100, 110],
    'max_features': [2, 3],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [50,100, 200, 300, 1000]
}

RF = RandomForestRegressor()

gsc_rf = GridSearchCV(estimator = RF, param_grid = params, 
                          cv = 3, n_jobs = -1, verbose = 2)

rf_best_model = gsc_rf.fit(X_train,y_train)
models.loc['train_mse','RandomForest'] = mean_squared_error(y_pred=rf_best_model.predict(X_train), y_true=y_train)

"""## Adaboost"""

params = {
 'n_estimators': [50, 100],
 'learning_rate' : [0.01, 0.05, 0.1, 0.5],
 'loss' : ['linear', 'square', 'exponential']
}

boosting = AdaBoostRegressor()         
gsc_adaboost = GridSearchCV(estimator = boosting, param_grid = params, 
                          cv = 3, n_jobs = -1, verbose = 2)                    
boosting_best_model = gsc_adaboost.fit(X_train, y_train)
models.loc['train_mse','Boosting'] = mean_squared_error(y_pred=boosting_best_model.predict(X_train), y_true=y_train)

"""## Ridge Regression"""

params = {'alpha':[0.001, 0.01, 0.1, 1, 10, 100, 1000]}

lg = Ridge()
gsc_lg = GridSearchCV(estimator = lg, param_grid = params, 
                          cv = 3, n_jobs = -1, verbose = 2)                    
lg_best_model = gsc_lg.fit(X_train, y_train)
models.loc['train_mse','Ridge'] = mean_squared_error(y_pred=lg_best_model.predict(X_train), y_true=y_train)

"""## SVR"""

params = {'kernel': ('linear', 'rbf','poly'), 'C':[1.5, 10],'gamma': [1e-7, 1e-4],'epsilon':[0.1,0.2,0.5,0.3]}

svr = SVR()
gsc_svr = GridSearchCV(estimator = svr, param_grid = params, 
                          cv = 3, n_jobs = -1, verbose = 2)   
svr_best_model = gsc_svr.fit(X_train, y_train)
models.loc['train_mse','SVR'] = mean_squared_error(y_pred=svr_best_model.predict(X_train), y_true=y_train)

"""## Decision Tree"""

params = {"min_samples_split": [10, 20, 40],
          "max_depth": [2, 6, 8],
          "min_samples_leaf": [20, 40, 100],
          "max_leaf_nodes": [5, 20, 100],
          }

tree = DecisionTreeRegressor()
gsc_tree = GridSearchCV(estimator = tree, param_grid = params, 
                          cv = 3, n_jobs = -1, verbose = 2)   
tree_best_model = gsc_tree.fit(X_train, y_train)
models.loc['train_mse','Decision Tree'] = mean_squared_error(y_pred=tree_best_model.predict(X_train), y_true=y_train)

"""# Evaluasi

Scaling pada data test
"""

X_test.loc[:, numerical_features] = scaler.transform(X_test[numerical_features])

"""Evaluasi model dengan metrik MSE (Mean Squared Error)"""

mse = pd.DataFrame(columns=['train', 'test'], index=['KNN', 'RandomForest', 'Boosting',"Ridge","SVR","Decision Tree"])
 
model_dict = {'KNN': knn_best_model, 
              'RandomForest': rf_best_model, 
              'Boosting': boosting_best_model,
              "Ridge":lg_best_model,
              "SVR":svr_best_model,
              "Decision Tree":tree_best_model}
 
for name, model in model_dict.items():
    mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))
    mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))
 
mse

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

"""## Pengujian model"""

prediksi = X_test.iloc[:1].copy()
pred_dict = {'y_true':y_test[:1]}
for name, model in model_dict.items():
    pred_dict['prediksi_'+name] = model.predict(prediksi).round(1)
 
pd.DataFrame(pred_dict)

"""Terlihat Decision tree memberikan hasil yang sesuai."""