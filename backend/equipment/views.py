import pandas as pd
import io
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import Dataset
from .serializers import UserSerializer  

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) 
    serializer_class = UserSerializer

class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_csv(file)

            total_equipment = len(df)
            avg_flowrate = float(df["Flowrate"].mean())
            avg_pressure = float(df["Pressure"].mean())
            avg_temperature = float(df["Temperature"].mean())
            type_distribution = df["Type"].value_counts().to_dict()

            dataset = Dataset.objects.create(
                filename=file.name,
                total_equipment=total_equipment,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature,
                type_distribution=type_distribution
            )

            return Response({
                "message": "CSV uploaded successfully",
                "dataset_id": dataset.id,
                "total_equipment": total_equipment,
                "avg_flowrate": avg_flowrate,
                "avg_pressure": avg_pressure,
                "avg_temperature": avg_temperature,
                "type_distribution": type_distribution
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class DatasetHistoryView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        datasets = Dataset.objects.order_by("-uploaded_at")[:5]

        history = []
        for d in datasets:
            history.append({
                "id": d.id,
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "total_equipment": d.total_equipment,
                "avg_flowrate": d.avg_flowrate,
                "avg_pressure": d.avg_pressure,
                "avg_temperature": d.avg_temperature,
                "type_distribution": d.type_distribution,
            })

        return Response(history)


class DatasetPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=404)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        text = p.beginText(40, 800)
        text.setFont("Helvetica", 12)

        text.textLine("Chemical Equipment Parameter Report")
        text.textLine("")
        text.textLine(f"Filename: {dataset.filename}")
        text.textLine(f"Uploaded At: {dataset.uploaded_at}")
        text.textLine("")
        text.textLine(f"Total Equipment: {dataset.total_equipment}")
        text.textLine(f"Average Flowrate: {dataset.avg_flowrate:.2f}")
        text.textLine(f"Average Pressure: {dataset.avg_pressure:.2f}")
        text.textLine(f"Average Temperature: {dataset.avg_temperature:.2f}")
        text.textLine("")
        text.textLine("Equipment Type Distribution:")

        for k, v in dataset.type_distribution.items():
            text.textLine(f"  - {k}: {v}")

        p.drawText(text)
        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"{dataset.filename}_report.pdf"
        )