from copy import deepcopy
import dao
from ph_types import UnsortedImgType, ParsedImgType
from utils import hash_tag


def prepare_tags_for_prediction(tags: list[str]) -> list[str]:
    # get and hash tags were used for model training
    all_tags = [hash_tag(tag) for tag in dao.get_tags_used_for_training()]
    # hash img tags
    hashed_img_tags = [hash_tag(tag) for tag in tags]
    return [int(tag in hashed_img_tags) for tag in all_tags]


def prepare_unsorted_img(img: ParsedImgType, is_good: bool, likelihood: int) -> UnsortedImgType:
    img = deepcopy(img)
    img["likelihood"] = likelihood
    img["isGood"] = is_good
    return img


if __name__ == "__main__":
    from unittest.mock import patch

    img = {"1": ["tag1", "tag2"]}
    with patch("dao.get_tags_used_for_training", return_value=["tag1", "tag2", "tag3"]):
        assert prepare_tags_for_prediction(img) == [1, 1, 0]
    
    img = {"1": ["tag1", "tag2"]}
    is_good = True
    likelihood = 50
    expected = {"1": ["tag1", "tag2"], "likelihood": 50, "isGood": True}
    assert prepare_unsorted_img(img, is_good, likelihood) == expected
