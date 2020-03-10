from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from main_project.models import File
from comments.models import  Comment
from main_project.forms FileForm
# Create your views here.


class IndexView(View):
	def get(self,request):
		files = File.objects.filter(owner_id=request.user.id)
		print(files)
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
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })