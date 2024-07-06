# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import PDF

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_pdf(request, pdf_id):
    if request.method == 'DELETE':
        pdf = get_object_or_404(PDF, pk=pdf_id)
        pdf.delete()
        return JsonResponse({'message': 'PDF deleted successfully!'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed!'}, status=405)
