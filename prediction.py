import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from processLibrary import *
import time
from matplotlib.backends.backend_agg import FigureCanvasAgg
import os
df = pd.read_csv('dataframe.csv')
df.drop(['Unnamed: 0'], inplace=True, axis=1)
df.drop(['Takas'], inplace=True, axis=1)
df.drop(['Plaka'], inplace=True, axis=1)

df.Fiyat = df.Fiyat.apply(removeDot)
df.Fiyat = df.Fiyat.apply(removeDigitEU)
df.Fiyat = df.Fiyat.apply(removeDigitTL)
df.Arac_Durum = df.Arac_Durum.apply(flattenDurum)
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
df["Arac_Durum_Train"], dictionary["Arac_Durum"] = Translator(df["Arac_Durum"])
df['KM'] = pd.to_numeric(df['KM'], downcast='integer')

X = df.iloc[:, 14:].values
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


def plotKM_train():
    filename = os.path.join(os.getcwd(), 'graphs', 'km_train.png')
    if os.path.exists(filename):
        if time.time()-os.path.getmtime(filename) < 300:
            return
    df1 = pd.DataFrame(X_train, dtype='float64')
    v1 = df1.iloc[:,6].values
    fig = plt.figure(figsize=(8,6))
    plt.rcParams.update({'font.size': 14})
    plt.scatter(v1,y_train, color='magenta')
    plt.title('Kilometre Değerine Göre Fiyat(Eğitim Verisi Tablosu)')
    plt.xlabel('KM')
    plt.ylabel('Fiyat')
    FigureCanvasAgg(fig).print_png(filename)
    return


def plotKM_test():
    filename = os.path.join(os.getcwd(), 'graphs', 'km_test.png')
    if os.path.exists(filename):
        if time.time()-os.path.getmtime(filename) < 300:
            return
    df1 = pd.DataFrame(X_test, dtype='float64')
    v1 = df1.iloc[:,6].values
    fig = plt.figure(figsize=(8,6))
    plt.rcParams.update({'font.size': 14})
    plt.scatter(v1,y_test, color='blue')
    plt.title('Kilometre Değerine Göre Fiyat(Test Verisi Tablosu)')
    plt.xlabel('KM')
    plt.ylabel('Fiyat')
    FigureCanvasAgg(fig).print_png(filename)
    return


def plotYakit():
    filename = os.path.join(os.getcwd(), 'graphs', 'yakit.png')
    if os.path.exists(filename):
        if time.time()-os.path.getmtime(filename) < 300:
            return
    graph = df[:]
    df.drop(df.loc[df.Motor_Hacmi.isnull()].index, inplace=True)
    graph.drop(graph.loc[graph.Yakıt == 'Elektrik'].index, inplace=True)
    graph.drop(graph.loc[graph.Yakıt == 'Hybrid'].index, inplace=True)
    fig = plt.figure(figsize=(8,6))
    plt.rcParams.update({'font.size': 16})
    plt.title("Yakıt Çeşitlenmesi")
    graph.groupby('Yakıt').Yakıt.count().plot(kind='pie')
    FigureCanvasAgg(fig).print_png(filename)
    return


def plotAvgKM():
    filename = os.path.join(os.getcwd(), 'graphs', 'ortalamaKM.png')
    if os.path.exists(filename):
        if time.time()-os.path.getmtime(filename) < 300:
            return
    fig = plt.figure(figsize=(8,6))
    plt.rcParams.update({'font.size': 16})
    df[:].groupby('Marka').KM.mean().plot(kind='bar')
    plt.title("Araba markalarına göre ortalama KM değerleri")
    plt.xlabel('Markalar')
    plt.ylabel('Ortalama Km\'ler')
    FigureCanvasAgg(fig).print_png(filename)
    return


def plotRenk():
    filename = os.path.join(os.getcwd(), 'graphs', 'renk.png')
    if os.path.exists(filename):
        if time.time()-os.path.getmtime(filename) < 300:
            return
    fig = plt.figure(figsize=(8,6))
    plt.rcParams.update({'font.size': 16})
    df[:].groupby('Renk').Renk.count().plot(kind='bar')
    plt.title("Arabaların Renk Dağılımı")
    plt.xlabel('Renk')
    plt.ylabel('Adet')
    FigureCanvasAgg(fig).print_png(filename)
    return


def plotMotor():
    filename = os.path.join(os.getcwd(), 'graphs', 'motor.png')
    if os.path.exists(filename):
        if time.time()-os.path.getmtime(filename) < 300:
            return
    df['Motor_Gucu'] = pd.to_numeric(df['Motor_Gucu'], downcast='integer')
    df['Motor_Hacmi'] = pd.to_numeric(df['Motor_Hacmi'], downcast='integer')
    df["Guc_Hacim"] = (df["Motor_Gucu"] / df["Motor_Hacmi"])
    fig = plt.figure(figsize=(32,24))
    plt.rcParams.update({'font.size': 16})
    df[:].groupby('Seri').Guc_Hacim.mean().plot(kind='bar')
    fig.suptitle("Araba Motor Performans Değer Tablosu",fontsize=32)
    plt.xlabel('Model')
    plt.ylabel('Araç Güç/Hacim')
    FigureCanvasAgg(fig).print_png(filename)
    return

def plotAvgPrice():
    filename = os.path.join(os.getcwd(), 'graphs', 'ortalamaFiyat.png')
    if os.path.exists(filename):
        if time.time()-os.path.getmtime(filename) < 300:
            return
    fig = plt.figure(figsize=(32,24))
    plt.rcParams.update({'font.size': 16})
    plt.xticks(rotation=30)
    df[:].groupby('Seri').Fiyat.mean().plot(kind='bar')
    fig.suptitle("Araba modellerinin ortalama fiyatları",fontsize=32)
    plt.xlabel('Seriler')
    plt.ylabel('Ortalama Fiyatlar')
    FigureCanvasAgg(fig).print_png(filename)
    return