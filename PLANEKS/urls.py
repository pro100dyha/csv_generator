from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from challenge import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(views.DataSchemaList.as_view()), name='profile-list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('schema/add/', login_required(views.DataSchemaFieldCreate.as_view()), name='profile-add'),
    path('schema/<int:pk>/', login_required(views.DataSchemaFieldUpdate.as_view()), name='profile-update'),
    path('schema/<int:pk>/delete/', login_required(views.DataSchemaDelete.as_view()), name='profile-delete'),
    path('generator/', login_required(views.DataSetGenerate.as_view()), name='generator'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
