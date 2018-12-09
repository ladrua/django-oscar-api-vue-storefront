from rest_framework.authtoken.views import ObtainAuthToken
from oscar_vue_api.renderers import CustomJSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomObtainAuthToken(ObtainAuthToken):
    renderer_classes = (CustomJSONRenderer,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(token.key)

obtain_auth_token = CustomObtainAuthToken.as_view()
