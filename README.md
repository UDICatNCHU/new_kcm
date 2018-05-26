# Keyword Correlation Model (KCM 關鍵字相關性模型)[![Build Status](https://travis-ci.com/UDICatNCHU/KCM.svg?token=XRWFynWvo8Gsjgh9wqTN&branch=master)](https://travis-ci.com/UDICatNCHU/KCM)

KCM API are also available now：[API Online Version](https://github.com/UDICatNCHU/udic-nlp-API)  

## Getting Started

### Prerequisities

* If you want to use `the English version of KCM`， please download nltk data：`python3 -m nltk.downloader -d /usr/local/share/nltk_data all`

## Install

* (Recommended): Use [docker-compose](https://github.com/udicatnchu/udic-nlp-api) to install

## Manually Install

If you want to integrate `kcm` into your own django project, use manually install.

* `pip install kcm`

### Config

1. add django app `kcm` in `settings.py`：

    - add this:

      ```python
      INSTALLED_APPS=[
      ...
      ...
      ...
      'kcm',
      ]
      ```

2. add url patterns of kcm into `urls.py`：

    - add this:

      ```python
      import kcm.urls
      urlpatterns += [
          url(r'^kcm/', include(kcm.urls))
      ]
      ```

3. use `python3 manage.py buildKcm --lang <lang, e.g., zh or en or th> ` to build model of kcm.
4. fire `python manage.py runserver` and go `127.0.0.1:8000/` to check whether the config is all ok.

## API

1. Get correlated keywords：_`/kcm`_
    - keyword
    - num (default=10)
    - keyFlag (default=[])
    - valueFlag (defualt=[])
    - example1：[http://udiclab.cs.nchu.edu.tw/kcm?keyword=周杰倫&lang=zh](http://udiclab.cs.nchu.edu.tw/kcm?keyword=周杰倫&lang=zh)

        ```json
        {
          "PartOfSpeech": ["nr"],
          "similarity": 1.0,
          "key": "周杰倫",
          "value": [
            ["巡迴演唱", "l", 861],
            ["世界", "n", 705],
            ["周杰倫", "nr", 424],
            ["專輯", "n", 286],
            ["歌曲", "n", 241],
            ["時間", "n", 234]
          ]
        }
        ```

    - example2 (with specific keyFlag and valueFlag)：[http://udiclab.cs.nchu.edu.tw/kcm/?keyword=周杰倫&valueFlag=n+nr&keyFlag=nr&lang=zh](http://udiclab.cs.nchu.edu.tw/kcm/?keyword=周杰倫&valueFlag=n+nr&keyFlag=nr&lang=zh)

        ```json
        {
          "PartOfSpeech": ["nr"],
          "similarity": 1.0,
          "key": "周杰倫",
          "value": [
            ["世界", "n", 705],
            ["周杰倫", "nr", 424],
            ["專輯", "n", 286],
            ["歌曲", "n", 241],
            ["時間", "n", 234],
            ["深圳站", "n", 146],
            ["演唱會", "n", 139],
            ["成都站", "n", 132],
            ["電影", "n", 119],
            ["蔡依林", "nr", 111]
          ]
        }
        ```
2. Get similar keywords, not semantic similar but literally similar：_`/search`_
    - keyword
    - lang
    - threshold (default=0)
    - num (default=10)
    - example1：[http://udiclab.cs.nchu.edu.tw/kcm/search?keyword=台灣高速鐵路&lang=zh](http://udiclab.cs.nchu.edu.tw/kcm/search?keyword=台灣高速鐵路&lang=zh)

        ```json
        [
          [
            "臺灣高速鐵路",
            0.45454545454545453
          ],
          [
            "高速鐵路",
            0.4
          ],
          [
            "京廣高速鐵路",
            0.3333333333333333
          ]
          ...
          ...
          ...
        ]
        ```
    - example2：[http://udiclab.cs.nchu.edu.tw/kcm/search?keyword=台灣高速鐵路&lang=zh&threshold=0.2&num=15](http://udiclab.cs.nchu.edu.tw/kcm/search?keyword=台灣高速鐵路&lang=zh&threshold=0.2&num=15)

        ```json
        [
          [
            "臺灣高速鐵路",
            0.45454545454545453
          ],
          [
            "高速鐵路",
            0.4
          ],
          [
            "京廣高速鐵路",
            0.3333333333333333
          ]
          ...
          ...
          ...
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