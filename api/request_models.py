from marshmallow import Schema, fields, post_load


class SummarizeRequestSchema(Schema):
    text = fields.Str(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return SummarizeRequestDto(**data)


class SummarizeRequestDto:
    def __init__(self, text) -> None:
        self.text = text


class ChunkTextRequestSchema(Schema):
    text = fields.Str(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return ChunkTextRequestDto(**data)


class ChunkTextRequestDto:
    def __init__(self, text) -> None:
        self.text = text


class ReadTextRequestSchema(Schema):
    text = fields.Str(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return ChunkTextRequestDto(**data)


class ReadTextRequestDto:
    def __init__(self, text) -> None:
        self.text = text


class QuestionTextRequestSchema(Schema):
    text = fields.Str(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return ChunkTextRequestDto(**data)


class QuestionTextRequestDto:
    def __init__(self, text) -> None:
        self.text = text
