from contextvars import ContextVar

from fastapi import FastAPI

current_app: ContextVar[FastAPI] = ContextVar("current_app")
