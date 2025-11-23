def get_choice_input(maximum: int|None = None) -> int:
    """
    Returns the user's desired choice.
    Note that this is 1 indexed (unless we change that in the future).
    maximum is inclusive
    """
    while True:
        inp = input("Enter desired choice: ")
        if not inp:
            print("Please provide a choice selection.")
        elif inp.isdigit():
            i = int(inp)
            if i <= 0:
                print("Please enter a positive number.")
            elif (maximum is not None) and (i > maximum):
                print(f"Choice must be less than or equal to {maximum}.")
            else:
                return i
