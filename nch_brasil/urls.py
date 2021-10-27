from django.contrib import admin
from django.urls import path
from nch import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('nch/funds_nch', views.funds_nch, name='funds_nch'),
    path('nch/funds_ibx', views.funds_ibx, name='funds_ibx'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
