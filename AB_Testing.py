import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_excel("Datasets\\ab_testing.xlsx")

df.head(20)


#Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı
#değişkenlere atayınız.

control_group = pd.read_excel("Datasets\\ab_testing.xlsx", sheet_name="Control Group")

test_group = pd.read_excel("Datasets\\ab_testing.xlsx", sheet_name="Test Group")

#Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

# 1.Yol

def check_df(dataframe, head=5):
    print("#############################  Shape  #############################")
    print(dataframe.shape)
    print("#############################  Types  #############################")
    print(dataframe.dtypes)
    print("#############################  Head  #############################")
    print(dataframe.head(head))
    print("#############################  Tail  #############################")
    print(dataframe.tail(head))
    print("#############################  NA  #############################")
    print(dataframe.isnull().sum())
    print("#############################  Quantiles  #############################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(control_group)
check_df(test_group)


#Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

print(pd.concat([control_group, test_group], join="inner", ignore_index=True))

#Görev 2: A/B Testinin Hipotezinin Tanımlanması

#Adım 1: Hipotezi tanımlayınız.

H0 : M1 = M2 #(Kontrol ve test grubu ortalamaları arasında istatistiksel olarak anlamlı bir fark #yoktur)
H1 : M1!= M2 #(Kontrol ve test grubu ortalamaları arasında istatistiksel olarak anlamlı bir fark #vardır)

#Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.

test_group["Purchase"].mean() #582.10

control_group["Purchase"].mean() #550.89

#Görev 3: Hipotez Testinin Gerçekleştirilmesi

# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği

#1:Normallik Varsayımı

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(test_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#pvalue  =0.15 > 0.05 Ho reddilemez. Normallik varsayımı test grubu için sağlanmaktadır.

test_stat, pvalue = shapiro(control_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#pvalue  =0.15 > 0.05 Ho reddilemez. Normallik varsayımı control grubu için de sağlanmaktadır.

#2:Varyans Homojenliği

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(test_group["Purchase"],
                           control_group["Purchase"].dropna())

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#pvalue = 0.10 > 0.05 Ho reddilemez. Varyanslar homojendir.


#Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)

test_stat, pvalue = ttest_ind(test_group["Purchase"],
                              control_group["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#pvalue = 0.34 > 0.05 Ho hipotezi reddilemez. Yani; kontrol ve test grubu satın alma ortalamaları arasında istatistiki
#olarak anlamlı bir fark yoktur.

#Görev 4: Sonuçların Analizi
#Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

#Yorum: Kontrol ve test grubunun normallik varsayımına uyup uymadığını  test etmek için Shapiro testi kullanılmıştır.
#Her iki gruptada normallik varsayımı sağlandığı için bir sonraki adımda varyans homojenliği testine geçilmiştir.
#Varyans homojenliği için Levene testi kullanılmıştır. Test sonucunda her iki gruptada varyans homojenlikleri arasında benzerlik olduğu görülmüştür.
#İki varsayımda sağlandığı için, iki grup arasındaki istatistiksel anlamları ortaya çıkarabilmek için Bağımsız İki Örneklem T testi kullanılmıştır.
#Bağımsız İki Örneklem T testi sonucunda hipotez reddilememiştir. Sonuç olarak; Kontrol ve test gruplarının ortalamaları arasında fark olduğu görülse bile
#bunun istatistiksel olarak anlamlı olmadığı yapılan analizler sonucu tespit edilmiştir.

#Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

#Web sitesine eklenen yeni sistemi tekrardan incelemek için daha fazla örneklem ile yeni bir test yapılabilir. Test ettiğimiz yeni sistem kazanç ortalamalarında anlamlı bir
#farklılık yaratmamıştır. Şu an için hayata geçirilmesine gerek yoktur.
