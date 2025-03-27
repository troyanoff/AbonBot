def _forward_sides(data: list[dict], right_side: int):
    len_data = len(data)
    left_side = right_side
    if right_side > len_data - 1:
        left_side = 0
    last_index = len_data - 1
    right_side = left_side + 5
    if right_side > last_index:
        right_side = last_index + 1
    return left_side, right_side


def _back_sides(data: list[dict], left_side: int):
    len_data = len(data)
    # last_index = len_data - 1
    if left_side == 0:
        int_pages = (len_data // 5) * 5
        print(int_pages)
        left_side = len_data - 5 if int_pages == len_data else int_pages

        right_side = len_data
        return left_side, right_side
    right_side = left_side
    left_side = right_side - 5
    return left_side, right_side


def create_offset_forward_inline_kb(
    data: list,
    left_side: int
):
    # left_side, right_side = _back_sides(data=data, left_side=left_side)
    # print(left_side, right_side)
    # print(data[left_side: right_side])
    left_side, right_side = _forward_sides(data=data, right_side=left_side)
    print(left_side, right_side)
    print(data[left_side: right_side])


create_offset_forward_inline_kb(list(range(1, 4)), 3)
