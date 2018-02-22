from django.core.management.base import BaseCommand, CommandError
import os, json_lines, subprocess
from kcm import KCM
# from opencc import OpenCC

class Command(BaseCommand):
    help = 'use this to build KCM !'
    def __init__(self, *args, **kwargs):
        # super(BaseCommand, self).__init__(*args, **kwargs)
        self.baseDir = os.path.dirname(os.path.abspath(__file__))
        
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--lang', type=str)
    
    def handle(self, *args, **options):
        def getWikiData():
            subprocess.call(['wget', 'https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2'])

            if not os.path.isdir('wikijson'):
                subprocess.call([os.join(self.baseDir, 'WikiExtractor.py'), 'zhwiki-latest-pages-articles.xml.bz2', '-o', 'wikijson', '--json'])

        getWikiData()
        k = KCM('wikijson', options['lang'])
        k.build()
        self.stdout.write(self.style.SUCCESS('build KCM success!!!'))