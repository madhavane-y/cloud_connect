from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from django.views.generic import RedirectView
from django.conf import settings

# URLs here

urlpatterns=[
    # path('',include('django.contrib.auth.urls')),
    url('login',views.login_view,name='login'),
    # path('',RedirectView.as_view(url='login')),
    path('account',include('dash.urls'))
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)