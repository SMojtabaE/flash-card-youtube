from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from card.models import FlashCard
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from card.serializers import (
    CreateFlashCardSerializer,
    UpdateFlashCardSerializer,
    ListFlashCardSerializer,
)



class CreateFlashCardView(APIView):

    permission_classes=(IsAuthenticated,)

    def post(self, request):

        serializer = CreateFlashCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateFlashCardView(APIView):
    
    permission_classes=(IsAuthenticated,IsOwner)

    def put(self, request, id):

        flash_card = get_object_or_404(FlashCard, id=id)

        serializer = UpdateFlashCardSerializer(
            data=request.data, instance=flash_card)

        self.check_object_permissions(request,flash_card) # checks if the user is the owner of flash-cards
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteFlashCardView(APIView):
    
    permission_classes=(IsAuthenticated,IsOwner)

    def delete(self, request, id):
        flash_card = get_object_or_404(FlashCard, id=id)
        self.check_object_permissions(request,flash_card)  # checks if the user is the owner of flash-cards
        flash_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class ListFlashCardsView(APIView):
    
    permission_classes = (IsAuthenticated,IsOwner)
    
    def get(self, request, user_id):

        all_user_flash_cards = get_list_or_404(FlashCard, user__id=user_id)

        serializer = ListFlashCardSerializer(all_user_flash_cards, many=True)
        self.check_object_permissions(request, all_user_flash_cards[0])  # checks if the user is the owner of flash-cards
        return Response(serializer.data)
