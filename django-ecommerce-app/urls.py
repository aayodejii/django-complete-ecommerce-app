from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
	# path('admin/doc/', include('django.contrib.admindocs.urls'))
	path('', include('themall.urls')),
	path('seller/', include('seller.urls')),
]


urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)