from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from core.models import Post, Category, Competition
from emails.models import EmailTemplate
from submit.models import Profile
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.project.settings import ADMIN_PATH
from core.views import index, subscribe, unsub, subscribed, terms, unsubscribe, unsubscribed, optout, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CategoryPostListView


class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)
admin_site.register(Post)
admin_site.register(Category)
admin_site.register(Competition)
admin_site.register(EmailTemplate)
admin_site.register(Profile)

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('psm-secure-admin/', admin_site.urls),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name='post-delete'),
    path('category/<int:pk>/',CategoryPostListView.as_view(),name='category-posts'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user-posts/<str:username>/',UserPostListView.as_view(),name='user-posts'),
    path('subscribe/', subscribe, name='subscribe'),
    path('subscribed/', subscribed, name='subscribed'),
    path('competition_list/', views.competition_list, name='competition_list'),
    path('submit/<int:competition_id>/',views.submit_entry,name='submit_entry'),
    path('create/', views.create_competition, name='create_competition'),
    path('', include('submit.urls')),
    path('', include('emails.urls')),
    path('optout/', optout, name='optout'),
    path('unsub/', unsub, name='unsub'),
    path('terms/', terms, name='terms'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
    path('unsubscribed/', unsubscribed, name='unsubscribed'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='submit/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='submit/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='submit/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='submit/password_reset_complete.html'),name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
