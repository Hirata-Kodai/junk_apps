import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from calu_emb_and_save import calc_emb_from_df


def main():
    st.title("Ploter of mds scatter")
    with st.form(key="file_upload"):
        uploaded_raw_haiku_file = st.file_uploader("Choose a haiku file")
        uploaded_embed_file = st.file_uploader("Choose a embeded file(.npy)", type="npy")
        submit_button = st.form_submit_button(label="Plot!")
    if submit_button:
        if uploaded_raw_haiku_file and uploaded_embed_file:
            D_transformed_df = pd.DataFrame(np.load(uploaded_embed_file), columns=["dim1", "dim2"])
            haiku_df = pd.read_csv(uploaded_raw_haiku_file)
            haikus = haiku_df['本文']
            source = pd.concat([D_transformed_df, pd.DataFrame(haikus)], axis=1)
            source.columns = ["dim1", "dim2", "haiku"]
            st.write("## Scatter with Hover")
            c = alt.Chart(source).mark_circle(size=60).encode(
                x='dim1',
                y='dim2',
                tooltip=["haiku"])
            st.altair_chart(c)
        elif uploaded_raw_haiku_file:
            st.write("Calclating embedding...")
            haiku_df = pd.read_csv(uploaded_raw_haiku_file)
            D_transformed_df = pd.DataFrame(calc_emb_from_df(haiku_df), columns=["dim1", "dim2"])
            haikus = haiku_df['本文']
            source = pd.concat([D_transformed_df, pd.DataFrame(haikus)], axis=1)
            source.columns = ["dim1", "dim2", "haiku"]
            st.write("## Scatter with Hover")
            c = alt.Chart(source).mark_circle(size=60).encode(
                x='dim1',
                y='dim2',
                tooltip=["haiku"])
            st.altair_chart(c)
        else:
            st.error("Should need a raw haiku file at least.")


if __name__ == '__main__':
    main()
