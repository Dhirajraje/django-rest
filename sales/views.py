# Create your views here.
from datetime import datetime, timedelta
from rest_framework import status
from pandas import read_excel
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate


from sales.models import Sale
from .serializer import SaleAggrSerializer, SaleSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sales(request):
    sales = Sale.objects.filter(
        sales_person=request.user.id).order_by('-created_on')
    count = sales.count()
    serializedSale = SaleSerializer(sales[int(request.query_params.get(
        'page_no', 0)):min(int(request.query_params.get('page_size', 15))+int(request.query_params.get('page_no', 0)), count)], many=True)
    return Response({'data': serializedSale.data, 'count': count}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sales_aggr(request):
    no_of_days = int(request.query_params.get('no_of_days', 7))
    start_date = datetime.now()+timedelta(days=-no_of_days)
    sales = Sale.objects.filter(
        sales_person=request.user.id, created_on__range=(start_date, datetime.now())).values('created_on__date').order_by('created_on__date').annotate(**{
            'total': Count('id'),
            'amount': Sum('sale_amount')
        }).values('total', 'amount', 'created_on__date')
    serialized_sale = SaleAggrSerializer(sales, many=True)
    return Response({'result': serialized_sale.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_sale(request):
    serializedSale = SaleSerializer(data=request.data)
    if serializedSale.is_valid():
        serializedSale.save()
        return Response(serializedSale.data, status=status.HTTP_200_OK)
    return Response(serializedSale.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def upload_sales_excel(request):
    print(dir(request.FILES.get('file')))
    result = read_excel(request.FILES.get(
        'file')).transpose().to_dict().values()
    for entry in result:
        sale = SaleSerializer(data=entry)
        if sale.is_valid():
            sale.save()
    return Response({'success': True}, status=status.HTTP_201_CREATED)
