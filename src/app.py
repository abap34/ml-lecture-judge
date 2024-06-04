import streamlit as st
from celery.result import AsyncResult
from tasks import evaluate_code_in_docker

st.title("ml-lecture-evaluation")
user_code = st.text_area("Input your code here", height=20)

if st.button("submit"):
    task = evaluate_code_in_docker.delay(user_code)
    st.write("タスクID:", task.id)

    # 結果をポーリングして表示
    result = AsyncResult(task.id)
    while not result.ready():
        st.write("waiting...")

    output = result.get()

    if output['status'] == 'success':
        st.write("Success!", output['result'])
    else:
        st.write("エラー:", output['error'])
        st.write(output.get('traceback', ''))
