from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from documents.models import Document
from .models import AnalysisResult
import PyPDF2
import io
from django.contrib import messages

ISO_9001_CLAUSES = [
    'Scope', 'Normative references', 'Terms and definitions', 'Context of the organization',
    'Leadership', 'Planning', 'Support', 'Operation', 'Performance evaluation', 'Improvement'
]

@login_required
def launch_analysis(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    if doc.file.name.endswith('.pdf'):
        file_stream = doc.file.open('rb')
        reader = PyPDF2.PdfReader(file_stream)
        text = " ".join(page.extract_text() or '' for page in reader.pages)
        file_stream.close()
    else:
        text = ''
    score = 0
    found_clauses = []
    for clause in ISO_9001_CLAUSES:
        if clause.lower() in text.lower():
            score += 1
            found_clauses.append(clause)
    compliance_score = round((score / len(ISO_9001_CLAUSES)) * 100, 2)
    details = f"Found clauses: {', '.join(found_clauses)}"
    AnalysisResult.objects.update_or_create(document=doc, defaults={
        'compliance_score': compliance_score,
        'details': details
    })
    messages.success(request, f'Analysis complete. Compliance score: {compliance_score}%')
    return redirect('list_documents')

@login_required
def view_analysis(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    analysis = AnalysisResult.objects.filter(document=doc).first()
    return render(request, 'analysis/view.html', {'document': doc, 'analysis': analysis})
