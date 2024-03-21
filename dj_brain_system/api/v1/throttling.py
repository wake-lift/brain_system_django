from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonMinuteThrottle(AnonRateThrottle):
    """Ограничение числа запросов в минуту для анонимного пользователя."""
    scope = 'anon_minute'


class AnonHourThrottle(AnonRateThrottle):
    """Ограничение числа запросов в час для анонимного пользователя."""
    scope = 'anon_hour'


class UserMinuteThrottle(UserRateThrottle):
    """Ограничение числа запросов в минуту для
    аутентифицированного пользователя."""
    scope = 'user_minute'


class UserHourThrottle(UserRateThrottle):
    """Ограничение числа запросов в час для
    аутентифицированного пользователя."""
    scope = 'user_hour'
