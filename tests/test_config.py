from local_friend.config import CAPTURE_INTERVAL_SECONDS, MAX_IMAGE_WIDTH


def test_capture_interval_is_positive():
    assert CAPTURE_INTERVAL_SECONDS > 0


def test_max_image_width_is_positive():
    assert MAX_IMAGE_WIDTH > 0