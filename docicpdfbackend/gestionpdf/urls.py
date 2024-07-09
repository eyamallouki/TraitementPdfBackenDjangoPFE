from django.urls import path
from .AfficheFileView import AfficheFileView
from .ClientFilesView import  get_patient_files
from .PDFDetailView import  ServePDFView
from .delete_pdf import delete_pdf
from .uploadfileview import PDFUploadView, get_pdf_images
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', PDFUploadView.as_view(), name='file-upload'),
    path('affichefile/', AfficheFileView.as_view(), name='affichefile'),
    path( 'pdf/<int:pdf_id>/images/', get_pdf_images, name='pdf_images' ),
    path('delete/<int:pdf_id>/', delete_pdf, name='delete_pdf'),
    path( 'patient/<int:patient_id>/files/', get_patient_files, name='patient-files' ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


