from django.urls import path
from . import views

#  Users will be listed on the first opened page and a new user will be posted.
#  By going to the 'get_patch_user/<int:user_id>/' extension, the user with the entered id will be brought and
#  a partial update will be applied to this user.
#  By going to the 'get_put_delete/<int:user_id>/' extension, the user with the entered id will be brought and
#  this user can be updated or deleted.

urlpatterns = [
    path('', views.add_user, name="get_post_user"),
    path('get_patch_user/<int:user_id>/', views.patch_user, name="get_patch_user"),
    path('get_put_delete/<int:user_id>/', views.update_delete_user, name="get_put_delete")
]
