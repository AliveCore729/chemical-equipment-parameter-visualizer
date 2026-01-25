from django.urls import path
from .views import UploadCSVView, DatasetHistoryView, DatasetPDFView

urlpatterns = [
    path("upload/", UploadCSVView.as_view()),
    path("history/", DatasetHistoryView.as_view()),
    path("report/<int:dataset_id>/", DatasetPDFView.as_view()),
]
