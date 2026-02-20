from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm
from .models import Document
from accounts.decorators import department_required

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.department = request.user.department
            doc.save()
            return redirect('employee_dashboard')
    else:
        form = DocumentUploadForm()
    return render(request, 'documents/upload.html', {'form': form})

@login_required
def list_documents(request):
    if hasattr(request.user, 'department'):
        docs = Document.objects.filter(department=request.user.department)
    else:
        docs = Document.objects.none()
    return render(request, 'documents/list.html', {'documents': docs})
