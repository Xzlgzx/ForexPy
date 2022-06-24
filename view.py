import streamlit as st
import datetime

from forex import ForexRequest

st.header("Forex App")
begin_container, end_container = st.columns(2)

today = datetime.date.today()
begin = begin_container.date_input("Put start date here", today)
end = end_container.date_input("Put end date here", today)
confirm = st.button("Confirm here.")

if confirm:
    if begin > today or end > today or begin > end:
        st.warning("Bad inputs, please select again!")
    else:
        usd_cad_status = ForexRequest.get_usd_cad(begin, end)
        if usd_cad_status:
            ForexRequest.create_usd_cad_list()
            high = ForexRequest.get_high(False)
            low = ForexRequest.get_low(False)
            avg = ForexRequest.get_avg(False)
            st.write(f"USD/CAD: High is {high}. Low is {low}. Avg is {avg}")
        else:
            st.write("Data unavailable for USD/CAD.")

        corra_status = ForexRequest.get_corra(begin, end)
        if corra_status:
            ForexRequest.create_corra_list()
            high = ForexRequest.get_high(True)
            low = ForexRequest.get_low(True)
            avg = ForexRequest.get_avg(True)
            st.write(f"CORRA: High is {high}. Low is {low}. Avg is {avg}")
        else:
            st.write("Data unavailable for CORRA.")

        if corra_status and usd_cad_status:
            corr = ForexRequest.get_correlation()
            st.write(f"Pearson coefficient of correlation: {corr}")
        else:
            st.write("Data unavailable for correlation.")
    ForexRequest.reset_class()
