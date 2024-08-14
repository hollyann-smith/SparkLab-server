from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from sparklabapi.models import Supply

class SupplySerializer(serializers.ModelSerializer):
  class Meta:
    model = Supply
    fields = ['id', 'name']
    depth = 2
    
class SupplyView(ViewSet):
  def retrieve(self, request, pk):
    try:
      supply = Supply.objects.get(pk=pk)
      serializer = SupplySerializer(supply, context={'request':request})
      return Response(serializer.data)
    except Supply.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    supply = Supply.objects.all()
    serializer = SupplySerializer(supply, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    try:
      name = request.data['name']
      supply = Supply.objects.create(
        name=name,
      )
      serializer = SupplySerializer(supply, context={'request': request})
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Supply.DoesNotExist:
            return Response({'error': 'Invalid part'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
          
  def update(self, request, pk):
    try:
      supply = Supply.objects.get(pk=pk)
      
      supply.name = request.data['name']
      supply.save()
      return Response(None, status=status.HTTP_204_NO_CONTENT)
    except Supply.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    except KeyError:
      return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)   

  def destroy(self, request, pk):
        try:
            supply = Supply.objects.get(pk=pk)
            supply.delete()
            return Response({'message': 'Supply deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Supply.DoesNotExist:
            return Response({'message': 'Supply not found'}, status=status.HTTP_404_NOT_FOUND)
