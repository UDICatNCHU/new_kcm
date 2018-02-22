# Keyword Correlation Model (KCM 關鍵字相關性模型)[![Build Status](https://travis-ci.com/UDICatNCHU/KCM.svg?token=XRWFynWvo8Gsjgh9wqTN&branch=master)](https://travis-ci.com/UDICatNCHU/KCM)

KCM API are also available now：[API Online Version](https://github.com/UDICatNCHU/udic-nlp-API)  

不知道要寫啥  
Now three languages are available：
* Chinese
* English

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

1. OS：Ubuntu / OSX would be nice
2. environment：need python3 `sudo apt-get update; sudo apt-get install; python3 python3-dev`
3. (optional) 簡繁轉換：`sudo apt-get install -y opencc`
4. (optional) 英文版Wiki，請先下載nltk：`python3 -m nltk.downloader -d /usr/local/share/nltk_data all`
4. (optional) 用各論壇資料建立KCM模型：請先參照這篇產出輸入檔[KCM Data Source Extractor](https://github.com/UDICatNCHU/KCM-Data-Source-Extractor)

### Installing

* Install By Docker：
  1. You can only run this command in directory which has Dockerfile：`sudo docker build -t kcm .`
* Install manually：
  1. 使用虛擬環境 Use virtualenv is recommended：
    1. `virtualenv venv`
    2. 啟動方法 How to activate virtualenv
      1. for Linux：`. venv/bin/activate`
      2. for Windows：`venv\Scripts\activate`
  2. 安裝 Install：`pip install -e git://github.com/UDICatNCHU/KCM.git@master#egg=KCM`

## Running & Testing

## Run

* 整體使用方法 Usage：

  * KCM物件的參數：
    * lang：cht `中文`、英文 `eng`
    * io_dir：讀取建立model用的input檔的路徑
    * thread_count：輸入整數，為啟動的執行緒數量
    * uri：Mongo連接網址，`mongodb://資料庫IP`
  * Instance Method：
    * main：建立模型的函式
    * setLang：選擇語系的函式，build會根據設定的語言到相對應的資料夾讀取input檔
    * removeDB：清空MongoDB
    * get：到MongoDB查詢結果
  * 執行方法（二選一）：
    1. command line執行：`python3 src/kcm/KCM/__main__.py(或是你放kcm/__main__.py的路徑) -p 你放要建立模型輸入檔的地方`
    2.  
      ```
      from KCM.__main__ import KCM
      k = KCM('cht', '含有輸入檔的資料夾路徑')
      k.removeDB()
      k.main()

      print(k.get('美國隊長', 10))
      ```

### Results

the result of querying KCM model with keyword "Captain America"：

  ```
  [
    ["電影",93],
    ["復仇者",78],
    ["戰士",55],
    ["英雄",55],
    ["鋼鐵",52],
    ["內戰",50],
    ["復仇者聯盟",44],
    ["漫畫",42],
    ["酷寒",39],
    ["巴基",36]
  ]
  ```



### Break down into end to end tests


1. 執行全部的測試 run whole test：`python3 run_tests.py`

### And coding style tests

目前沒有coding style tests...


## Deployment

目前只是一般的python程式，`pip install` 即可

## Built With

* python3.5

## Versioning

For the versions available, see the [tags on this repository](https://github.com/david30907d/KCM/releases).

## Contributors

* **范耀中** [教授](http://web.nchu.edu.tw/~yfan/)
* **黃思穎**
* **陳聖軒**
* **Yen-Ju Lee**
* **張泰瑋** [david](https://github.com/david30907d)

## License

## Acknowledgments

* [WikiExtractor](https://github.com/attardi/wikiextractor)
* 感謝fxsjy的jieba斷詞系統 Thanks python library jieba from fxsjy
* 感謝Google工程師釋出的word2vec Thanks word2vec from Google
