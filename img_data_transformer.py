from copy import deepcopy
import dao
from utils import hash_tag

def prepare_tags_for_prediction(img: dict) -> list[str]:
    # get and hash tags were used for model training
    all_tags = [hash_tag(tag) for tag in dao.get_tags_used_for_training()]
    # get and hash img tags
    img_tags = [hash_tag(tag) for tag in list(img.values())[0]]
    return [int(tag in img_tags) for tag in all_tags]


def prepare_unsorted_img(img: dict, is_good: bool, likelihood: int) -> dict:
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
