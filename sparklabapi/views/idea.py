from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from sparklabapi.models.idea import Idea
from sparklabapi.models.user import User

class IdeaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Idea
    fields = ('id', 'user', 'title', 'description', 'saved', 'img', 'supplies' )
    depth = 3
    
class IdeaView(ViewSet):
  def retrieve(self, request, pk):
    try:
      idea = Idea.objects.get(pk=pk)
      serializer = IdeaSerializer(idea, context={'request': request})
      return Response(serializer.data)
    except Idea.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    ideas=Idea.objects.all()
    serializer = IdeaSerializer(ideas, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
            user = User.objects.get(id=request.data["user"])
            
            idea = Idea.objects.create(
              user = user,
              title = request.data['title'],
              description = request.data['description'],
              saved = request.data['saved'],
              img = request.data['img'],
            )
            if 'supplies' in request.data:
              idea.supplies.set(request.data['supplies'])
            serializer = IdeaSerializer(idea)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          
  def update(self, request, pk):
    try:
      idea = Idea.objects.get(pk=pk)
      
      idea.user = User.objects.get(pk=request.data['user'])
      idea.title = request.data['title']
      idea.description = request.data['description']
      idea.saved = request.data['saved']
      idea.img = request.data['img']
      idea.supplies.set(request.data['supplies'])
      idea.save()
      return Response(None, status=status.HTTP_204_NO_CONTENT)
    except Idea.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)      

  def destroy(self, request, pk):
    idea = Idea.objects.get(pk=pk)
    idea.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
