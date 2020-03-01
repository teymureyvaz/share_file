from django.shortcuts import render
from django.views import View
from main_project.models import File
# Create your views here.


class IndexView(View):
	def get(self,request):
		files = File.objects.filter(owner_id=request.user.id)
		print(files)
		return render(request,'index.html',{"files":files})

