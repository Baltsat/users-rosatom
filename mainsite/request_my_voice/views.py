from django.shortcuts import render
from rest_framework import viewsets
from .models import QAItem
from .serializers import QASerializer
# Create your views here.

class QAItemAPIView(viewsets.ModelViewSet):
    """
    API endpoint that allows QAItem to be viewed or created.
    """
    queryset = QAItem.objects.all()
    serializer_class = QASerializer