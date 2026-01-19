import inject
from rest_framework.exceptions import ValidationError

from evaluations.domain.user.entity import User
from evaluations.usecase.user.query_service import UserQueryService, UserRetrieveModel


class UserUsecase:
    @inject.autoparams()
    def __init__(self, user_query_service: UserQueryService):
        self.user_query_service = user_query_service

    def get_user(self, request_user: User) -> UserRetrieveModel:
        user = self.user_query_service.get_user(request_user)
        if user is None:
            raise ValidationError("ユーザーが存在しません。")
        return user
