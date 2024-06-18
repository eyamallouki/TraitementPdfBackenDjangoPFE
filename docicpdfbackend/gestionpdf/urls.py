from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

from .AfficheFileView import AfficheFileView
from .PDFDetailView import PDFDetailView
from .uploadfileview import  PDFUploadView

urlpatterns = [
    path('upload/', PDFUploadView.as_view(), name='file-upload'),
    path('affichefile/', AfficheFileView.as_view(), name='affichefile'),
    path('pdfs/<int:pk>/', PDFDetailView.as_view(), name='pdf-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
