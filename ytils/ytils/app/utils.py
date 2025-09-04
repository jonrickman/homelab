def _find_substring(input_str: str, substring: str) -> str:
    index = input_str.find(substring)
    if index != -1:
        return input_str[index + len(substring):]
    return

def extract_video_id(input_str: str)-> str:
    """
    Examples can include a wide array such as the following:

    https://www.youtube.com/watch?v=fLxQtcrzTlA
    youtu.be/fLxQtcrzTlA
    fLxQtcrzTlA
    """
    substrings = ["/watch?v=", "youtu.be/"]

    for substring in substrings:
        video_id = _find_substring(input_str, substring)
        if video_id:
            return video_id

    return input_str


if __name__ == "__main__":
    expected_video_id = "fLxQtcrzTlA"
    assert extract_video_id("https://www.youtube.com/watch?v=fLxQtcrzTlA") == expected_video_id
    assert extract_video_id("youtube.com/watch?v=fLxQtcrzTlA") == expected_video_id
    assert extract_video_id("youtu.be/fLxQtcrzTlA") == expected_video_id
    assert extract_video_id("fLxQtcrzTlA") == expected_video_id
