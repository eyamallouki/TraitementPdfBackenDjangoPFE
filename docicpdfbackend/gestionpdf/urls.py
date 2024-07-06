from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from eventlet import serve
from .AfficheFileView import AfficheFileView
from .PDFDetailView import  ServePDFView
from .delete_pdf import delete_pdf
from .uploadfileview import PDFUploadView

urlpatterns = [
    path('upload/', PDFUploadView.as_view(), name='file-upload'),
    path('affichefile/', AfficheFileView.as_view(), name='affichefile'),
    path( 'pdfs/', serve, {'document_root': settings.MEDIA_ROOT} ),
    path('pdfs/<str:filename>/', ServePDFView.as_view(), name='serve-pdf'),
    path('delete/<int:pdf_id>/', delete_pdf, name='delete_pdf'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
