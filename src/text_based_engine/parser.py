import re
import typing

def parse_file(file: typing.TextIO) -> tuple[dict, list]:
    """
    Splits a file into room text arrays.
    """
    rooms = []
    current_room = []
    has_content = False
    for line in file:
        stripped_line = line.strip()
        if stripped_line == "---":
            if has_content:
                rooms.append(current_room)
            current_room = []
            has_content = False
        else:
            current_room.append(line)
            if not has_content and stripped_line:
                has_content = True
    if has_content:
        rooms.append(current_room)
    return parse_header(rooms[0]), rooms[1:]

def parse_header(header: list[str]) -> dict[str, str]:
    header_dict = {}
    for line in header:
        split = line.split(":", 1) # consider using regex
        if len(split) > 1:
            header_dict[split[0]] = split[1]
    return header_dict

def parse_choice(choice: str) -> dict[str, str|None]:
    # Test if it is [text](#id) or (#id)
    # If the latter, text is the title of the room
    # Except that requires later knowledge hmmm.
    # So maybe we should make a later pass
    text_pattern = r"\[([\w ()[\]-]*)\]\(#([\w-]*)\)"
    id_pattern = r"\(#([\w-]*)\)"
    choice = choice.strip()
    id_match = re.match(id_pattern, choice)
    choice_dict: dict[str, str | None] = {
        "text": None,
        "id": None,
    }
    if id_match:
        choice_dict["id"] = id_match.group(1)
    else:
        text_match = re.match(text_pattern, choice)
        if text_match:
            choice_dict["text"], choice_dict["id"] = text_match.group(1, 2)
            # or .groups()
        else:
            raise ValueError(f"Choice `{choice}` did not match expected patterns.")
    return choice_dict

def parse_choices_list(choices_list: list[str]) -> list[dict[str, str|None]]:
    choices = []
    pattern = r"\d+\.\s+"
    for line in choices_list:
        split = re.split(pattern, line)
        if len(split) == 1:
            # Reached extra line after choices
            # For now, we assume that this line must be unimportant (empty)
            break
        # We do not check for proper numbering
        choices.append(parse_choice(split[1]))
    return choices

def parse_room_body_list(room_body_list: list[str]) \
        -> tuple[str, list[dict[str, str | None]]]:
    pattern = r"\d+\.\s+"
    for i, line in enumerate(room_body_list):
        if re.match(pattern, line):
            return "\n".join(room_body_list[:i]), parse_choices_list(room_body_list[i:])
    return "\n".join(room_body_list), parse_choices_list([])

def parse_room_lists(room_lists: list[list[str]]) -> dict[str, dict]:
    rooms = {}
    for current_room in room_lists:
        title = current_room[0].strip()
        room_id = current_room[1].strip()
        if room_id[0] == "#":
            # otherwise, we don't have an id maybe
            # depending on our choices
            # and then maybe we should assign it?
            room_id = room_id[1:].strip() # or just lstrip
        room_body, room_choices = parse_room_body_list(current_room[2:])
        if room_id in rooms:
            raise ValueError(f"Room id {room_id} is not unique")
        else:
            rooms[room_id] = {
                "title": title,
                "body": room_body,
                "choices": room_choices,
            }
    return rooms

def fill_titles(room_dict: dict[str, dict]):
    """
    Modifies the names of rooms in the choices.
    """
    for room in room_dict.values():
        for i, choice in enumerate(room["choices"]):
            if choice["text"] is None:
                choice["text"] = room_dict[choice["id"]]["title"]
