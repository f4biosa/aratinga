from contextvars import ContextVar

_current_theme: ContextVar = ContextVar("aratinga_theme", default=None)


def set_theme(theme) -> None:
    _current_theme.set(theme)


def get_theme():
    return _current_theme.get()
