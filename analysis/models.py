from django.db import models
from documents.models import Document

class AnalysisResult(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    compliance_score = models.FloatField()
    analysis_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"Analysis for {self.document.title}"
