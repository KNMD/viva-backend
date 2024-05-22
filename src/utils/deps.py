from fastapi import Header

from schemas.core import Consumer


def get_consumer(authorization: str = Header(None)) -> Consumer:
    return Consumer(id="1", name="test", tenant="01")