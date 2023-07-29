from typing import Any

from fastapi import FastAPI, Response
from fastapi.responses import FileResponse


class CustomFileResponse(FileResponse):
    def __init__(self, file_content: bytes, json_content: dict, filename: str):
        super().__init__(file_content, filename=filename)
        self.json_content = json_content

    async def __call__(self, scope, receive, send):
        response = Response(self.json_content, media_type="application/json")
        await response(scope, receive, send)
        await super().__call__(scope, receive, send)
# I think this function will return two responses.
# That could be weird.
