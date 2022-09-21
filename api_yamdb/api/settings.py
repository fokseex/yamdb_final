from django.utils.translation import get_language

SENDER_EMAIL = 'yambd@example.com'

current_language = get_language()
if get_language() == 'ru-RU':
    SIGNUP_EMAIL_MESSAGE = {
        'theme': 'YaMBD Регистрация на сайте.',
        'message': ('Уважаемый пользователь!\n'
                    'На ваши контактные была произведена регистрация на сайте'
                    ' Yambd. Для получения токена для доступа к сайту'
                    ' используйте данный код:'),
        'sender': SENDER_EMAIL
    }
else:
    SIGNUP_EMAIL_MESSAGE = {
        'theme': 'YaMBD Register on the site.',
        'message': ('Dear user!\n'
                    'Your contacts have been registered on the site'
                    ' Yambd. To get a token to access the site, use'
                    ' given code:'),
        'sender': SENDER_EMAIL
    }
