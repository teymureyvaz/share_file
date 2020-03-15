from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from main_project.models import File,UserFile
from comments.models import  Comment
from main_project.forms import FileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import email_or_username

class IndexView(View):
	def get(self,request):
		files = File.objects.filter(owner_id=request.user.id,is_active=True)
		print(files)
		message = None
		if len(files) < 1:
			message = "You dont have any uploaded files,upload a new file or check if other users shared a file with you"
		return render(request,'index.html',{"files":files, "message":message,"username":request.user.username})


class DetailView(View):
	def get(self,request,file_id):
		file = File.objects.get(id=file_id)
		shared_file = UserFile.objects.filter()
		print(request.user.is_authenticated)
		is_commentable = None
		comments = []
		if file.owner_id.id == request.user.id:
			is_commentable= True
		else:
			shared_file = UserFile.objects.filter(file_id=file_id,shared_user_id=request.user.id).values('is_commentable')
			print(shared_file)
			if shared_file.count() < 1:
				return HttpResponse("You dont have acces this file")
			is_commentable = shared_file[0]['is_commentable']
		if is_commentable == True:
			comments = Comment.objects.filter(file=file_id,is_active=True)
		user = request.user.username
		return render(request,'detail.html',{"file":file,"comments":comments,"username":user,"is_commentable":is_commentable})


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
		
@login_required
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
    	print(request.user)
    	file_obj = File(name=name,description=description,expiration_date=expiration_date,file=file,owner_id=request.user)
    	print(file_obj)
    	file_obj.save()
    	print("salam")
    	return redirect('/')
    else:
    	form = FileForm()
    	return render(request, 'upload.html', {'form': form })

@login_required
def share(request,file_id):
	if request.method == 'POST':
		username_or_email =request.POST.get("username_or_email")
		is_commentable = request.POST.get("comment")
		print(type(is_commentable))
		user = None
		if email_or_username(username_or_email):
			user = User.objects.filter(email=username_or_email)
			if not user:
				return render(request, 'share.html',{'error':"sorry,cannot find this email"})
		else:
			print("this is username")
			user = User.objects.filter(username=username_or_email)
			if not user:
				return render(request, 'share.html',{'error':"sorry,cannot find this username"})
		print(user[0])
		if user[0].username == request.user.username:
			return render(request, 'share.html',{'error':'You cant share file with yourself,sorry'})
		file = File.objects.get(id=file_id)
		user_obj = User.objects.get(id=user[0].id)

		uf = UserFile(file_id=file,shared_user_id=user_obj,is_commentable=is_commentable)
		uf.save()
		success =  f"File shared with {user[0].username}"
		return render(request, 'share.html',{'success':success})

	else:
		return render(request, 'share.html')

class SharedWithMe(View):
	def get(self,request):
		shared_files =  UserFile.objects.filter(shared_user_id=request.user.id)
		message = None
		if len(shared_files) <1 :
			message = "No one shared a file with you,you can ask them directly to share file with you."
		files = []
		for shared in shared_files:
			files.append(shared.file_id)

		return render(request,'shared_with_me.html',{"files":files,"message":message})

@login_required
def download(request,file_id):
	object_name = File.objects.get(id=file_id)
	filename = object_name.file.name.split('/')[-1]
	response = HttpResponse(object_name.file, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=%s' % filename

	return response