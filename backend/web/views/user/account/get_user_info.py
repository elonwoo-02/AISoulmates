from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile


class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            return Response({
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'photo': user_profile.photo.url,
                'profile': user_profile.profile,
                'background_image': user_profile.background_image.url if user_profile.background_image else '',
            })
        except:
            return Response({
            'result': 'system failed, try it later',
        })