import time
import subprocess

import streamlit as st

from insert_data import get_data
from create_db import create
from delete_db import delete_rows
from manage_scripts import get_scripts, add_script, delete_script


def print_temp_msg(msg, type):
    temp_msg = st.empty()
    if type=="success":
        temp_msg.success(msg)
    else:
        temp_msg.error(msg)
    time.sleep(2)
    temp_msg.empty() 

def refresh_data():
    delete_rows()
    create()
    print_temp_msg("Refreshing Data. It might take some time.", "success")
    get_data()
    st.write("Data refreshed")

def add(script_name):
    if script_name != "":
        resp = add_script(script_name)
        if resp:
            print_temp_msg(f"'{script_name}' added successfully!", "success")
        elif resp is None:
            print_temp_msg(f"'{script_name}' cannot be added. There might be a problem with the symbol. Check again", "error")
        else:
             print_temp_msg("{} already added".format(script_name), "error")
        st.session_state.add = ""

def delete(script):
    if delete_script(script):
        print_temp_msg(f"'{script}' deleted successfully!", "success")
    else:
        print_temp_msg(f"'{script}' could not be deleted", "error")

def view_scripts():
    scripts = get_scripts()
    for script in scripts:
        col1, col2 = st.columns(2)
        col1.write(script[0])
        col2.button("Delete", key=script[0], on_click=delete, args=(script[0],))

def run():
    subprocess.run(["python3", "main.py"])


create()
st.sidebar.title("Stock Analysis")
refresh_button = st.sidebar.button("Refresh Data", key="Refresh")
scripts_button = st.sidebar.button("Scripts", key="scripts")
run_button = st.sidebar.button("Run", key="run")

add_text = st.sidebar.text_input("Enter Script Name: ", key = "add_textbox", placeholder="code")
add_button = st.sidebar.button("Add", on_click=add_script, args=(add_text,), key="add")

if not scripts_button and not run_button:
    view_scripts()

if refresh_button:
    st.title("Refresh Data")
    refresh_data()

elif scripts_button:
    st.title("Scripts")
    view_scripts()

elif run_button:
    st.title("Program Running")
    run()

new_stock = st.sidebar.text_input("Script to add:", key="add_stock").upper()
st.sidebar.button(label="Add", on_click=add, args=(new_stock,))
