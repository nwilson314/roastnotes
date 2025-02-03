from typing import Any, Callable, TypeVar

from fastapi import APIRouter
from fastapi.types import DecoratedCallable
from sqlmodel import SQLModel


_TSQLModel = TypeVar("_TSQLModel", bound=SQLModel)

class FastApiRouter(APIRouter):
    """
    This solution solves both 307 Temporary Redirect and 405 Method Not Allowed
    https://github.com/tiangolo/fastapi/issues/2060#issuecomment-834868906
    """

    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        add_path = super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )

        alternate_path = path + "/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs
        )

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            add_alternate_path(func)
            return add_path(func)

        return decorator


def update_model(model: _TSQLModel, updates: _TSQLModel) -> None:
    """Update a SQLModel object instance with items in the provided dictionary

    Arguments:
        model: The SQLModel object instance
        new_data: the dict that contains the key, value pairs to add to model

    Returns:
        None: we really on the side effects of this function in terms of setting new attrs on
            input model
    """
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(model, key, value)