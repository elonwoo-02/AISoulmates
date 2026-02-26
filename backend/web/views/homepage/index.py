from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.character import Character


class HomepageIndexView(APIView):
    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count', 0))
            search_query = request.query_params.get('search_query', '').strip()
            if search_query:
                queryset = Character.objects.filter(
                    Q(name__icontains=search_query)
                )
            else:
                queryset = Character.objects.all()
            characters_raw = queryset.order_by('-id')[items_count:items_count+10]
            characters = []
            for character in characters_raw:
                author = character.author
                characters.append({
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url if character.photo else '',
                    'background_image': character.background_image.url if character.background_image else '',
                    'author': {
                        'user_id': author.user_id,
                        'username': author.user.username,
                        'photo': author.photo.url if author.photo else ''
                    }
                })
            return Response({
                "result": "success",
                "characters": characters
            })
        except Exception as e:
            return Response({
                "result": f"An error occurred"
            })
