import streamlit as st
import pandas as pd
import plotly.express as px
import datetime


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

    if st.session_state.get("sops") is None:
        st.session_state["sops"] = {}
    sops = st.session_state["sops"]

    # Input fields
    company = st.text_input("Enter company name:")
    number_of_shares = st.number_input("number of shares:", min_value=0)
    start_date = st.date_input("Start date")
    vesting_period = st.number_input("Vesting period (months):", min_value=0)
    vesting_tranche = st.number_input(
        "Enter percentage:", min_value=0.0, max_value=100.0, format="%f"
    )
    today = datetime.date.today()

    # Submit button
    if st.button("Add Data"):
        months = (today - start_date) / pd.Timedelta(days=30)
        vested_shares = number_of_shares * (
            (vesting_tranche / 100) * (months / vesting_period)
        )
        if company not in sops:
            data = pd.DataFrame(
                {
                    "status": ["To be vested", "Vested"],
                    "number_of_shares": [
                        number_of_shares - vested_shares,
                        vested_shares,
                    ],
                }
            )
            sops[company] = [data]
        else:
            data = sops[company][0]
            data.loc[0, "number_of_shares"] = (
                number_of_shares - vested_shares + data.loc[0, "number_of_shares"]
            )

            data.loc[1, "number_of_shares"] = (
                data.loc[1, "number_of_shares"] + vested_shares
            )
            sops[company] = [data]

    for company, data in sops.items():
        data = data[0]
        # Display pie chart and details
        if "data" in locals():
            st.subheader(f"{company}:")
            pie_chart = generate_pie_chart(data)
            st.plotly_chart(pie_chart)


if __name__ == "__main__":
    main()
