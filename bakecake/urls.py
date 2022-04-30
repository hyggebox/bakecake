from django.contrib import admin
from django.urls import path, include

from cakes import views
from .views import render_index_page
from .views import render_lk_page
from .views import cake_api
from .views import success_page, fail_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render_index_page, name='render_index_page'),
    path('lk', render_lk_page, name='render_lk_page'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/cake', cake_api),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('auth/', include('django.contrib.auth.urls')),
    path('success', success_page),
    path('fail', fail_page),
]
