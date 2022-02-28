from django.test import TestCase
from requests import post, get


from rest_framework.status import HTTP_204_NO_CONTENT


class UserAuthenticationTest(TestCase):
    URL = "http://localhost:8000/api/persons"
    user_id = None

    def setUp(self) -> None:
        response = post(self.URL + "/login", data={"loginNumber": "99999999", "password": "admin@admin"}).json()
        self.access = response.get('access')
        self.user_id = response.get("userId")

    def test_get_user(self):
        response = get(self.URL + f"/{self.user_id}", headers={'Authorization': f'Bearer {self.access}'}).json()
        print(response)
        self.assertIsNotNone(response.get("name"))

    def test_sign_up(self):
        data = {
            'name': 'triki',
            'loginNumber': '11608168',
            'email': None,
            'telephone': '+21624127616',
            'password': 'omartriki712@+=',
            'typeUser': 'school',
            'localisation': {
                'governorate': 'sfax',
                'delegation': 'afran',
                'zipCode': 3093
            }
        }
        response = post(self.URL + "/signup", json=data)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_create_school(self):
