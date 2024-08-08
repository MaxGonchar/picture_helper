import zlib


def hash_tag(tag: str) -> int:
    return zlib.crc32(tag.encode())

def get_img_id(img: dict) -> str:
    for key in img.keys():
        if key.isnumeric():
            return key

def generate_file_name(id_: int) -> str:
    start = (id_ // 10000) * 10000
    end = start + 9999
    return f"imgs-{start}-{end}.json"
