from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile
from web.views.utils.ai_config import mask_api_key


class AISettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            return Response(self._build_payload(user_profile))
        except Exception:
            return Response({'result': 'system error'}, status=500)

    def post(self, request):
        try:
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

            api_key = request.data.get('api_key')
            api_base = request.data.get('api_base')

            if api_key is not None:
                user_profile.api_key = api_key.strip()
            if api_base is not None:
                user_profile.api_base = api_base.strip()

            user_profile.save(update_fields=['api_key', 'api_base'])
            return Response(self._build_payload(user_profile))
        except Exception:
            return Response({'result': 'system error'}, status=500)

    def _build_payload(self, user_profile):
        api_key = (user_profile.api_key or '').strip()
        api_base = (user_profile.api_base or '').strip()

        return {
            'result': 'success',
            'api_key_configured': bool(api_key),
            'api_key_masked': mask_api_key(api_key),
            'api_base': api_base,
            'using_default_api_key': not bool(api_key),
            'using_default_api_base': not bool(api_base),
        }
