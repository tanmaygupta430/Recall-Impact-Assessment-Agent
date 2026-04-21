-- =============================================================
-- Recall Impact Assessment Agent - Snowflake Setup
-- =============================================================
-- This script creates the database, schema, tables, and file
-- format needed for the Recall Impact Assessment Streamlit app.
-- =============================================================

-- 1. Database and Schema
CREATE DATABASE IF NOT EXISTS RECALL_AGENT_DB;
CREATE SCHEMA IF NOT EXISTS RECALL_AGENT_DB.SUPPLY_CHAIN;

USE SCHEMA RECALL_AGENT_DB.SUPPLY_CHAIN;

-- 2. Hospital Inventory Table
CREATE TABLE IF NOT EXISTS HOSPITAL_INVENTORY (
    ITEM_ID        VARCHAR,
    ITEM_NAME      VARCHAR,
    MANUFACTURER   VARCHAR,
    PRODUCT_CODE   VARCHAR,
    DEPARTMENT     VARCHAR,
    UNITS_ON_HAND  NUMBER(38,0),
    UNIT_COST      NUMBER(12,2)
);

-- 3. FDA Recalls Table
CREATE TABLE IF NOT EXISTS FDA_RECALLS (
    RECALL_NUMBER        VARCHAR,
    PRODUCT_DESCRIPTION  VARCHAR,
    REASON_FOR_RECALL    VARCHAR,
    RECALLING_FIRM       VARCHAR,
    CLASSIFICATION       VARCHAR,
    EVENT_DATE_INITIATED VARCHAR,
    STATUS               VARCHAR,
    PRODUCT_TYPE         VARCHAR,
    PRODUCT_CODE         VARCHAR
);

-- 4. Raw Device Recalls Staging Table (for JSON ingestion)
CREATE TABLE IF NOT EXISTS FDA_DEVICE_RECALLS_RAW (
    RAW_DATA VARIANT
);

-- 5. File Format for CSV Loading
CREATE FILE FORMAT IF NOT EXISTS CSV_LOAD_FORMAT
    TYPE = CSV
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('', 'NULL');

-- 6. Internal Stage for Data Loading
CREATE STAGE IF NOT EXISTS DATA_STAGE
    FILE_FORMAT = CSV_LOAD_FORMAT;

-- 7. Load sample inventory data
-- Upload the CSV first:
--   PUT file://data/sample_inventory.csv @DATA_STAGE AUTO_COMPRESS=FALSE;
--
-- Then copy into the table:
--   COPY INTO HOSPITAL_INVENTORY
--     FROM @DATA_STAGE/sample_inventory.csv
--     FILE_FORMAT = CSV_LOAD_FORMAT
--     ON_ERROR = 'CONTINUE';

-- 8. Streamlit Stage
CREATE STAGE IF NOT EXISTS STREAMLIT_STAGE;

-- 9. Deploy the Streamlit App
-- Upload files first:
--   PUT file://app.py @STREAMLIT_STAGE/streamlit_app.py AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--   PUT file://agent.py @STREAMLIT_STAGE/agent.py AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
--
-- Then create the Streamlit:
--   CREATE STREAMLIT IF NOT EXISTS RECALL_IMPACT_APP
--     ROOT_LOCATION  = '@RECALL_AGENT_DB.SUPPLY_CHAIN.STREAMLIT_STAGE'
--     MAIN_FILE      = 'streamlit_app.py'
--     QUERY_WAREHOUSE = COMPUTE_WH
--     TITLE           = 'Recall Impact Assessment Agent';
