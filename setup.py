from distutils.core import setup

setup(
    name = 'kcm',
    packages = ['kcm'],
    package_data={'kcm':['management/commands/*', 'build/*']},
    version = '0.1',
    description = 'kcm class file',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/udicatnchu/kcm',
    download_url = 'https://github.com/udicatnchu/kcm/archive/v0.1.tar.gz',
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
    ],
    zip_safe=True
)
