from .models import Sale
from rest_framework import serializers


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class SaleAggrSerializer(serializers.Serializer):
    created_on__date = serializers.DateField()
    total = serializers.IntegerField()
    amount = serializers.FloatField()



