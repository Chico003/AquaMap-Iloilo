from django.contrib.auth.views import LoginView


class AquaMapLoginView(LoginView):

    template_name = "accounts/login.html"

    redirect_authenticated_user = True

    def get_success_url(self):

        user = self.request.user

        if hasattr(user, "profile"):

            if user.profile.role == "BFAR":

                return "/bfar/"

            if user.profile.role == "MUNICIPAL":

                return "/municipal/"

        return "/dashboard/"