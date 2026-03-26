from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import BankStatementParser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class BankStatementUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = request.FILES['file']
        try:
            result = BankStatementParser.parse_and_categorize(csv_file, request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)

@login_required
def bank_upload_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        view = BankStatementUploadView()
        response = view.post(request)
        if response.status_code == 201:
            messages.success(request, "Bank statement uploaded and processed successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, f"Error: {response.data.get('error', 'Unknown error')}")
            return redirect('bank-upload')
    return render(request, 'bank/bank_upload.html')
