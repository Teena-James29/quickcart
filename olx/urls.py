"""
URL configuration for olx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from shop.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homefn),
    path('login/',loginfn),
    path('form/',formfn),
    path('logout/',logoutfn),
    path('profile/',profilefn),
    path('register/',registerfn),
    path('about/',aboutfn),
    path('buynow/', buynowfn),
    path('addprofile/',addprofilefn),
    path('addproduct/',addproductfn),
    path('viewproduct/<int:pid>/',viewproductfn),
    path('editproduct/<int:pid>/',editproductfn),
    path('deleteproduct/<int:pid>/',deletefn),
    path('viewcategory/<int:cid>/', viewcategoryfn),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/<str:action>/',update_quantity, name='update_quantity'),
    path('userprofile/<int:uid>/',userprofilefn),
     path('editprofile/',editprofilefn),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
