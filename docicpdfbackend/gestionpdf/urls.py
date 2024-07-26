from django.urls import path
from .AfficheFileView import AfficheFileView
from .ClientFilesView import get_patient_files
from .delete_pdf import delete_pdf
from .uploadfileview import PDFUploadView, get_pdf_images
from django.conf import settings
from django.conf.urls.static import static
from .AddNewPageView import AddNewPageView
from .DeletePagesView import DeletePagesView
from .RotatePagesView import  RotatePagesView
from .MovePageView import  MovePageView
from .ImportDocumentView import  ImportDocumentView
from .ExtractPagesView import ExtractPagesView

urlpatterns = [
    path('upload/', PDFUploadView.as_view(), name='file-upload'),
    path('affichefile/', AfficheFileView.as_view(), name='affichefile'),
    path('pdf/<int:pdf_id>/images/', get_pdf_images, name='pdf_images'),
    path('delete/<int:pdf_id>/', delete_pdf, name='delete_pdf'),
    path('patient/<int:patient_id>/files/', get_patient_files, name='patient-files'),
    path('<int:pdf_id>/add-page/', AddNewPageView.as_view(), name='add-new-page'),
    path('<int:pdf_id>/delete-pages/', DeletePagesView.as_view(), name='delete-pages'),
    path('<int:pdf_id>/rotate-pages/', RotatePagesView.as_view(), name='rotate-pages'),
    path('<int:pdf_id>/move-page/', MovePageView.as_view(), name='move-page'),
    path('<int:pdf_id>/import-document/', ImportDocumentView.as_view(), name='import-document'),
    path('<int:pdf_id>/extract-pages/', ExtractPagesView.as_view(), name='extract-pages'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
