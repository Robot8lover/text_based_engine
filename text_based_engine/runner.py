from .user_input import get_choice_input
from .parser import parse_file, parse_room_lists, fill_titles

def choices_to_str(choice_list: list) -> str:
    return "\n".join(f"{i+1}. {choice["text"]}" for i, choice in enumerate(choice_list))

def loop(rooms, start_id):
    current_id = start_id
    while True:
        current_room = rooms[current_id]
        room_body = current_room["body"]
        choices = current_room["choices"]
        print(current_room["title"])
        print()
        print(room_body["text"])
        print()
        print(choices_to_str(choices))
        next_index = get_choice_input(len(choices)) - 1
        current_id = choices[next_index]["id"]

def run(game_file_path: str):
    with open(game_file_path, "r") as file:
        header, room_lists = parse_file(file)
        rooms = parse_room_lists(room_lists)
        fill_titles(rooms)
        start_id = header["start"]
        loop(rooms, start_id)
