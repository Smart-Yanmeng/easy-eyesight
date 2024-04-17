from pydantic import BaseModel


class FaceImgDto(BaseModel):
    # imageByte: bytes
    username: str
    orgId: int
