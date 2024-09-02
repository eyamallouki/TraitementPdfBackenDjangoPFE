from django.urls import path
from .AfficheFileView import AfficheFileView
from .ClientFilesView import get_patient_files
from .OCRProcessView import OCRProcessView, CropImageView
from .ResumerDocumentView import  DocumentProcessingView
from .UpdatePageOrderView import UpdatePageOrderView, GetPdfPagesView
from .delete_pdf import delete_pdf
from .uploadfileview import FileUploadView
from django.conf import settings
from django.conf.urls.static import static
from .AddNewPageView import AddNewPageView
from .DeletePagesView import DeletePagesView
from .RotatePagesView import RotatePagesView
from .MovePageView import MovePageView
from .ImportDocumentView import ImportDocumentView
from .ExtractPagesView import ExtractPagesView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('affichefile/', AfficheFileView.as_view(), name='affichefile'),
    path('delete/<int:pdf_id>/', delete_pdf, name='delete_pdf'),
    path('patient/<int:patient_id>/files/', get_patient_files, name='patient-files'),
    path('<int:pdf_id>/add-page/', AddNewPageView.as_view(), name='add-new-page'),
    path( 'process/', DocumentProcessingView.as_view(), name='document-processing' ),
    path('<int:pdf_id>/delete-pages/', DeletePagesView.as_view(), name='delete-pages'),
    path('<int:pdf_id>/rotate-pages/', RotatePagesView.as_view(), name='rotate-pages'),
    path('<int:pdf_id>/move-page/', MovePageView.as_view(), name='move-page'),
    path('<int:pdf_id>/import-document/', ImportDocumentView.as_view(), name='import-document'),
    path('<int:pdf_id>/extract-pages/', ExtractPagesView.as_view(), name='extract-pages'),
    path('pdf/<int:pdf_id>/update-page-order/', UpdatePageOrderView.as_view(), name='update_page_order'),
    path('pdf/<int:pdf_id>/pages/', GetPdfPagesView.as_view(), name='pdf_pages'),
    path( 'ocr/<int:pdf_id>/', OCRProcessView.as_view(), name='ocr_process' ),
    path( 'crop/<int:image_id>/', CropImageView.as_view(), name='crop_image' ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
