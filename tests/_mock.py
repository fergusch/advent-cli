from mock import MagicMock


mock_get_config = MagicMock()
mock_get_config.return_value = {'session_cookie': '',
                                'private_leaderboards': ['1111111'],
                                'disable_color': True}
