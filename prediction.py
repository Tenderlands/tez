import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from processLibrary import *

import json

df = pd.read_csv('dataframe.csv')
df.drop(['Unnamed: 0'], inplace=True, axis=1)
df.drop(['Takas'], inplace=True, axis=1)
df.drop(['Plaka'], inplace=True, axis=1)

df.Fiyat = df.Fiyat.apply(removeDot)
df.Fiyat = df.Fiyat.apply(removeDigitEU)
df.Fiyat = df.Fiyat.apply(removeDigitTL)
df['Fiyat'] = pd.to_numeric(df['Fiyat'], downcast='integer')
df['Yıl'] = pd.to_numeric(df['Yıl'], downcast='integer')
df.KM = df.KM.apply(removeDot)
df.Motor_Gucu = df.Motor_Gucu.apply(removeDigitHP)
df.Motor_Hacmi = df.Motor_Hacmi.apply(removeDigitCC)

# Motor Gücü veya Hacmi Belirtilmemiş girdilerin çıkartılması
df.drop(df.loc[df.Motor_Hacmi.isnull()].index, inplace=True)
df.drop(df.loc[df.Motor_Gucu.isnull()].index, inplace=True)

df.drop(['Cekis'], inplace=True, axis=1)
df.drop(['Garanti'], inplace=True, axis=1)
df.drop(['Arac_Durum'], inplace=True, axis=1)

jsonifyDict(df)

dictionary = {}

df["Marka_Train"], dictionary["Marka"] = Translator(df["Marka"])
df["Seri_Train"], dictionary["Seri"] = Translator(df["Seri"])
df["Model_Train"], dictionary["Model"] = Translator(df["Model"])
df["Yıl_Train"] = df["Yıl"]
df["Yakıt_Train"], dictionary["Yakıt"] = Translator(df["Yakıt"])
df["Vites_Train"], dictionary["Vites"] = Translator(df["Vites"])
df["KM_Train"] = df["KM"]
df["Kasa_Tipi_Train"], dictionary["Kasa_Tipi"] = Translator(df["Kasa_Tipi"])
df["Motor_Gucu_Train"] = (df["Motor_Gucu"])
df["Motor_Hacmi_Train"] = (df["Motor_Hacmi"])
df["Renk_Train"], dictionary["Renk"] = Translator(df["Renk"])
df["Kimden_Train"], dictionary["Kimden"] = Translator(df["Kimden"])
df['KM'] = pd.to_numeric(df['KM'], downcast='integer')

X = df.iloc[:, 13:].values
y = df.iloc[:, 0].values

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 5, random_state=10)

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn import model_selection
from sklearn import metrics
from sklearn import linear_model
from sklearn.model_selection import cross_val_predict

regressor = RandomForestRegressor(n_estimators=10, random_state=10)
regressor.fit(X_train, y_train)
model = RandomForestRegressor(n_estimators=150, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 5, random_state=10)
model.fit(X_train, y_train)
