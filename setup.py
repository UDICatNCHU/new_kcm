from distutils.core import setup

setup(
    name = 'kcm',
    packages = ['kcm'],
    package_data={'kcm':['management/commands/*', 'utils/*']},
    version = '1.3',
    description = 'kcm class file',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/udicatnchu/kcm',
    download_url = 'https://github.com/udicatnchu/kcm/archive/v1.3.tar.gz',
    keywords = ['kcm'],
    classifiers = [],
    license='GPL3.0',
    install_requires=[
        'simplejson',
        'requests',
        'pymongo',
        'jieba',
        'ngram',
        'json-lines',
        'pympler',
        'opencc-python-reimplemented',
        'pythainlp',
        'nltk',
        'mecab-python3'
    ],
    dependency_links=[
        'git+git://github.com/attardi/wikiextractor.git@2a5e6aebc030c936c7afd0c349e6826c4d02b871',
    ],
    zip_safe=True
)
