from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from web.models.character import Character


class HomepageIndexView(APIView):
    def get(self, request):
        try:
            items_count = int(request.query_params.get('items_count', 0))
            if items_count < 0:
                items_count = 0
            search_query = request.query_params.get('search_query', '').strip()
            if search_query:
                terms = [term for term in search_query.split() if term]
                queryset = Character.objects.all()
                for term in terms:
                    queryset = queryset.filter(
                        Q(name__icontains=term)
                        | Q(profile__icontains=term)
                        | Q(author__user__username__icontains=term)
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
        except (TypeError, ValueError):
            return Response({
                "result": "invalid_items_count",
                "characters": []
            }, status=400)
        except Exception:
            return Response({
                "result": "An error occurred",
                "characters": []
            }, status=500)
