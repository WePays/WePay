from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def authentication_error(self, request, provider_id, error, exception, extra_context):
        print({'provider_id': provider_id, 'error': error.__str__(), 'exception': exception.__str__(), 'extra_context': extra_context})
        return super().authentication_error(request, provider_id, error, exception, extra_context)
