from home.models import *
from login.models import *
from costmanagement.models import *
from datetime import datetime
from django.contrib.auth import authenticate, login

user=None
def logger(username):
	global user
	user=username

	return True

def UserName():
	# print(user)
	return str(user)


def Logging(request,action):
	if request.user.is_authenticated:

		print(str(request.user.name) +' in auth')
	# try:
	# 	auth=Users.objects.get(name=user).authority
	# 	print(auth+'in log')
	# except Exception as e:
	# 	print(e)
	# 	auth=None

		logtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		try:
			print('logging '+logtime)
			log=Log.objects.create(logdate=logtime,user=request.user.name,authority=request.user.authority,action=action)
			log.save()
			print('logged')
		except Exception as e:
			print(e)
	return True
