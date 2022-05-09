from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views as view
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'posts.views.page_not_found'  # noqa
handler500 = 'posts.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('posts.urls')),

]

urlpatterns += [
    path('about/about-author/', view.flatpage, {'url': '/about-author/'}, name='about'),
    path('about/about-spec/', view.flatpage, {'url': '/about-spec/'}, name='tech'),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')), ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
