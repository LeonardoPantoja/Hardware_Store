from django.contrib.auth.models import User

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            try:
                user = User.objects.get(id=user_id)
                request.user = user
            except User.DoesNotExist:
                pass

        response = self.get_response(request)

        return response