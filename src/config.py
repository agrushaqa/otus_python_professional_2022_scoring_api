from http import HTTPStatus


class Config:
    def __init__(self):
        self.salt = "Otus"
        self.admin_login = "admin"
        self.admin_salt = "42"
        self.errors = {
            HTTPStatus.BAD_REQUEST: "Bad Request",
            HTTPStatus.FORBIDDEN: "Forbidden",
            HTTPStatus.NOT_FOUND: "Not Found",
            HTTPStatus.UNPROCESSABLE_ENTITY: "Invalid Request",
            HTTPStatus.INTERNAL_SERVER_ERROR: "Internal Server Error",
        }
        self.birthday_delta = 365 * 70

        # UNKNOWN = 0
        # MALE = 1
        # FEMALE = 2
        # GENDERS = {
        #     UNKNOWN: "unknown",
        #     MALE: "male",
        #     FEMALE: "female",
        # }