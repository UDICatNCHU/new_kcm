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
		wiki_dir_name = 'Wikipedia'
		wiki_json_dir = 'wikijson'
		
		def getWikiData():
			subprocess.call(['mkdir', wiki_dir_name])
			subprocess.call(['mkdir', wiki_json_dir])
			lang = options['lang']
			url = 'https://dumps.wikimedia.org/{}wiki/latest/{}wiki-latest-pages-articles.xml.bz2'.format(lang, lang)
			if not os.path.exists(os.path.join(wiki_dir_name, '{}wiki-latest-pages-articles.xml.bz2'.format(lang))):
				subprocess.call(['wget', url,'-P', wiki_dir_name])
				subprocess.call(['WikiExtractor.py', os.path.join(wiki_dir_name, '{}wiki-latest-pages-articles.xml.bz2'.format(lang)), '-o', wiki_json_dir, '--json'])

		getWikiData()
		self.stdout.write(self.style.SUCCESS('finish the extraction of Wikipedia'))
		k = KCM(input_dir=wiki_json_dir, lang=options['lang'], uri=uri)
		k.build()
		self.stdout.write(self.style.SUCCESS('finish build material of KCM'))
		k.merge()
		self.stdout.write(self.style.SUCCESS('build KCM success!!!'))