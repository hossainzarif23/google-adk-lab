def find_max(numbers: list[int]) -> int:
    """
    Finds the maximum value in a list of integers.
    Args:
        numbers: A list of integers.
    Returns:
        The maximum integer in the list.
    """
    maximum = 0

    for number in numbers:
        if number > maximum:
            maximum = number

    return maximum
