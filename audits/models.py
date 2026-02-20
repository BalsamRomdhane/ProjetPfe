from django.db import models
from documents.models import Document
from django.conf import settings

class AuditReport(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='audit_reports/')

    def __str__(self):
        return f"Audit Report for {self.document.title}"
