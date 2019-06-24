from rest_framework.renderers import JSONRenderer


class MyRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {
            'code': data.pop('code'),
            'data': data
        }

        return super().render(data, accepted_media_type=None, renderer_context=None)
