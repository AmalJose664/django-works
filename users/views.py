from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError
# Create your views here.

def signup(request):
	error_message=None
	user = None

	if request.POST:
		
		username = request.POST.get('username')	
		email = request.POST.get('email')	
		password = request.POST.get('password')	

		print(username,password,email)
		try:

			user = User.objects.create_user(username=username,password=password,email=email)
			user.full_clean() 
			
		except Exception as e:
			
			
			error_message="Email and Username must be unique"
			
			


	return render (request,'users/create.html',{'user':user,'error':error_message})

def loginUser(request):

	error_message=None
	user = None
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user:
			login(request,user)
			return redirect('list')
		else:
			error_message="invalid credentials "
	
	return render(request ,'users/login.html',{'user':user,'error':error_message})



def logoutUser(request):
	logout(request)

	return redirect('login')

