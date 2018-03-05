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
			subprocess.call(['mkdir', 'build'])
			subprocess.call(['wget', 'https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2'])

			if not os.path.isdir('wikijson'):
				subprocess.call(['WikiExtractor.py', 'zhwiki-latest-pages-articles.xml.bz2', '-o', 'wikijson', '--json'])

		getWikiData()
		self.stdout.write(self.style.SUCCESS('finish the extraction of Wikipedia'))
		k = KCM(input_dir='wikijson', lang=options['lang'], uri=uri)
		k.build()
		self.stdout.write(self.style.SUCCESS('finish build material of KCM'))
		k.merge()
		self.stdout.write(self.style.SUCCESS('build KCM success!!!'))