#!/usr/bin/python3
# No se permiten comillas dobles en la inserción a base de datos
import os, sys, glob, datetime, string, psycopg2, psycopg2.extras, shutil, math, argparse, getpass
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'dj_books.settings'
django.setup()
from books.models import *
from django.contrib.auth.models import Permission,  Group, User

class Mem:
	def __init__(self):
		self.con=self.connect()

	def connect(self):
		strmq="dbname='{}' port='{}' user='{}' host='{}' password='{}'".format(args.db, args.port, args.user, args.host, password)
		try:
			return psycopg2.extras.DictConnection(strmq)
		except psycopg2.Error:
			print("Error conecting database")
			sys.exit(112)

	def disconnect(self):
		self.con.close()


def Yn(pregunta):
	ok = False
	while True:
		user_input = input(pregunta +" [Y|n]").strip().lower()
		if not user_input or user_input == 'y':
			return True
		elif user_input == 'n':
			return False
		else:
			print ("Please enter 'Y', 'n'")


parser=argparse.ArgumentParser('Films documentation')
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--insert', help='Insert films from current numbered directory', action="store_true")
group.add_argument('-g', '--generate', help='Generate films documentation', action="store_true")
parser.add_argument('-U', '--user', help='Postgresql user', default='postgres')
parser.add_argument('-p', '--port', help='Postgresql server port', default=5432)
parser.add_argument('-H', '--host', help='Postgresql server address', default='127.0.0.1')
parser.add_argument('-d', '--db', help='Postgresql database', default='books')
args=parser.parse_args()

password=getpass.getpass()


dj_user = User.objects.get(username="worker")
print(dj_user)

mem=Mem()
#if Yn("¿Desea realizar la migración?")==True:
cur=mem.con.cursor()
cur.execute("select * from authors,books where authors.id_authors=books.id_authors")
for i, row in enumerate(cur.fetchall()):
	print(row['id_authors'])
	dj_author=Author(id=row['id_authors'],name=row['name'],family_name=row['family_name'], birth=row['birth'],death=row['death'])
	dj_author.save()
	dj_book=Book(id=row['id_books'], author=dj_author, title=row['title'], year=row['year'])
	dj_book.save()
	if row['valoration']!=None:
		dj_valoration=Valoration(id=i, book=dj_book, comment=row['comment'], read_start=row['read_start'], read_end=row['read_end'], user=dj_user, valoration=row['valoration']*10)
	else:
		dj_valoration=Valoration(id=i, book=dj_book, comment=row['comment'], read_start=row['read_start'], read_end=row['read_end'], user=dj_user, valoration=None)
	
	dj_valoration.save()
cur.close()

mem.disconnect()


