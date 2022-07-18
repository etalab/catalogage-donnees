import functools
import inspect
from typing import Any, Callable, List, cast

import fastapi.params
from fastapi import Depends, HTTPException
from fastapi.security.base import SecurityBase

from server.domain.auth.entities import UserRole

from ..resources import auth_backend
from ..types import APIRequest


class BasePermission:
    error_msg = "Permission denied"
    status_code = 403

    def has_permission(self, request: APIRequest) -> bool:
        raise NotImplementedError  # pragma: no cover

    def error(self) -> HTTPException:
        return HTTPException(status_code=self.status_code, detail=self.error_msg)

    def __call__(self, request: APIRequest) -> None:
        if not self.has_permission(request):
            raise self.error()

    def __or__(self, other: Any) -> "BasePermission":
        """
        Aithorize requests for which this permission OR the other permission passes.

        Usage:
            PermA() | PermB()
        """
        if not isinstance(other, BasePermission):
            raise NotImplementedError

        this = self

        class OrImpl(BasePermission):
            @_patch_openapi_security_params(this, other)
            def __call__(self, request: APIRequest) -> None:
                assert isinstance(other, BasePermission)
                if this.has_permission(request):
                    return
                if other.has_permission(request):
                    return
                raise other.error()

        return OrImpl()

    def __and__(self, other: Any) -> "BasePermission":
        """
        Authorize requests for which this permission AND the other permission passes.

        Usage:
            PermA() & PermB()
        """
        if not isinstance(other, BasePermission):
            raise NotImplementedError

        this = self

        class AndImpl(BasePermission):
            @_patch_openapi_security_params(this, other)
            def __call__(self, request: APIRequest) -> None:
                this(request)
                other(request)

        return AndImpl()


class IsAuthenticated(BasePermission):
    """
    Require requests to be authenticated.

    Usage:
        @router.get(
            ...,
            dependencies=[
                Depends(IsAuthenticated()),
            ],
        )
    """

    status_code = 401
    error_msg = "Invalid credentials"

    def has_permission(self, request: APIRequest) -> bool:
        return request.user.is_authenticated

    def __call__(
        self,
        request: APIRequest,
        _: SecurityBase = Depends(auth_backend.security),  # For OpenAPI docs.
    ) -> None:
        super().__call__(request)


class HasRole(BasePermission):
    """
    An add-on to `IsAuthenticated()` which requires to authenticated user to
    have specific roles.

    Usage:

        @router.get(
            ...,
            dependencies=[
                Depends(IsAuthenticated() & HasRole(...)),
            ],
        )
    """

    def __init__(self, *roles: UserRole) -> None:
        super().__init__()
        self._roles = roles

    def has_permission(self, request: APIRequest) -> bool:
        if not request.user.is_authenticated:
            raise RuntimeError(
                "Running HasRole but user is not authenticated. "
                "Hint: use IsAuthenticated() & HasRole(...)"
            )

        return request.user.obj.role in self._roles


def _patch_openapi_security_params(*permissions: BasePermission) -> Callable:
    # Make FastAPI register all the security schemes declared in each permission
    # __call__ signature in the generated OpenAPI documentation.
    #
    # FastAPI's DI relies on function signatures, and FastAPI provides no explicit
    # OpenAPI registration utilities, so we manipulate signatures directly.

    def decorate(func: Callable) -> Callable:
        sig = inspect.signature(func)

        # Gather security dependencies in each permission's '__call__' signature.

        securities: List[SecurityBase] = []

        for perm in permissions:
            perm_sig = inspect.signature(perm.__call__)
            for param in perm_sig.parameters.values():
                if not isinstance(param.default, fastapi.params.Depends):
                    continue
                if not isinstance(param.default.dependency, SecurityBase):
                    continue
                security = param.default.dependency
                securities.append(security)

        # Create signature parameters for each security dependency we found.

        extra_params = []

        for security in securities:
            # Choose a name we can easily recognize later on.
            name = f"__security_{security.scheme_name.lower().replace(' ', '_')}"
            assert name.isidentifier(), name
            param = inspect.Parameter(
                name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=Depends(cast(Callable, security)),
            )
            extra_params.append(param)

        # Build the patched signature and assign it.

        patched_sig = inspect.Signature(
            parameters=[*sig.parameters.values(), *extra_params],
            return_annotation=sig.return_annotation,
        )

        @functools.wraps(func)
        def f(*args: Any, **kwargs: Any):  # type: ignore
            # We added Depends parameters to the signature, so FastAPI will resolve them
            # and pass them here. We need to drop them as the real '__call__' won't
            # accept them.
            kwargs = {
                k: v for k, v in kwargs.items() if not k.startswith("__security_")
            }
            return func(*args, **kwargs)

        f.__signature__ = patched_sig  # type: ignore

        return f

    return decorate
