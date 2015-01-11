import os
import sys
import shutil
import events
import random
import datetime
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roombook.settings")

from django.core.files import File

from django.contrib.auth.models import User,Group
from django.core.management import execute_from_command_line
from django.utils import timezone


function_list=[]
SETUP_SUPPORT_FOLDER='setup_support'

def clean_to_string(string):
	'''
	removes non ascii characters
	'''
	allowed='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'#alphabets
	allowed+=allowed.lower()#lowercase
	allowed+='!@#$%^&*()_+=-.,: '
	allowed+="'"
	allowed+='\n'
	new_str=''
	for i in string:
		if i in allowed:
			new_str+=i
	return new_str



def locations():
	'''
	locations in college'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'locations')
	f=open(filepath,'r')
	loc=f.readlines()
	f.close()
	for i in loc:
		l=events.models.Location()
		l.name=i.strip().capitalize()[:40]
		l.save()
function_list.append(locations)
#------------------------------------------------------------------------------------------------
def run_function(fn):
	'''Runs the function and acts as a wrapper'''
	print(fn.__name__.replace('_',' ').capitalize())
	fn()
	print ('--------->Done')
	
def run_setup():
	print ('================================================================')
	for i in function_list:
		run_function(i)	
	print ('EVENTS SETUP COMPLETE')
	print ('================================================================')
