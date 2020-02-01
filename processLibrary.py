import numpy as np
import json
from sklearn.preprocessing import LabelEncoder


def removeDot(text):
    return text.replace(".", "").replace("\'", "").strip()


def removeDigitTL(text):
    return text.replace(" TL", "")


def removeDigitEU(text):
    if '€' in text:
        text = text.replace("€", "").strip()
        sayi = int(text)
        sayi = sayi * 6.5
        text = str(sayi)
    return text


def removeDigitHP(text):
    if ('hp' in text):
        return text.replace(" hp", "")
    elif ('HP' in text):
        ind = text.find(' ')
        if ind > -1:
            text = text[:ind]
        return text.strip()
    else:
        return np.nan


def removeDigitCC(text):
    if 'cc' in text:
        return text.replace(" cc", "")
    elif 'cm3' in text:
        ind = text.find(' ')
        if ind > -1:
            text = text[:ind]
        return text.strip()
    else:
        return np.nan


def Translator(data):
    values = np.array(data)
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    mapping = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))
    return integer_encoded, mapping


def SampleTranslator(Marka,Seri,Model,Yıl,Yakıt,Vites,KM,Kasa_Tipi,Motor_Gucu,Motor_Hacmi,Renk,Kimden,dictionary):
    return [[dictionary['Marka'][Marka],dictionary['Seri'][Seri],dictionary['Model'][Model],Yıl,dictionary['Yakıt'][Yakıt],dictionary['Vites'][Vites],KM,dictionary['Kasa_Tipi'][Kasa_Tipi],Motor_Gucu,Motor_Hacmi,dictionary['Renk'][Renk],dictionary['Kimden'][Kimden]]]


def jsonifyDict(df):
    Dict = {}
    Dict['Marka'] = {}
    Dict['Yakıt'] = df['Yakıt'].unique().tolist()
    Dict['Vites'] = df['Vites'].unique().tolist()
    Dict['Kasa_Tipi'] = df['Kasa_Tipi'].unique().tolist()
    Dict['Renk'] = df['Renk'].unique().tolist()
    Dict['Kimden'] = df['Kimden'].unique().tolist()
    for marka in df['Marka'].unique().tolist():
        Dict['Marka'][marka] = {}
        dfM = df.loc[df['Marka'] == marka]
        seriList = dfM['Seri'].unique().tolist()
        for seri in seriList:
            dfS = df.loc[df['Seri'] == seri]
            Dict['Marka'][marka][seri] = dfS['Model'].unique().tolist()
    jstr = json.dumps(Dict, indent=2)
    with open('series.json', 'w', encoding='utf-8') as f:
        f.write(jstr)


def getDict():
    return json.loads(open('series.json', 'r').read())


def processChoices(list):
    tList = [("", "Seçiniz")]
    for item in list:
        tList.append((item, item))
    return tList
