from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    # Post URLs
    path('', views.PostListView.as_view(), name='home'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like-comment'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='update-comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add-reply'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)