import streamlit as st
import pandas as pd
import plotly.express as px


def generate_pie_chart(data, title="Shares"):
    fig = px.pie(
        data,
        names="status",
        values="number_of_shares",
        title=title,
    )
    return fig


def main():
    st.title("See SOP 👀")

    # Input fields
    company = st.text_input("Enter company name:")
    number_of_shares = st.number_input("number of shares:", min_value=0)
    start_date = st.date_input("Start date")
    vesting_period = st.number_input("Vesting period (months):", min_value=0)
    vesting_tranche = st.number_input(
        "Enter percentage:", min_value=0.0, max_value=100.0, format="%f"
    )
    today = pd.Timestamp("today")

    # this dataframe will represent one SOP agreement.
    data = pd.DataFrame(
        {
            "status": ["vested", "unvested"],
            "number_of_shares": [50, 50],
        }
    )

    # Submit button
    if st.button("Add Data"):
        pass

    # data = pd.DataFrame(
    #     {
    #         "company": ["company", "company2"],
    #         "number_of_shares": [5, 10],
    #     }
    # )
    # Display pie chart and details
    if "data" in locals():
        st.subheader("Pie Chart:")
        pie_chart = generate_pie_chart(data)
        st.plotly_chart(pie_chart)

        # st.subheader("Details:")
        # st.write(data.describe())


if __name__ == "__main__":
    main()
