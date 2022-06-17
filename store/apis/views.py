from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import response
from store.models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product(request):

    if request.method == 'GET':
        snippets = Product.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)