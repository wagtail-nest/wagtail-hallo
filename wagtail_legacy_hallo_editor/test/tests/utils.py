from django.contrib.auth import get_user_model


class TestUtils:
    @staticmethod
    def create_test_user():
        """
        Override this method to return an instance of your custom user model
        """
        user_model = get_user_model()
        # Create a user
        user_data = dict()
        user_data[user_model.USERNAME_FIELD] = "test@email.com"
        user_data["email"] = "test@email.com"
        user_data["password"] = "password"

        for field in user_model.REQUIRED_FIELDS:
            if field not in user_data:
                user_data[field] = field

        return user_model.objects.create_superuser(**user_data)

    def login(self, user=None, username=None, password="password"):
        # wrapper for self.client.login that works interchangeably for user models
        # with email as the username field; in this case it will use the passed username
        # plus '@example.com'

        user_model = get_user_model()

        if username is None:
            if user is None:
                user = self.create_test_user()

            username = getattr(user, user_model.USERNAME_FIELD)

        if user_model.USERNAME_FIELD == "email" and "@" not in username:
            username = "%s@example.com" % username

        # Login
        self.assertTrue(
            self.client.login(
                password=password, **{user_model.USERNAME_FIELD: username}
            )
        )

        return user
