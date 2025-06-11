import streamlit as st
from utils.pricing_models import black_scholes
from utils.greeks import compute_greeks
from utils.visuals import draw_payoff_chart, simulate_theta, simulate_vol_smile,\
                            simulate_delta, simulate_rho,\
                            simulate_vega, simulate_gamma
import pandas as pd

st.title("Vanilla Option Pricer 🧠")

st.sidebar.header("Parameters Input")

option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
S = st.sidebar.number_input("Spot Price", value=100.0)
K = st.sidebar.number_input("Strike Price", value=100.0)
T = st.sidebar.number_input("Time to Maturity (in years)", value=1.0)
r = st.sidebar.number_input("Risk-Free Rate", value=0.01)
sigma = st.sidebar.number_input("Volatility", value=0.2)
premium = st.sidebar.number_input("Premium (optional)", value=0)

if st.sidebar.button("Calculate"):
    price = black_scholes(S, K, T, r, sigma, option_type)
    greeks = compute_greeks(S, K, T, r, sigma, option_type)
    
    st.subheader(f"Fair Value: ${price}")
    
    
    st.plotly_chart(draw_payoff_chart(S, K, premium, option_type))
    # st.plotly_chart(draw_payoff_chart(S, K, T, r, sigma, option_type, price))

    st.subheader("Option Price reaction to changes in:")
    tabs = st.tabs(["Price", "Time to maturity", "Volatility", "Interest rate"])
    
    with tabs[0]:
        st.text(f"{option_type} | K = {K} | T = {int(T)} year(s) | σ = {sigma*100}% | r = {r*100}%")
        st.plotly_chart(simulate_delta(S, K, T, r, sigma, option_type))
    
    with tabs[1]:
        st.text(f"{option_type} | K = {K} | S = {S} | σ = {sigma*100}% | r = {r*100}%")
        st.plotly_chart(simulate_theta(S, K, T, r, sigma, option_type='call'))

    with tabs[2]:
        st.text(f"{option_type} | K = {K} | S = {S} | T = {int(T)} year(s)  | r = {r*100}%")
        st.plotly_chart(simulate_vega(S, K, T, r, sigma, option_type='call'))

    with tabs[3]:
        st.text(f"{option_type} | K = {K} | S = {S} | T = {int(T)} year(s)  | σ = {sigma*100}%")
        st.plotly_chart(simulate_rho(S, K, T, r, sigma, option_type='call'))

    st.markdown("### Greeks")
    st.dataframe(greeks)

    st.subheader("📉 Volatility Smile")
    st.plotly_chart(simulate_vol_smile(K))