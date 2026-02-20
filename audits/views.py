from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AuditReport
from documents.models import Document
from analysis.models import AnalysisResult
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io

@login_required
def generate_audit_report(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    analysis = AnalysisResult.objects.filter(document=doc).first()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Audit Report for: {doc.title}")
    p.drawString(100, 780, f"Status: {doc.status}")
    if analysis:
        p.drawString(100, 760, f"Compliance Score: {analysis.compliance_score}%")
        p.drawString(100, 740, f"Details: {analysis.details}")
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="audit_report_{doc.id}.pdf"'
    return response
