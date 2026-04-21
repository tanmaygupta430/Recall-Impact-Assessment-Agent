from decimal import Decimal
import json


def check_inventory_match(session, manufacturer: str, product_keywords: str) -> dict:
    """Query hospital inventory for items from the recalled manufacturer."""
    result = session.sql(
        """
        SELECT
            ITEM_ID,
            ITEM_NAME,
            DEPARTMENT,
            UNITS_ON_HAND,
            UNIT_COST,
            (UNITS_ON_HAND * UNIT_COST) AS TOTAL_EXPOSURE
        FROM RECALL_AGENT_DB.SUPPLY_CHAIN.HOSPITAL_INVENTORY
        WHERE UPPER(MANUFACTURER) LIKE UPPER('%' || ? || '%')
        """,
        params=[manufacturer],
    ).collect()

    if result:
        items = []
        for row in result:
            d = row.as_dict()
            items.append(
                {k: float(v) if isinstance(v, Decimal) else v for k, v in d.items()}
            )
        return {
            "affected": True,
            "items": items,
            "total_financial_exposure": sum(
                item["TOTAL_EXPOSURE"] for item in items
            ),
        }
    return {"affected": False, "items": [], "total_financial_exposure": 0}


def run_recall_agent(session, recall_number: str) -> str:
    """Fetch the recall, cross-reference inventory, and generate an AI assessment."""
    recall = (
        session.sql(
            "SELECT * FROM RECALL_AGENT_DB.SUPPLY_CHAIN.FDA_RECALLS "
            "WHERE RECALL_NUMBER = ?",
            params=[recall_number],
        )
        .collect()[0]
        .as_dict()
    )

    inventory_impact = check_inventory_match(
        session,
        manufacturer=recall["RECALLING_FIRM"],
        product_keywords=recall["PRODUCT_DESCRIPTION"],
    )

    context = f"""
    RECALL INFORMATION:
    - Recall Number: {recall['RECALL_NUMBER']}
    - Product: {recall['PRODUCT_DESCRIPTION']}
    - Reason: {recall['REASON_FOR_RECALL']}
    - Firm: {recall['RECALLING_FIRM']}
    - Classification: {recall['CLASSIFICATION']}
    - Date: {recall['EVENT_DATE_INITIATED']}

    INVENTORY IMPACT:
    - Affected: {inventory_impact['affected']}
    - Items Found: {json.dumps(inventory_impact['items'], indent=2)}
    - Total Financial Exposure: ${inventory_impact['total_financial_exposure']:,.2f}
    """

    prompt = f"""
    You are a healthcare supply chain analyst.
    Based on the following recall and inventory data, produce:

    1. A 2-sentence executive summary of the recall risk
    2. A bullet list of affected departments and units
    3. Total financial exposure
    4. Three immediate action steps for the supply chain team
    5. A draft email subject line and first paragraph to notify department heads

    {context}

    Be specific, concise, and use a professional tone appropriate
    for hospital operations.
    """

    response = (
        session.sql(
            "SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', ?) AS result",
            params=[prompt],
        )
        .collect()[0]["RESULT"]
    )
    return response
