import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from collections import deque
from time import sleep

from libs.stream import DataStream

WINDOW_SIZE = 100

DATA_PATH = (
    "data/Fridge/Fridge_1/anomaly_Major_15.70/"
    "fridge_1_day4_ANOMALIES.csv"
)


st.set_page_config(
    page_title="Energy Anomaly Detection",
    page_icon="⚡",
    layout="wide",
)


st.title("⚡ Energy-Based Machine Anomaly Detection")

st.write("Simulated real-time power consumption monitoring")


# -------------------------------
# Session State Initialization
# -------------------------------

if "stream" not in st.session_state:
    st.session_state.stream = DataStream(DATA_PATH)

if "display_window" not in st.session_state:
    st.session_state.display_window = deque(
        maxlen=WINDOW_SIZE
    )


# -------------------------------
# Controls
# -------------------------------

col1, col2 = st.columns(2)

with col1:
    start = st.button("▶ Start Stream")

with col2:
    reset = st.button("🔄 Reset")


# -------------------------------
# Reset
# -------------------------------

if reset:
    st.session_state.stream = DataStream(DATA_PATH)
    st.session_state.display_window = deque(
        maxlen=WINDOW_SIZE
    )

    st.rerun()

# -------------------------------
# Start Streaming
# -------------------------------

chart_placeholder = st.empty()

col1, col2, col3 = st.columns(3)

metric1 = col1.empty()
metric2 = col2.empty()
metric3 = col3.empty()

if start:

    while True:

        try:
            reading = st.session_state.stream.next_reading

            st.session_state.display_window.append(reading)

            chart_data = pd.DataFrame(
                list(st.session_state.display_window)
            )

            max_power = chart_data["active_power"].max()
            y_max = max(100, max_power * 1.2)

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=chart_data["timestamp"],
                    y=chart_data["active_power"],
                    mode="lines",
                    name="Active Power",
                )
            )

            fig.update_layout(
                title="Live Power Consumption",
                xaxis_title="Time",
                yaxis_title="Active Power (W)",
                height=500,
            )

            fig.update_yaxes(
                range=[0, y_max]
            )

            chart_placeholder.plotly_chart(
                fig,
                use_container_width=True,
            )

            metric1.metric(
                "Current Power",
                f"{reading['active_power']:.2f} W"
            )

            metric2.metric(
                "Timestamp",
                reading["timestamp"].strftime("%H:%M:%S")
            )
            if "label" in reading:
                metric3.metric(
                    "Anomaly Detected",
                    reading["label"]
                )
            else:
                metric3.metric(
                    "Anomaly Detected",
                    "N/A"
                )

            sleep(1)

        except StopIteration:
            st.success("Data stream has been exhausted.")
            break