from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from.import views

app_name='schoolapp'

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login',views.login_view,name='login'),
    path('student_add', views.student_add, name='student_add'),
    path('load_courses/', views.load_courses, name='load_courses'),
    path('logout/',views.logout,name='logout'),
    path('confirm',views.confirm, name='confirm'),
 
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)