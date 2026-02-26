from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend
from web.models.user import UserProfile


class GetOrCreateFriendView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            character_id = request.data['character_id']
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            friends = Friend.objects.filter(character_id=character_id, me=user_profile)
            if friends.exists():
                friend = friends.first()
            else :
                friend = Friend.objects.create(character_id=character_id, me=user_profile)
            character = friend.character
            author = character.author
            return Response({
                'result': 'success',
                'friend': {
                    'id': friend.id,
                    'character': {
                        'id': character.id,
                        'name': character.name,
                        'profile': character.profile,
                        'photo': character.photo.url,
                        'background_image': character.background_image.url,
                        'author': {
                            'user_id': author.user.id,
                            'username': author.user.username,
                            'photo': author.photo.url
                        }
                    }
                }
            })
        except:
            return Response({
                "result": "failed"
            })