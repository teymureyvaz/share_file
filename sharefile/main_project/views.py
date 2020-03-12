from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from main_project.models import File
from comments.models import  Comment
from main_project.forms import FileForm
from django.contrib.auth.models import User
# Create your views here.
import re

def email_or_username(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


class IndexView(View):
	def get(self,request):
		files = File.objects.filter(owner_id=request.user.id)
		return render(request,'index.html',{"files":files})


class DetailView(View):
	def get(self,request,file_id):
		file = File.objects.get(id=file_id)
		comments = Comment.objects.filter(file=file_id)
		return render(request,'detail.html',{"file":file,"comments":comments})


def signup_view(request):
	form = UserCreationForm()
	if request.method == 'POST':
	    form = UserCreationForm(request.POST)
	    if form.is_valid():
	        form.save()
	        username = form.cleaned_data.get('username')
	        password = form.cleaned_data.get('password1')
	        user = authenticate(username=username, password=password)
	        login(request, user)
	        return redirect('home')
	    return render(request, 'registration/register.html', {'form': form})
	else:
		return render(request,'registration/register.html', {'form': form})

def model_form_upload(request):
    if request.method == 'POST':
    	print(request.POST)
    	print("___________________")
    	name = request.POST.get('name')
    	print(name)
    	description  = request.POST.get('description')
    	expiration_date = request.POST.get('expiration_date')
    	file= request.FILES.get('file')
    	print(file)
    	file_obj = File(name=name,description=description,expiration_date=expiration_date,file=file,owner_id=request.user)
    	print(file_obj)
    	file_obj.save()
    	print("salam")
    	return redirect('/')
    else:
    	form = FileForm()
    	return render(request, 'upload.html', {'form': form })


def share(request,file_id):
	if request.method == 'POST':
		username_or_email =request.POST.get("username_or_email")
		if email_or_username(username_or_email):
			user = User.objects.filter(email=username_or_email)

		else:
			print("this is username")
			user = User.objects.filter(username=username_or_email)
			if not user:
				return render 
		return redirect('/')
	else:
		return render(request, 'share.html')