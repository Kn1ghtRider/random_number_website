import streamlit as st
import random
import sqlite3


# Function to generate a random number between 1 and 24
def generate_random_number():
    return random.randint(1, 24)


# Function to initialize the database
def init_db():
    conn = sqlite3.connect("chosen_numbers.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS chosen_numbers (number INTEGER)""")
    conn.commit()
    conn.close()


# Function to insert a chosen number into the database
def insert_number(number):
    conn = sqlite3.connect("chosen_numbers.db")
    c = conn.cursor()
    c.execute("INSERT INTO chosen_numbers (number) VALUES (?)", (number,))
    conn.commit()
    conn.close()


# Function to check if a number has already been chosen
def is_number_chosen(number):
    conn = sqlite3.connect("chosen_numbers.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM chosen_numbers WHERE number = ?", (number,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0


# Function to choose a number
def choose_number():
    number = generate_random_number()
    while is_number_chosen(number):
        number = generate_random_number()
    insert_number(number)
    return number


# Function to check if all numbers have been chosen
def all_numbers_chosen():
    return len(get_all_chosen_numbers()) == 24


# Function to get all chosen numbers
def get_all_chosen_numbers():
    conn = sqlite3.connect("chosen_numbers.db")
    c = conn.cursor()
    c.execute("SELECT number FROM chosen_numbers")
    chosen_numbers = [row[0] for row in c.fetchall()]
    conn.close()
    return chosen_numbers


# Main function
def main():
    init_db()
    st.markdown(
        """
        <h1 style='font-family: Sedgwick Ave Display, cursive; '>Random Number Generator</h1>
    """,
        unsafe_allow_html=True,
    )

    st.write("Click the button below to generate a random number between 1 and 24.")

    if all_numbers_chosen():
        st.write("All numbers have been chosen!")
        if st.button("Reset"):
            reset_numbers()
            st.write("Numbers reset. You can now generate random numbers again.")
            st.rerun()
    else:
        if st.button("Generate Random Number"):
            number = choose_number()
            st.write("Random Number:", number)


# Function to reset numbers
def reset_numbers():
    conn = sqlite3.connect("chosen_numbers.db")
    c = conn.cursor()
    c.execute("DELETE FROM chosen_numbers")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
