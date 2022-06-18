from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product(request):

    if request.method == 'GET':
        snippets = Product.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serrializer.data, status=status.HTTP_201_CREATED)
        return Response(serialier.errors, status=status.HTTP_400_BAD_REQUEST)