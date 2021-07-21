import tkinter
from tkinter import *
from tkinter import filedialog
import tkinter as tk

import input_handler
import logging
import os
from functools import partial

logging.basicConfig(level=logging.INFO)

test_case_output = "test_cases\\output"
gui = Tk()
Textbox = tk.Text(gui, height=50, width=70)
Textbox2 = tk.Text(gui, height=50, width=70)
# H=55, W=70 This seems to be the sweet spot on the appearance.
Textbox.pack(side=tk.LEFT, expand=True)
Textbox2.pack(side=tk.RIGHT, expand=True)


def main():
    global case_val

    case_val = "x"

    # GUI
    w, h = gui.winfo_screenwidth(), gui.winfo_screenheight()
    gui.geometry("%dx%d+0+0" % (w, h))

    label_1 = Label(gui, text="Press this button:")
    label_1.config(font=('arial', 10))
    # The labels is going to look weird. After trial and error, it eventually looked 'ok'. -Alex

    # Python doesn't like ".grid" and the TextBox together. It's been comment out. -Alex
    canvas1 = tk.Canvas(gui, width=100, height=60)
    canvas1.pack()
    canvas1.create_window(-50, 30, window=label_1)

    action_with_arg = partial(buttonAction, gui)

    button = Button(gui, text="Save File and then Interpret", command=action_with_arg)
    canvas1.create_window(0, 60, window=button)

    gui.mainloop()


def buttonAction(gui):
    # do something
    input_Value = Textbox.get("1.0", "end-1c")
    print("Text from the textbox: \n" + input_Value)  # This just prints the stuff in the textbox into the console.

    # Dialogue Box to name and save.
    file_save()

    # Read File
    # Note: Use askopenfilenames with a 's' at the end to open multiple files.
    text_file = filedialog.askopenfilename(title=" Select File ",
                                           filetypes=(("Text file", "*.txt*"), ("all files", "*.*")))
    # print("Prints the text_file: \n" + text_file)

    text_file2 = open(text_file, 'r')
    stuff = text_file2.read()
    # print("\nOpened file, before Interpretation: \n" + stuff)

    # Interpret
    interpret_single_file(text_file)
    # print("Print the Translated data: \n" + data)
    output_file_name = "output_" + (text_file[text_file.rindex('/') + 1:])
    output_file_path = test_case_output + "\\" + output_file_name
    with open(output_file_path, "r") as f:
        new_data = f.read()
        # print("Print new_data \n" + new_data)

    Textbox2.delete('1.0', END)
    Textbox2.insert(END, new_data)  # Change "stuff" later
    # print("\nResults after Interpretation: \n" + data)


def file_save():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(Textbox.get(1.0, END))  # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close()

# For GUI use only
def interpret_single_file(file_path):
    is_first_run = True
    indent = 0
    file_data = input_handler.single_file(file_path)
    for line in file_data:
        if line.strip() == "{":
            indent += 1
            continue
        elif line.strip() == "}":
            indent -= 1
            continue

        for token in token_dict.keys():
            if token in line:
                arg = line.replace(token, "")
                arg = arg.strip()

                token_dict[token](arg, indent, False, file_path, is_first_run)
                is_first_run = False


def get_indent(indent_count):
    back_t = ""

    for i in range(indent_count):
        back_t = back_t + "\t"

    return back_t


def remove_argument_types(arg):
    for item in argument_type_list:
        if item in arg:
            return arg.replace(item, "")

    return arg


# ===============================================
# INDIVIDUAL CASES
# ===============================================


def public_class(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + "class " + str(arg) + ":")
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")

    else:
        print(output)


def public_static_void_main(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + 'def main' + str(arg) + ':')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def system_out_println(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + 'print' + str(arg) + '')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def if_stmt(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + 'if' + str(arg) + ':')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def else_stmt(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'else:')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def while_loop(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + 'while' + str(arg) + ':')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def i_plus_plus(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'i += 1')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def int_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


# Sprint 2


def array_list(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    arg = arg.replace("{", "[")
    arg = arg.replace("}", "]")
    output = (indents + "numbers " + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def case(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent - 1)
    arg = remove_argument_types(arg).strip()
    case_case = arg.replace(":", "")
    output = (indents + 'if ' + case_val + ' = ' + str(case_case) + ":")
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def default(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent - 1)
    output = (indents + 'else:')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def break_semicolon(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'break')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def switch(arg, indent, is_output_all, file_path, is_first_run):
    remove_left_par = arg.replace("(", "")
    case_val = remove_left_par.replace(")", "")
    indents = get_indent(indent)
    output = (indents + ' ')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def j_plus_plus(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'j += 1')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def i_minus_minus(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'i -= 1')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def j_minus_minus(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'j -= 1')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def double_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def float_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def byte_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def short_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def long_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def char_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def boolean_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def string_type(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    arg = remove_argument_types(arg)
    output = (indents + str(arg))
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def j_plus_plus(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'j += 1')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def i_minus_minus(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'i -= 1')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)


def j_minus_minus(arg, indent, is_output_all, file_path, is_first_run):
    indents = get_indent(indent)
    output = (indents + 'j -= 1')
    if not is_output_all:
        test_case_name = test_case_output + "\\output_" + (file_path[file_path.rindex('/') + 1:])
        if is_first_run:
            with open(test_case_name, "w") as f:
                f.write(output + "\n")
        else:
            with open(test_case_name, "a") as f:
                f.write(output + "\n")
    else:
        print(output)
# ===============================================
# VALUES
# ===============================================


token_dict = {"public class": public_class,
              "public static void main": public_static_void_main,
              "System.out.println": system_out_println,
              "if": if_stmt,
              "else": else_stmt,
              "i++": i_plus_plus,
              "while": while_loop,
              "int ": int_type,
              "switch": switch,
              "case": case,
              "default": default,
              "String[] numbers": array_list,
              "break": break_semicolon,
              "j--": j_minus_minus,
              "i--": i_minus_minus,
              "j++": j_plus_plus,
              "string ": string_type,
              "String ": string_type,
              "boolean ": boolean_type,
              "char ": char_type,
              "long ": long_type,
              "short ": short_type,
              "byte ": byte_type,
              "float ": float_type,
              "double ": double_type
              }

argument_type_list = ["String[] ", "String ", "int ", "byte ", "short ", "long ", "float ", "double ", "char ",
                      "boolean ", "double "]

main()
