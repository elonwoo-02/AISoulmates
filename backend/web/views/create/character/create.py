from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character
from web.models.user import UserProfile

# 角色创建接口
class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            name = request.data.get('name').strip()
            profile = request.data.get('profile').strip()[:100000]
            photo = request.FILES.get('photo', None)
            background_image = request.FILES.get('background_image', None)

            if not name:
                return Response({
                    "result": "Name is required."
                })
            if not profile:
                return Response({
                    "result": "Profile is required."
                })
            if not photo:
                return Response({
                    "result": "Photo is required."
                })
            # if not background_image:
            #     return Response({
            #         "result": "Background image is required."
            #     })
            Character.objects.create(
                author=user_profile,
                name=name,
                profile=profile,
                photo=photo,
                background_image=background_image,
            )
            return Response({
                "result": "success"
            })
        except:
            return Response({
                "result": "An error occurred while creating the character."
            })