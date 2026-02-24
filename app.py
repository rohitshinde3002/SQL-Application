import streamlit as st
import sqlite3
import google.generativeai as genai

# ---------------------- CONFIGURE GEMINI API ----------------------
genai.configure(api_key='API KEY')

# ---------------------- FUNCTION TO QUERY GEMINI ----------------------
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt + "\n" + question)
    return response.text.strip()

# ---------------------- FUNCTION TO RUN SQL QUERY ----------------------
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return f"SQL ERROR: {e}"

# ---------------------- PROMPT FOR GEMINI ----------------------
prompt = """
You are an expert in converting English questions into SQL queries.
The SQL table name is Naresh_it_employee.
Columns are:
 - employee_name
 - employee_role
 - employee_salary
 - employee_address

Rules:
- Only return the SQL query.
- Do NOT include ``` or ‘sql’ in the output.
- Do NOT add explanations.
- Output only pure SQL.
"""

# ---------------------- STREAMLIT UI ----------------------
st.set_page_config(page_title="Gemini SQL Query Generator")
st.header("🔍 GEMINI APP TO CREATE SQL QUERY  AND RUN IT)")

question = st.text_input("Enter your question:")

if st.button("Generate SQL Query & Run"):
    with st.spinner("Generating SQL Query..."):
        sql_query = get_gemini_response(question, prompt)

    st.subheader("🔹 Generated SQL Query")
    st.code(sql_query, language="sql")

    st.subheader("🔹 SQL Output")

    result = read_sql_query(sql_query, "Naresh_it_employee.db")

    if isinstance(result, str):   # error case
        st.error(result)
    else:
        if len(result) == 0:
            st.warning("No results found.")
        else:
            for row in result:
                st.write(row)