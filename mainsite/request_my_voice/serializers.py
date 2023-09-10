from rest_framework import serializers
from .models import QAItem

class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QAItem
        fields = '__all__'