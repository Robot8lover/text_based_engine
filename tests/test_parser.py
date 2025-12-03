from text_based_engine.parser import (
    parse_file,
    parse_header,
    parse_choice,
    parse_choices_list,
    parse_room_body_list,
    parse_room_lists,
    fill_titles,
)

def test_fill_titles():
    bar_title = "The _Bar -Room"
    foo_choice_text = "Go over to the foo room"
    room_dict = {
        "foo": {
            "title": "The Foo Room",
            "body": "Welcome to the Foo Room",
            "choices": [{
                "text": None,
                "id": "bar-room",
            }],
        },
        "bar-room": {
            "title": bar_title,
            "body": "This is the bar room!",
            "choices": [{
                "text": foo_choice_text,
                "id": "foo"
            }],
        }
    }
    fill_titles(room_dict)
    assert room_dict["foo"]["choices"][0]["text"] == bar_title
    assert room_dict["foo"]["choices"][0]["id"] == "bar-room"
    assert room_dict["bar-room"]["choices"][0]["text"] == foo_choice_text
    assert room_dict["bar-room"]["choices"][0]["id"] == "foo"
