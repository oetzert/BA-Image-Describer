from pydantic import BaseModel

class DescribeParams(BaseModel):
    temperature: float = 0.2
    max_tokens: int = 400

class DescribeResponse(BaseModel):
    text: str
    model: str
    tokens_in: int | None = None
    tokens_out: int | None = None

class DescribeItemResponse(BaseModel):
    filename: str
    text: str
    model: str
    tokens_in: int | None = None
    tokens_out: int | None = None

class DescribeBatchResponse(BaseModel):
    count: int
    results: list[DescribeItemResponse]
