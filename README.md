# Keyword Correlation Model (KCM 關鍵字相關性模型)[![Build Status](https://travis-ci.com/UDICatNCHU/KCM.svg?token=XRWFynWvo8Gsjgh9wqTN&branch=master)](https://travis-ci.com/UDICatNCHU/KCM)

KCM API are also available now：[API Online Version](https://github.com/UDICatNCHU/udic-nlp-API)  

Now three languages are available：
* Chinese
* English (Comming soon)
* Thai (Comming soon)
* Japanese (Comming soon)

## Getting Started

### Prerequisities

* If you want to use `the English version of KCM`， please download nltk data：`python3 -m nltk.downloader -d /usr/local/share/nltk_data all`
* To build KCM using other data sources, please take a look at [KCM Data Source Extractor](https://github.com/UDICatNCHU/KCM-Data-Source-Extractor)

## Installing

`pip install kcm`

### Config

1. add django app `kcm` in `settings.py`：

  - add this:

    ```
    INSTALLED_APPS=[
    ...
    ...
    ...
    'kcm',
    ]
    ```

2. add url patterns of kcm into `urls.py`：

  - add this:

    ```
    import kcm.urls
    urlpatterns += [
        url(r'^kcm/', include(kcm.urls))
    ]
    ```

3. fire `python manage.py runserver` and go `127.0.0.1:8000/` to check whether the config is all ok.

## Commands

Need to execute these commands before query the APIS.

1. Build KCM: `python3 manage.py buildKcm --lang=zh_TW`

## API

1. the result of querying KCM model with keyword `美國隊長`(Captain America)：`/kcm`_
  - keyword
  - num (default=10)
  - keyFlag (default=[])
  - valueFlag (defualt=[])
  - example：[http://140.120.13.244:10000/kem?keyword=美國隊長&num=100](http://140.120.13.244:10000/kem?keyword=美國隊長&num=100)

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

## Break down into end to end tests

`python3 manage.py test kcm`

## Deployment

`kcm` is a django-app, so depends on django project.

## Built With

* python3.5

## Contributors

* **張泰瑋** [david](https://github.com/david30907d)

## License

This package use `GPL3.0` License.

## Acknowledgments

* [WikiExtractor](https://github.com/attardi/wikiextractor)
* OpenCC-reimplement