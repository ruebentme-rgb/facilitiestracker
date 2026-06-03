"""
APRIL Bilateral Facilities Register
=====================================
Streamlit app — Banking Facilities Overview across HK, SG & UAE
As at 02 June 2026

Deploy to Streamlit Cloud:
  1. Push this file to a GitHub repo as  app.py  (or any name)
  2. Go to https://share.streamlit.io  → New app → select repo/file
  3. Click Deploy

Run locally:
  pip install streamlit pandas
  streamlit run april_bilateral_facilities.py
"""

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="APRIL Bilateral Facilities Register",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    /* Hide default Streamlit header padding */
    .block-container { padding-top: 0rem; }

    /* App header banner */
    .app-header {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 50%, #1565c0 100%);
        color: white;
        padding: 28px 40px;
        text-align: center;
        border-radius: 0 0 8px 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .app-header h1 { font-size: 2em; font-weight: 700; letter-spacing: 1px; margin: 0 0 4px 0; }
    .app-header p  { font-size: 1em; opacity: 0.85; font-weight: 300; margin: 0; }

    /* Stat cards */
    .stat-row { display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; margin-bottom: 20px; }
    .stat-card {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border-left: 4px solid #1565c0;
        border-radius: 10px;
        padding: 14px 28px;
        text-align: center;
        min-width: 160px;
    }
    .stat-card.expired {
        background: linear-gradient(135deg, #ffebee, #ffcdd2);
        border-left-color: #c62828;
    }
    .stat-card .num { font-size: 1.8em; font-weight: 700; color: #0d47a1; }
    .stat-card.expired .num { color: #c62828; }
    .stat-card .lbl { font-size: 0.78em; color: #546e7a; text-transform: uppercase; letter-spacing: 1px; }

    /* Guarantor summary */
    .g-summary {
        background: #fff8e1;
        border-left: 4px solid #f9a825;
        border-radius: 8px;
        padding: 16px 22px;
        margin-bottom: 16px;
    }
    .g-summary h4 { color: #e65100; margin: 0 0 8px 0; }

    /* Table */
    .fac-table { width: 100%; border-collapse: collapse; font-size: 0.86em; }
    .fac-table thead th {
        background: linear-gradient(135deg, #1a237e, #1565c0);
        color: white;
        padding: 11px 12px;
        text-align: left;
        font-size: 0.80em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    .fac-table tbody td { padding: 9px 12px; border-bottom: 1px solid #eceff1; vertical-align: top; }
    .fac-table tbody tr:nth-child(even) td { background: #f8f9fb; }
    .fac-table tbody tr.expired-row td { background: #fff3f3 !important; }

    /* Badges */
    .badge-loc {
        display: inline-block; padding: 2px 10px; border-radius: 10px;
        font-size: 0.78em; font-weight: 600; color: white;
    }
    .badge-HK  { background: #2e7d32; }
    .badge-SG  { background: #1565c0; }
    .badge-UAE { background: #6a1b9a; }
    .badge-expired {
        display: inline-block; background: #c62828; color: white;
        padding: 2px 8px; border-radius: 10px; font-size: 0.75em; font-weight: 700;
        margin-left: 4px;
    }

    /* Footer */
    .footer { text-align: center; padding: 20px; color: #90a4ae; font-size: 0.82em; margin-top: 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

RAW_DATA = [
    {"bankName":"Bank of China (Hong Kong) Limited","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"11/09/2018 amended on 20/03/2024","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 11/09/18","guarantorList":["APRIHL"]},
    {"bankName":"Bank of China (Hong Kong) Limited","location":"HK","borrower":"AFPT","borrowerList":["AFPT"],"dateOfFacility":"26/11/2024","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Bank of China (Hong Kong) Limited","location":"HK","borrower":"AIE, AFPT, IWC, ASHK, ASCH","borrowerList":["AIE","AFPT","IWC","ASHK","ASCH"],"dateOfFacility":"28/05/2025","currency":"USD","quantum":"85,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Bank of China, Macau branch","location":"HK","borrower":"ICL","borrowerList":["ICL"],"dateOfFacility":"01/03/2024","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Bank of China, Macau branch","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"01/04/2025","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Bank of Communications, HK","location":"HK","borrower":"IWC","borrowerList":["IWC"],"dateOfFacility":"3/10/16, amended on 8/12/17, 1/3/19, 10/1/20, 22/3/23","currency":"USD","quantum":"70,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 13/10/16","guarantorList":["APRIL"]},
    {"bankName":"Bank of East Asia, HK","location":"HK","borrower":"ASCH, ASHK","borrowerList":["ASCH","ASHK"],"dateOfFacility":"25/11/2024","currency":"USD","quantum":"18,000,000 / 2,000,000","facilityType":"Trade Finance, Derivatives","facilityTypeList":["Trade Finance","Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 20/05/2024","guarantorList":["APRIL"]},
    {"bankName":"Bank Sinopac, HK","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"Negotiating","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Negotiating","securityPackage":"Negotiating","guarantorList":[]},
    {"bankName":"Cathay United Bank","location":"HK","borrower":"ASHK, AIE","borrowerList":["ASHK","AIE"],"dateOfFacility":"09/09/2025","currency":"USD","quantum":"15,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 09/09/25","guarantorList":["APRIL"]},
    {"bankName":"Cathay United Bank","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"03/10/2025","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 3/10/25","guarantorList":["APRIL"]},
    {"bankName":"Changhwa Commercial Bank","location":"HK","borrower":"AFPT","borrowerList":["AFPT"],"dateOfFacility":"27/8/2024 amended on 29/07/25","currency":"USD","quantum":"30,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"30/06/2025","tenureExpired":True,"status":"Current","securityPackage":"APRIHL Guarantee dd 03/09/24","guarantorList":["APRIHL"]},
    {"bankName":"China CITIC Bank International Limited","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"16/7/2020, amended on 26/06/23","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 16/07/20","guarantorList":["APRIHL"]},
    {"bankName":"China CITIC Bank International Limited","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"07/12/2017","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 21/07/21","guarantorList":["APRIL"]},
    {"bankName":"China CITIC Bank International Limited","location":"HK","borrower":"ASHK, IWC, ASCH, AIE, GGTMCO AFEM, AFPT","borrowerList":["ASHK","IWC","ASCH","AIE","GGTMCO AFEM","AFPT"],"dateOfFacility":"12/6/2021 / ISDA dd 16/07/2020 amended on 26/06/2023","currency":"USD","quantum":"80,000,000","facilityType":"Trade Finance, Derivatives","facilityTypeList":["Trade Finance","Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Negotiating","securityPackage":"APRIL Guarantee dd 26/04/21; APRIHL Guarantee dd 16/07/20","guarantorList":["APRIHL","APRIL"]},
    {"bankName":"China Minsheng Banking Corp","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"29/11/2022","currency":"USD","quantum":"57,000,000","facilityType":"Trade Finance, Derivatives","facilityTypeList":["Trade Finance","Derivatives"],"tenure":"5 years","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Dah Sing Bank","location":"HK","borrower":"ASHK, ASCH","borrowerList":["ASHK","ASCH"],"dateOfFacility":"21/11/2018, amended on 29/07/19, 20/03/24","currency":"USD","quantum":"20,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 14/12/18","guarantorList":["APRIL"]},
    {"bankName":"E-Sun Bank","location":"HK","borrower":"ASHK","borrowerList":["ASHK"],"dateOfFacility":"02/04/2024","currency":"USD","quantum":"25,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 24/10/18","guarantorList":["APRIL"]},
    {"bankName":"E-Sun Bank","location":"HK","borrower":"AFPT","borrowerList":["AFPT"],"dateOfFacility":"24/3/2024 amended on 27/06/25","currency":"USD","quantum":"25,000,000","facilityType":"Trade Finance, Derivatives","facilityTypeList":["Trade Finance","Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 24/07/24; DFF Guarantee dd 24/07/24","guarantorList":["APRIHL","DFF"]},
    {"bankName":"Fubon Bank","location":"HK","borrower":"AIE, AFPT, IWC","borrowerList":["AIE","AFPT","IWC"],"dateOfFacility":"26/07/22 amended on 28/2/2025","currency":"USD","quantum":"50,000,000 / 20,000,000","facilityType":"Trade Finance, Derivatives","facilityTypeList":["Trade Finance","Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 28/03/25; APRIHL Guarantee dd 28/03/25","guarantorList":["APRIHL","APRIL"]},
    {"bankName":"Goldman Sachs International","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"03/05/2018","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"N/A","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 19/02/18","guarantorList":["APRIL"]},
    {"bankName":"Habib Bank Zurich (Hong Kong) Limited","location":"HK","borrower":"AFT","borrowerList":["AFT"],"dateOfFacility":"28/6/2022 amended on 07/05/25","currency":"USD","quantum":"7,640,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"PVHL Guarantee dd 28/02/22","guarantorList":["PVHL"]},
    {"bankName":"ICBC (Asia) Limited, Hong Kong","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"05/03/2019","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 05/03/19","guarantorList":["APRIL"]},
    {"bankName":"ICBC (Asia) Limited, Hong Kong","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"04/04/2022","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"24/11/2024","tenureExpired":True,"status":"Current","securityPackage":"APRIL Guarantee dd 04/04/22","guarantorList":["APRIL"]},
    {"bankName":"ICBC (Asia) Limited, Hong Kong","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"11/05/2021","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC (Asia) Limited, Hong Kong","location":"HK","borrower":"AIE, ASHK, GGTMCO","borrowerList":["AIE","ASHK","GGTMCO"],"dateOfFacility":"Negotiating","currency":"USD","quantum":"50,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Negotiating","securityPackage":"APRIL Guarantee dd 23/11/21","guarantorList":["APRIL"]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"09/02/2023","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"06/03/2024","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"5 years","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"29/05/2025","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"ASHK","borrowerList":["ASHK"],"dateOfFacility":"18/08/2022","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"ASHK","borrowerList":["ASHK"],"dateOfFacility":"09/05/2025","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"AFEM","borrowerList":["AFEM"],"dateOfFacility":"18/08/2022","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"AFEM","borrowerList":["AFEM"],"dateOfFacility":"29/05/2025","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"AFPT","borrowerList":["AFPT"],"dateOfFacility":"Negotiating","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Negotiating","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICBC, Jiangmen Xinhui","location":"HK","borrower":"AFPT","borrowerList":["AFPT"],"dateOfFacility":"Negotiating","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"10 years","tenureExpired":False,"status":"Negotiating","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"ICICI Bank Limited","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"06/12/2017","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 06/12/17","guarantorList":["APRIL"]},
    {"bankName":"Industrial Bank Co., Ltd","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"01/07/2025","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Intesa Sanpaolo, Hong Kong","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"11/12/2018 amended on 21/01/22","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"SGF Guarantee dd 01/10/24; APRIHL Guarantee dd 01/10/24","guarantorList":["APRIHL","SGF"]},
    {"bankName":"Intesa Sanpaolo, Hong Kong","location":"HK","borrower":"ASCH, ASHK, IWC, AFPT, AIE","borrowerList":["ASCH","ASHK","IWC","AFPT","AIE"],"dateOfFacility":"10/12/2021, amended on 2/3/2022, further amended on 5/7/2022, renewed 10/10/2024","currency":"USD","quantum":"50,000,000","facilityType":"Trade Finance, Derivatives","facilityTypeList":["Trade Finance","Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 09/07/22","guarantorList":["APRIL"]},
    {"bankName":"Intesa Sanpaolo, Hong Kong","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"11/08/2015, amended on 26/06/2020","currency":"EUR","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 25/08/25","guarantorList":["APRIL"]},
    {"bankName":"Intesa Sanpaolo, Hong Kong","location":"HK","borrower":"AFPT","borrowerList":["AFPT"],"dateOfFacility":"21/08/2020","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Clean","guarantorList":[]},
    {"bankName":"Maybank, Hong Kong","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"23/7/2020, novated on 26/06/2023, further amended on 05/03/2024","currency":"USD","quantum":"5,000,000","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 14/11/19","guarantorList":["APRIL"]},
    {"bankName":"Maybank, Hong Kong","location":"HK","borrower":"AIE, APRIL","borrowerList":["AIE","APRIL"],"dateOfFacility":"28/10/2019, amended on 26/05/2020, 27/06/2023","currency":"USD","quantum":"30,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 14/11/19","guarantorList":["APRIL"]},
    {"bankName":"Maybank, Hong Kong","location":"HK","borrower":"ASHK","borrowerList":["ASHK"],"dateOfFacility":"28/10/2019, amended on 26/05/2020, 21/06/2023, 02/01/2024, 22/02/2024 and 22/09/2025","currency":"USD","quantum":"20,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 14/11/19","guarantorList":["APRIL"]},
    {"bankName":"MUFG, Singapore","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"Negotiating","currency":"USD","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Negotiating","securityPackage":"APRIL Guarantee","guarantorList":["APRIL"]},
    {"bankName":"Nanyang Commercial Bank","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"03/05/2023","currency":"USD","quantum":"11,150,000","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Shanghai PuDong Development Bank, SG","location":"HK","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"13/01/2023","currency":"USD","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIL Guarantee dd 04/01/23","guarantorList":["APRIL"]},
    {"bankName":"Taishin International Bank, Hong Kong","location":"HK","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"31/1/2024 (ISDA dd 20/12/2018, amended on 01/03/24, 07/04/25)","currency":"USD","quantum":"80,000,000","facilityType":"Trade Finance, Derivatives","facilityTypeList":["Trade Finance","Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL + SGF Guarantee dd 23/01/25","guarantorList":["APRIHL","SGF"]},
    # --- SG ---
    {"bankName":"Arab Banking Corporation","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"20/12/2024","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 20/12/24","guarantorList":["APRIHL"]},
    {"bankName":"Arab Banking Corporation","location":"SG","borrower":"AIE, AFPT","borrowerList":["AIE","AFPT"],"dateOfFacility":"Negotiating","currency":"USD","quantum":"10,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Negotiating","tenureExpired":False,"status":"Negotiating","securityPackage":"APRIL Guarantee","guarantorList":["APRIL"]},
    {"bankName":"BBVA, SG","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"22/04/2026","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 22/05/26","guarantorList":["APRIHL"]},
    {"bankName":"Bank of East Asia","location":"SG","borrower":"ASCH","borrowerList":["ASCH"],"dateOfFacility":"17/01/2023","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Barclays Bank plc","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"14/03/2019, amended on 14/10/24","currency":"USD","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 20/12/19","guarantorList":["APRIHL"]},
    {"bankName":"BNP Paribas","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"30/03/2026","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 30/03/26","guarantorList":["APRIHL"]},
    {"bankName":"China Construction Bank","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"04/02/2025","currency":"N/A","quantum":"N/A","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"Nil","guarantorList":[]},
    {"bankName":"Deutsche Bank","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"11/06/2024","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 11/06/2024","guarantorList":["APRIHL"]},
    {"bankName":"DZ Bank AG, Singapore Branch","location":"SG","borrower":"APRIL, AFPT, APPT, AFEM","borrowerList":["APRIL","AFPT","APPT","AFEM"],"dateOfFacility":"21/04/2025","currency":"USD","quantum":"40,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 28/05/25; SGF Guarantee dd 28/05/25","guarantorList":["APRIHL","SGF"]},
    {"bankName":"Emirates NBD","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"10/4/2023 amended on 15/05/25","currency":"USD","quantum":"30,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 14/04/23","guarantorList":["APRIHL"]},
    {"bankName":"Emirates NBD","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"18/10/2016, amended on 15/05/25","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 14/04/23","guarantorList":["APRIHL"]},
    {"bankName":"First Abu Dhabi Bank","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"26/03/2025","currency":"USD","quantum":"10,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 21/04/25","guarantorList":["APRIHL"]},
    {"bankName":"Mizuho","location":"SG","borrower":"AIE, AFBT, AFT","borrowerList":["AIE","AFBT","AFT"],"dateOfFacility":"Negotiating","currency":"Negotiating","quantum":"Negotiating","facilityType":"Negotiating","facilityTypeList":["Negotiating"],"tenure":"Negotiating","tenureExpired":False,"status":"Negotiating","securityPackage":"Negotiating","guarantorList":[]},
    {"bankName":"MUFG, Singapore","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"25/04/2022, amended on 15/03/2024","currency":"USD","quantum":"25,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 05/12/24; DFF Guarantee dd 05/12/24; SGF Guarantee dd 05/12/24","guarantorList":["APRIHL","DFF","SGF"]},
    {"bankName":"MUFG, Singapore","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"18/8/2021, amended on 05/12/24","currency":"EUR","quantum":"16,600,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 05/12/24; DFF Guarantee dd 05/12/24; SGF Guarantee dd 05/12/24","guarantorList":["APRIHL","DFF","SGF"]},
    {"bankName":"MUFG, Singapore","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"2/1/2019, amended on 30/12/2019, further amended on 30/12/2020, 05/12/24","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 05/12/24; DFF Guarantee dd 05/12/24; SGF Guarantee dd 05/12/24","guarantorList":["APRIHL","DFF","SGF"]},
    {"bankName":"MUFG, Singapore","location":"SG","borrower":"AIE, AFPT, AFT","borrowerList":["AIE","AFPT","AFT"],"dateOfFacility":"07/11/24 amended on 23/05/25","currency":"USD","quantum":"50,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 05/12/24; DFF Guarantee dd 05/12/24; SGF Guarantee dd 05/12/24","guarantorList":["APRIHL","DFF","SGF"]},
    {"bankName":"MUFG, India","location":"SG","borrower":"OCPL","borrowerList":["OCPL"],"dateOfFacility":"24/10/2024","currency":"INR","quantum":"1,450,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Negotiating","tenureExpired":False,"status":"Negotiating","securityPackage":"Negotiating","guarantorList":[]},
    {"bankName":"MUFG, Jakarta","location":"SG","borrower":"RAPP","borrowerList":["RAPP"],"dateOfFacility":"31/01/2024","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 24/07/2019","guarantorList":["APRIHL"]},
    {"bankName":"MUFG, Malaysia","location":"SG","borrower":"AFEM, AFPT","borrowerList":["AFEM","AFPT"],"dateOfFacility":"17/04/2017, amended on 19/06/2017, amended on 21/09/2018, amended on 16/06/2020, amended on 8/12/2021, further amended 11/03/2024","currency":"USD","quantum":"75,000,000","facilityType":"Trade Finance","facilityTypeList":["Trade Finance"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL dd 24/09/24; DFF dd 24/09/24; SGF dd 24/09/24; MFF dd 24/09/24; SGF Guarantee dd 24/09/24","guarantorList":["APRIHL","DFF","MFF","SGF"]},
    {"bankName":"Nomura Singapore Limited","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"09/07/2018, amended on 19/05/2020, further amended 19/11/24","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 31/01/25","guarantorList":["APRIHL"]},
    {"bankName":"Shanghai Pudong Bank, Singapore","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"12/2/2020, amended on 21/08/24","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 12/02/2020, amended on 21/08/24","guarantorList":["APRIHL"]},
    {"bankName":"Taishin International Bank, Singapore","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"21/02/2024","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 11/06/2024","guarantorList":["APRIHL"]},
    {"bankName":"UBS, Singapore","location":"SG","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"21/08/2024","currency":"N/A","quantum":"N/A","facilityType":"Derivatives","facilityTypeList":["Derivatives"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 21/08/2024","guarantorList":["APRIHL"]},
    # --- UAE ---
    {"bankName":"AIE","location":"UAE","borrower":"AIE","borrowerList":["AIE"],"dateOfFacility":"06/12/2024","currency":"N/A","quantum":"25,000,000","facilityType":"Trade Financing","facilityTypeList":["Trade Financing"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"APRIHL Guarantee dd 30/12/24; SGF Guarantee dd 30/12/24","guarantorList":["APRIHL","SGF"]},
    {"bankName":"First Abu Dhabi Bank","location":"UAE","borrower":"AFPT","borrowerList":["AFPT"],"dateOfFacility":"02/09/2025","currency":"USD","quantum":"30,000,000","facilityType":"Trade Financing","facilityTypeList":["Trade Financing"],"tenure":"Undefined","tenureExpired":False,"status":"Current","securityPackage":"AFPT Security over Movable Assets dd 02/09/25","guarantorList":["AFPT"]},
]

# ---------------------------------------------------------------------------
# DERIVED FILTER OPTIONS
# ---------------------------------------------------------------------------

BORROWERS   = sorted({b for r in RAW_DATA for b in r["borrowerList"]})
BANKS       = sorted({r["bankName"] for r in RAW_DATA})
FAC_TYPES   = sorted({ft for r in RAW_DATA for ft in r["facilityTypeList"]})
GUARANTORS  = sorted({g for r in RAW_DATA for g in r["guarantorList"]})

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="app-header">
        <h1>📊 APRIL Bilateral Facilities Register</h1>
        <p>As at 02 June 2026 &nbsp;|&nbsp; Banking Facilities Overview across HK, SG &amp; UAE</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## 🔍 Filters")

    f_borrower = st.selectbox("Borrower", ["All Borrowers"] + BORROWERS)
    f_bank     = st.selectbox("Bank",     ["All Banks"]     + BANKS)
    f_fac      = st.selectbox("Facility Type", ["All Facility Types"] + FAC_TYPES)
    f_security = st.selectbox(
        "Guarantee / Security",
        ["All", "With Guarantee/Security", "No Guarantee/Security (Nil)"],
    )
    f_guarantor = st.selectbox("Guarantor", ["All Guarantors"] + GUARANTORS)
    f_tenure    = st.selectbox("Tenure Status", ["All", "Expired Only", "Non-Expired Only"])

    if st.button("❌ Clear All Filters"):
        st.rerun()

# Normalise selections
sel_borrower  = None if f_borrower  == "All Borrowers"    else f_borrower
sel_bank      = None if f_bank      == "All Banks"        else f_bank
sel_fac       = None if f_fac       == "All Facility Types" else f_fac
sel_security  = None if f_security  == "All"              else f_security
sel_guarantor = None if f_guarantor == "All Guarantors"   else f_guarantor
sel_tenure    = None if f_tenure    == "All"              else f_tenure

# ---------------------------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------------------------

filtered = RAW_DATA.copy()

if sel_borrower:
    filtered = [r for r in filtered if sel_borrower in r["borrowerList"]]
if sel_bank:
    filtered = [r for r in filtered if r["bankName"] == sel_bank]
if sel_fac:
    filtered = [r for r in filtered if sel_fac in r["facilityTypeList"]]
if sel_security == "With Guarantee/Security":
    filtered = [r for r in filtered if r["securityPackage"] not in ("Nil", "N/A", "")]
elif sel_security == "No Guarantee/Security (Nil)":
    filtered = [r for r in filtered if r["securityPackage"] in ("Nil", "N/A", "")]
if sel_guarantor:
    filtered = [r for r in filtered if sel_guarantor in r["guarantorList"]]
if sel_tenure == "Expired Only":
    filtered = [r for r in filtered if r["tenureExpired"]]
elif sel_tenure == "Non-Expired Only":
    filtered = [r for r in filtered if not r["tenureExpired"]]

n_filtered   = len(filtered)
n_expired    = sum(1 for r in filtered if r["tenureExpired"])
n_guarantees = sum(len(r["guarantorList"]) for r in filtered)

# ---------------------------------------------------------------------------
# STATS BAR
# ---------------------------------------------------------------------------

st.markdown(
    f"""
    <div class="stat-row">
        <div class="stat-card"><div class="num">{len(RAW_DATA)}</div><div class="lbl">Total Facilities</div></div>
        <div class="stat-card"><div class="num">{n_filtered}</div><div class="lbl">Showing</div></div>
        <div class="stat-card expired"><div class="num">{n_expired}</div><div class="lbl">Expired</div></div>
        <div class="stat-card"><div class="num">{n_guarantees}</div><div class="lbl">Guarantees (Filtered)</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# GUARANTOR SUMMARY
# ---------------------------------------------------------------------------

if sel_guarantor:
    g_items = [r for r in filtered if sel_guarantor in r["guarantorList"]]
    items_html = "".join(
        f"<li>{r['bankName']} — {r['borrower']} ({r['facilityType']})</li>"
        for r in g_items
    )
    st.markdown(
        f"""
        <div class="g-summary">
            <h4>{len(g_items)} guarantee(s) given by <strong>{sel_guarantor}</strong></h4>
            <ul style="margin:0;padding-left:20px;font-size:0.88em;color:#555">{items_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# TABLE
# ---------------------------------------------------------------------------

LOC_COLORS = {"HK": "#2e7d32", "SG": "#1565c0", "UAE": "#6a1b9a"}

if not filtered:
    st.info("No facilities match your current filters.")
else:
    rows_html = ""
    for i, r in enumerate(filtered):
        loc_color = LOC_COLORS.get(r["location"], "#555")
        loc_badge = (
            f'<span class="badge-loc badge-{r["location"]}">{r["location"]}</span>'
        )
        tenure_html = r["tenure"]
        if r["tenureExpired"]:
            tenure_html += ' <span class="badge-expired">⚠ EXPIRED</span>'
        row_class = 'class="expired-row"' if r["tenureExpired"] else ""
        rows_html += f"""
        <tr {row_class}>
            <td>{i+1}</td>
            <td>{r['bankName']}</td>
            <td>{loc_badge}</td>
            <td>{r['borrower']}</td>
            <td>{r['dateOfFacility']}</td>
            <td>{r['currency']}</td>
            <td>{r['quantum']}</td>
            <td>{r['facilityType']}</td>
            <td>{tenure_html}</td>
            <td>{r['status']}</td>
            <td style="font-size:0.82em">{r['securityPackage']}</td>
        </tr>"""

    table_html = f"""
    <div style="overflow-x:auto">
    <table class="fac-table">
        <thead>
            <tr>
                <th>#</th><th>Bank</th><th>Location</th><th>Borrower(s)</th>
                <th>Date of Facility</th><th>Currency</th><th>Quantum</th>
                <th>Facility Type</th><th>Tenure</th><th>Status</th><th>Security Package</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="footer">APRIL Bilateral Facilities Register &copy; 2026 &mdash; Data as at 02 June 2026</div>',
    unsafe_allow_html=True,
)
