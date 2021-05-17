# DSAI_HW3
## 摘要
本專案目的為使用過去發電量以及用電量資料建構一長短期記憶（Long Short-Term Memory，LSTM）模型，用過去七天的資料預測未來一天的用電情形，並將此模型用於

## 訓練資料
使用課程提供之訓練數據，先將資料進行前處理後，以便進行後續訓練。
### 用電量資料
* 資料來源：由課程助教提供
* 資料內容：資料內含每小時之產電與用電資料，總共291404筆，並將資料存放於[**training_data資料夾**](https://github.com/vf19961226/DSAI_HW3/tree/main/training_data)中，其詳細內容如下表所示。

|time|generation|consumption
|:---:|:---:|:---:
|2018-01-01 1:00:00|0|1.52
|2018-01-01 2:00:00|0.01|1.09
|2018-01-01 3:00:00|0|0.95
|2018-01-01 4:00:00|0|0.75
|2018-01-01 5:00:00|0|0.74

* 其整體資料分布如下圖所示。    
![surplus power](https://github.com/vf19961226/DSAI_HW3/blob/main/figure/Surplus_Power.png "surplus power") 
### 資料前處理
* 前處理方法：計算淨用電量與RobustScaler
* 概述：將產電資料與用電資料相減取得每日淨用電量，在使用RobustScaler進行資料處理。RobustScaler是使用中位數和四分位數，確保每個特徵的統計屬性都位於同一範圍。它會忽略與其他點有很大不同的數據點，即忽略異常值outlier。其公式如下圖所示。其中X'為新數據、X為舊數據、X.median為數據之中位數、IQR為數據之四分衛距。
* 公式：X' = (X - X.median) / IQR
* 處理後結果如下圖所示。    
![RS surplus power](https://github.com/vf19961226/DSAI_HW3/blob/main/figure/RS_Surplus_Power.png "RS surplus power")  

## 模型訓練
1. 將上述預處理之成果輸出成CSV檔以利後續訓練。
* 為csv檔加入表頭["Number", "RS"]。
* 刪除"Number"列並選取最後n列作為未來預測用途。
```py
train_data = pd.read_csv("/content/gdrive/MyDrive/DSAI_HM3/RS_sur.csv")
train_data.columns=["Number", "RS"]
train_data = train_data.drop(columns=["Number"])
train_data = train_data.iloc[-24:] #讀最後24條
train_data = train_data.reset_index(drop=True)#刪除索引
train_data.columns = [''] * len(train_data.columns)
```
2. 分割資料集
* 最後輸出 x_train - 三維數值，其直各為(N比數值,天數,數值）＝(262221, 24, 1)
* 最後輸出 y_train - 二維數值，其直各為(N比數值,數值）＝ (262221, 24)
```py
  X_train, Y_train = [], []
    for i in range(train.shape[0]-futureDay-pastDay):
      X_train.append(np.array(train.iloc[i:i+pastDay])) #分割訓練集      
      Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["RS"])) #分割輸出label
```
3. 建構模型
* 輸入層：(24,1)
* 輸出層：(24,1)


## 交易邏輯
使用上述模型訓練出之模型進行淨用電量預測，當預測出淨用電量為負的，則需要購買電以補足缺口，而購買價格需比市場電價電價來得低，目前市場電價1度約為2.5元新台幣。當預測出淨用電量為正，則代表有多餘的電力可以出售，而出售價格訂定為1度1新台幣。期望達成淨用電量為0的目標。

## 資料輸出
最終決定好買賣狀態後進行資料輸出，輸出為[**output.csv**](https://github.com/vf19961226/DSAI_HW3/blob/main/output.csv)，一次會輸出未來1天內每小時交易狀態，其格式如下表所示。    

|time|action|target_price|target_volume
|:---:|:---:|:---:|:---:
|2021-05-17 1:00:00|buy|2.5|3
|2021-05-17 2:00:00|sell|3|5
