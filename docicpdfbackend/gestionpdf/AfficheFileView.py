from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PDF
from .AffichefileSerializer import AffichpdfSerializer

class AfficheFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        pdf_files = []
        txt_files = []
        jpg_files = []
        png_files = []
        other_files = []

        for pdf in PDF.objects.filter(patient_associé=user):
            if pdf.file:  # Vérifie si le fichier existe et n'est pas None
                file_ext = pdf.file.name.lower()
                if file_ext.endswith('.pdf'):
                    pdf_files.append(pdf)
                elif file_ext.endswith('.txt'):
                    txt_files.append(pdf)
                elif file_ext.endswith('.jpg'):
                    jpg_files.append(pdf)
                elif file_ext.endswith('.png'):
                    png_files.append(pdf)
                else:
                    other_files.append(pdf)

        response_data = {
            'pdf_files': AffichpdfSerializer(pdf_files, many=True).data,
            'txt_files': AffichpdfSerializer(txt_files, many=True).data,
            'jpg_files': AffichpdfSerializer(jpg_files, many=True).data,
            'png_files': AffichpdfSerializer(png_files, many=True).data,
            'other_files': AffichpdfSerializer(other_files, many=True).data,
        }
        return Response(response_data)
