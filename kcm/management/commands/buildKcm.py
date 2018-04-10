from django.core.management.base import BaseCommand, CommandError
import os, subprocess
from kcm import KCM
from udic_nlp_API.settings_database import uri
from gensim.corpora import WikiCorpus

class Command(BaseCommand):
	help = 'use this to build KCM !'
		
	def add_arguments(self, parser):
		# Positional arguments
		parser.add_argument('--lang', type=str)
	
	def handle(self, *args, **options):
		def getWikiData():
			subprocess.call(['mkdir', 'Wikipedia'])
			subprocess.call(['mkdir', 'wikijson'])
			lang = options['lang']
			url = 'https://dumps.wikimedia.org/{}wiki/latest/{}wiki-latest-pages-articles.xml.bz2'.format(lang, lang)
			if not os.path.exists('{}wiki-latest-pages-articles.xml.bz2'.format(lang)):
				subprocess.call(['wget', url,'-P', 'Wikipedia'])
				subprocess.call(['WikiExtractor.py', 'zhwiki-latest-pages-articles.xml.bz2', '-o', 'wikijson', '--json'])

		getWikiData()
		self.stdout.write(self.style.SUCCESS('finish the extraction of Wikipedia'))
		k = KCM(input_dir='wikijson', lang=options['lang'], uri=uri)
		k.build()
		self.stdout.write(self.style.SUCCESS('finish build material of KCM'))
		k.merge()
		self.stdout.write(self.style.SUCCESS('build KCM success!!!'))