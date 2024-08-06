import zlib


def hash_tag(tag: str) -> int:
    return zlib.crc32(tag.encode())
