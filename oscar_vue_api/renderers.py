from rest_framework import renderers
from rest_framework import status

class CustomJSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}
        response_data['code'] = renderer_context['response'].status_code
        response_data['result'] = data
        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
        return response
