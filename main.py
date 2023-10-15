import sys
import os
import datetime

import js

global ROW_COUNT
global ROW_DICT
ROW_COUNT = 0
ROW_DICT = {}


def add_row(row_number):
    # declar id name
    size_id = "size_number_{row}".format(row=row_number)
    value_id = "value_number_{value}".format(value=row_number)
    row_id = "row_number_{value}".format(value=row_number)
    # create layout
    main_layout = js.document.getElementById("main_row")
    row_layout = js.document.createElement("div")
    row_layout.classList.add("row")
    row_layout.classList.add("g-3")
    row_layout.classList.add("mt-3")
    row_layout.id = row_id
    col1_layout = js.document.createElement("div")
    col1_layout.classList.add("col-sm-2")
    col2_layout = js.document.createElement("div")
    col2_layout.classList.add("col")
    col3_layout = js.document.createElement("div")
    col3_layout.classList.add("col")
    label = js.document.createElement("label")
    label.textContent = "สินค้า {row_number}.".format(row_number=row_number)
    input_size = js.document.createElement("input")
    input_size.classList.add("form-control")
    input_size.placeholder = "ปริมาตร, จำนวน"
    input_size.id = size_id
    input_size.setAttribute("type", "number")
    input_value = js.document.createElement("input")
    input_value.classList.add("form-control")
    input_value.placeholder = "ราคา"
    input_value.id = value_id
    input_value.setAttribute("type", "number")
    # adding layout item to main layout
    col1_layout.appendChild(label)
    col2_layout.appendChild(input_size)
    col3_layout.appendChild(input_value)
    row_layout.appendChild(col1_layout)
    row_layout.appendChild(col2_layout)
    row_layout.appendChild(col3_layout)
    main_layout.appendChild(row_layout)

    return {"size_id": size_id, "value_id": value_id, "row_id": row_id}


def do_add_row():
    global ROW_COUNT
    global ROW_DICT
    ROW_COUNT += 1
    result = add_row(ROW_COUNT)
    ROW_DICT[ROW_COUNT] = result
    set_element_value(element_name="output_label", value="")


def do_delete_row():
    global ROW_DICT
    global ROW_COUNT
    if ROW_COUNT <= 2:
        set_element_value(
            element_name="output_label", value="ข้อมูลเปรียบเทียบขั้นต่ำคือสองชุด"
        )
        return
    element = js.document.getElementById(ROW_DICT.get(ROW_COUNT).get("row_id"))
    element.remove()
    del ROW_DICT[ROW_COUNT]
    ROW_COUNT -= 1


def get_element_value(element_name):
    return Element(element_name).value


def set_element_value(element_name, value):
    Element(element_name).write(value)


def do_clear():
    global ROW_DICT
    for row, keys in ROW_DICT.items():
        Element(keys.get("size_id")).clear()
        Element(keys.get("value_id")).clear()
    set_element_value(element_name="output_label", value="")


def do_calculate():
    global ROW_COUNT
    global ROW_DICT
    compute_values = []
    # get value from all active item
    for row, keys in ROW_DICT.items():
        value = get_element_value(keys.get("value_id"))
        size = get_element_value(keys.get("size_id"))
        if not value or not size:
            do_clear()
            set_element_value(
                element_name="output_label", value="กรุณาใส่ข้อมูลให้ครบถ้วน"
            )
            return
        result = float(value) / float(size)
        compute_values.append(result)
    min_value = min(compute_values)

    if len(compute_values) == 2:
        norm_1 = compute_values[0]
        norm_2 = compute_values[1]
        if norm_1 < norm_2:
            discount = norm_2 - norm_1
            discount_percent = (discount / norm_2) * 100
            output_txt = "สินค้า 1. ถูกกว่า {percent}%".format(
                percent=int(discount_percent)
            )
        if norm_1 > norm_2:
            discount = norm_1 - norm_2
            discount_percent = (discount / norm_1) * 100
            output_txt = "สินค้า 2. ถูกกว่า {percent}%".format(
                percent=int(discount_percent)
            )
        if norm_1 == norm_2:
            output_txt = "สินค้าราคาเท่ากัน"
        set_element_value(element_name="output_label", value=output_txt)
    else:
        cheapest_item = []
        for index, value in enumerate(compute_values):
            item = index + 1
            if value == min_value:
                cheapest_item.append(item)
        cheapest_txt = []
        for chp in cheapest_item:
            item_name = "สินค้า {item}.".format(item=chp)
            cheapest_txt.append(item_name)
        if len(cheapest_item) == ROW_COUNT:
            output_txt = "สินค้าทั้งหมด ราคาเท่ากัน"
        else:
            item_list = " และ".join(cheapest_txt)
            output_txt = "{chp} ถูกที่สุด".format(chp=item_list)
        set_element_value(element_name="output_label", value=output_txt)


def main():
    # create default row as 2
    do_add_row()
    do_add_row()


if __name__ == "__main__":
    main()
