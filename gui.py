import time
import subprocess

import streamlit as st

from auth import generate
from insert_data import get_data
from create_db import create
from delete_db import delete_db
from manage_scripts import get_scripts, add_script, delete_script


def print_temp_msg(msg, type):
    temp_msg = st.empty()
    if type=="success":
        temp_msg.success(msg)
    else:
        temp_msg.error(msg)
    time.sleep(2)
    temp_msg.empty() 

# def authenticate():
#     st.write("Go to https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id=d5b31ac9-5c6b-421b-b2fd-6b738f66764d&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000")
#     st.write("Login and a new page will open with an error. In the url, copy everything after code=")
#     st.write("Enter it here and click Generate.")
#     code = st.text_input("Enter Code Here: ", key = "code", placeholder="code")
#     st.write(code)
    # st.button("Generate", on_click=generate, args=(code,), key="generate")

def refresh_data():
    delete_db()
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


st.sidebar.title("Stock Analysis")
st.write("Go to https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id=d5b31ac9-5c6b-421b-b2fd-6b738f66764d&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000")
st.write("Login and a new page will open with an error. In the url, copy everything after code=")
st.write("Enter it here and click Generate.")
code = st.text_input("Enter Code Here: ", key = "code", placeholder="code")
st.button("Generate", on_click=generate, args=(code,), key="generate")
# Sidebar buttons
# auth_button = st.sidebar.button("Authenticate", key="Auth")
refresh_button = st.sidebar.button("Refresh Data", key="Refresh")
scripts_button = st.sidebar.button("Scripts", key="scripts")
run_button = st.sidebar.button("Run", key="run")

if not refresh_button and not scripts_button and not run_button:
    view_scripts()

# # Handle button clicks
# if auth_button:
#     st.title("Authentication")
#     authenticate()

if refresh_button:
    st.title("Refresh Data")
    refresh_data()

elif scripts_button:
    st.title("Scripts")
    view_scripts()

elif run_button:
    st.title("Program Running")
    run()

new_stock = st.sidebar.text_input("Script to add:", key="add").upper()
st.sidebar.button(label="Add", on_click=add, args=(new_stock,))
