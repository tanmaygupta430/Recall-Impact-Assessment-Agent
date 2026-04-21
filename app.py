import streamlit as st
from snowflake.snowpark.context import get_active_session
from agent import check_inventory_match, run_recall_agent

session = get_active_session()

st.title("Recall Impact Assessment Agent")
st.caption("Powered by Snowflake Cortex")

st.session_state.setdefault("run_assessment", False)


def on_input_change():
    st.session_state.run_assessment = True


recall_input = st.text_input(
    "Enter FDA Recall Number or describe a product:",
    placeholder="e.g., Z-0004-2020 or 'Medtronic cardiac catheter'",
    key="recall_input",
    on_change=on_input_change,
)

if st.button("Assess Impact"):
    st.session_state.run_assessment = True

if st.session_state.run_assessment:
    st.session_state.run_assessment = False
    if not recall_input.strip():
        st.error("Please enter a recall number.")
    else:
        recall_rows = session.sql(
            "SELECT * FROM RECALL_AGENT_DB.SUPPLY_CHAIN.FDA_RECALLS "
            "WHERE RECALL_NUMBER = ?",
            params=[recall_input],
        ).collect()

        if not recall_rows:
            st.error(
                f"No recall found matching '{recall_input}'. "
                "Please check the recall number and try again."
            )
        else:
            with st.spinner("Agent is analyzing recall impact..."):
                result = run_recall_agent(session, recall_input)

                st.success("Assessment Complete")
                st.markdown(result)

                st.subheader("Affected Inventory Items")
                recall = recall_rows[0].as_dict()
                impact_data = check_inventory_match(
                    session, recall["RECALLING_FIRM"], recall["PRODUCT_DESCRIPTION"]
                )
                if impact_data["affected"]:
                    st.dataframe(impact_data["items"])
                    st.metric(
                        "Total Financial Exposure",
                        f"${impact_data['total_financial_exposure']:,.2f}",
                    )
                else:
                    st.info("No matching inventory items found.")
