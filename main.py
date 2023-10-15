import sys
import os
import datetime


def get_element_value(element_name):
    return Element(element_name).value


def set_element_value(element_name, value):
    Element(element_name).write(value)


def do_clear():
    Element("input_1_size").clear()
    Element("input_2_size").clear()
    Element("input_1_price").clear()
    Element("input_2_price").clear()
    set_element_value(element_name="output_label", value="")


def do_calculate():
    # get attribute from web
    input_1_size = get_element_value("input_1_size")
    input_2_size = get_element_value("input_2_size")
    input_1_price = get_element_value("input_1_price")
    input_2_price = get_element_value("input_2_price")

    if not input_1_size or not input_2_size or not input_1_price or not input_2_price:
        do_clear()
        set_element_value(element_name="output_label", value="กรุณาใส่ข้อมูลให้ครบถ้วน")
        return
    input_1_size = int(input_1_size)
    input_2_size = int(input_2_size)
    input_1_price = int(input_1_price)
    input_2_price = int(input_2_price)
    # calculate value
    norm_1 = input_1_price / input_1_size
    norm_2 = input_2_price / input_2_size
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
