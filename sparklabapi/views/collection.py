from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from sparklabapi.models.collection import Collection
from sparklabapi.models.user import User

class CollectionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Collection
    fields = ('id', 'user', 'name', 'cover', 'ideas')
    depth = 3

class CollectionView(ViewSet):
    def retrieve(self, request, pk):
      try:
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collection, context={'request': request})
        return Response(serializer.data)
      except Collection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
      
    def list(self, request):
      collections=Collection.objects.all()
      serializer = CollectionSerializer(collections, many=True, context={'request': request})
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
      user = User.objects.get(id=request.data["user"])
      
      collection = Collection.objects.create(
        user = user,
        name = request.data['name'],
        cover = request.data['cover'],
      )
      if 'ideas' in request.data:
        collection.ideas.set(request.data['ideas'])
      serializer = CollectionSerializer(collection)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
      try:
        collection = Collection.objects.get(pk=pk)
        
        collection.user = User.objects.get(pk=request.data['user'])
        collection.name = request.data['name']
        collection.cover = request.data['cover']
        collection.ideas.set(request.data['ideas'])
        collection.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      except Collection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
      except User.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
      except KeyError:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk):
      collection = Collection.objects.get(pk=pk)
      collection.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
