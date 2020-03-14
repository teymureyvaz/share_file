"""sharefile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from main_project import views

from django.contrib.auth.decorators import login_required, permission_required
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_required(views.IndexView.as_view()),name="home"),
    path('shared/',views.SharedWithMe.as_view(),name="shared"),
    path('file/<int:file_id>/',login_required(views.DetailView.as_view()),name="detail"),
    path('',include('django.contrib.auth.urls')),
    path('signup/', views.signup_view, name="signup"),
    path('upload/',views.model_form_upload,name="model_form_upload"),
    path('share/<int:file_id>/',views.share,name="share"),
    path('download/<int:file_id>/',views.download,name="download"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)