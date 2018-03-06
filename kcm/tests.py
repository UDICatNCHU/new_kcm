from django.test import TestCase
from kcm import KCM
from udic_nlp_API.settings_database import uri
kcmObject = KCM(uri=uri)

class APITestCase(TestCase):
	def test_get(self):
		a = kcmObject.get('周杰倫',10)
		b = kcmObject.get('周杰倫a',10)
		del a['similarity']
		del b['similarity']
		assert a == b and a != None

		a = kcmObject.get('周杰倫',10, valueFlag=['nr'])
		b = kcmObject.get('周杰倫a',10, valueFlag=['nr'])
		del a['similarity']
		del b['similarity']
		assert a == b and a != None

		a = kcmObject.get('周杰倫',10, keyFlag=['nr'], valueFlag=['nr'])
		b = kcmObject.get('周杰倫a',10, keyFlag=['nr'], valueFlag=['nr'])
		del a['similarity']
		del b['similarity']
		assert a == b and a != None

	def test_GridFS(self):
		assert type(kcmObject.get('曾經', 10)) == dict

		