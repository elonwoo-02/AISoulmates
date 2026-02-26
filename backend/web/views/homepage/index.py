from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.character import Character


class HomepageIndexView(APIView):
    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count', 0))
            characters_raw = Character.objects.all().order_by('-id')[items_count:items_count+10]
            characters = []
            for character in characters_raw:
                author = character.author
                characters.append({
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                    'author': {
                        'user_id': author.user_id,
                        'username': author.user.username,
                        'photo': author.photo.url
                    }
                })
            return Response({
                "result": "success",
                "characters": characters
            })
        except Exception as e:
            return Response({
                "result": f"An error occurred: {str(e)}"
            })
