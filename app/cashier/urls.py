from django.urls import path
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.conf.urls.static import static

#admin
def is_staff(user):
    return user.is_authenticated and user.is_staff
#user
def is_not_staff(user):
    return user.is_authenticated and not user.is_staff


urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('home', views.home, name='home'),

    path('home/list/', views.list, name='list'),
    path('home/record/<int:pk>', views.singular_record, name='record'),

    #crud admin
    path('home', user_passes_test(is_staff)(views.home), name="home"),
    path('home/create-gun', user_passes_test(is_staff)(views.create_record), name="create-gun"),
    path('home/update-record/<int:pk>', user_passes_test(is_staff)(views.update_record), name='update-record'),
    path('home/delete-record/<int:pk>', user_passes_test(is_staff)(views.delete_record), name="delete-record"),
     path('make-order', user_passes_test(is_staff)(views.create_order), name='make-order'),
    path('order_detail/<int:pk>/', user_passes_test(is_staff)(views.order_detail), name='order_detail'),
    path('make-payment/<int:pk>/', user_passes_test(is_staff)(views.make_payment), name='make-payment'),
     path('laporan_transaksi', user_passes_test(is_staff)(views.laporan_transaksi), name='laporan_transaksi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)