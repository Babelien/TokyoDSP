from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('signup/', SignUpView.as_view()),
    path('', AccountUpdateView.as_view()),
    path('profile/', ProfileUpdateView.as_view()),
    path('password_reset/', PasswordReset.as_view()), # Django 4.0でメール送信エラー確認。4.2.7にアップデートで解消
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
]