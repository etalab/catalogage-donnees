from server.application.auth.commands import CreateUser, DeleteUser
from server.application.auth.handlers import (
    create_user,
    delete_user,
    get_user_by_api_token,
    get_user_by_email,
    login,
)
from server.application.auth.queries import GetUserByAPIToken, GetUserByEmail, Login
from server.seedwork.application.modules import Module


class AuthModule(Module):
    command_handlers = {
        CreateUser: create_user,
        DeleteUser: delete_user,
    }

    query_handlers = {
        Login: login,
        GetUserByEmail: get_user_by_email,
        GetUserByAPIToken: get_user_by_api_token,
    }
