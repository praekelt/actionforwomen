from userprofile.backends.simple import SimpleBackend


class MamaBackend(SimpleBackend):
    def register(self, request, **kwargs):
        """
        Create and immediately log in a new user.

        This is a customization of normal userprofile
        backend to remove email field.
        """
        kwargs['email'] = ''
        return super(MamaBackend, self).register(request, **kwargs)
