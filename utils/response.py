from rest_framework.renderers import JSONRenderer


class custom_renderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if str(renderer_context["response"].status_code).startswith("2"):
                message = getattr(renderer_context["response"], "message", None)
                code = getattr(renderer_context["response"], "code", None)
                ret = {
                    "message": message if message else "SUCCESS",
                    "code": code if code else "000000",
                    "data": data,
                }

                return super().render(ret, accepted_media_type, renderer_context)
            else:
                return super().render(data, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
