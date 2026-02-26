from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend


class GetListFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count', 0))
            friends_raw = Friend.objects.filter(
                me__user=request.user,
            ).order_by('-update_time')[items_count: items_count + 20]
            friends = []
            for friend in friends_raw:
                character = friend.character
                author = character.author
                friends.append({
                    'id': friend.id,
                    'character': {
                        'id': character.id,
                        'name': character.name,
                        'profile': character.profile,
                        'photo': character.photo.url if character.photo else '',
                        'background_image': character.background_image.url if character.background_image else '',
                        'author': {
                            'user_id': author.user.id,
                            'username': author.user.username,
                            'photo': author.photo.url if author.photo else '',
                        }
                    }
                })
            return Response({
                'result': 'success',
                'friends': friends,
            })
        except:
            return Response({
                'result': 'failed'
            })
