
from math import log, sqrt, exp
from scipy.stats import norm
import numpy as np
import pandas as pd

def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def delta(S, K, T, r, sigma, option_type):
    d_1 = d1(S, K, T, r, sigma)
    if option_type == 'call':
        return norm.cdf(d_1)
    else:
        return -norm.cdf(-d_1)

def gamma(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return norm.pdf(d_1) / (S * sigma * np.sqrt(T))

def vega(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return S * norm.pdf(d_1) * np.sqrt(T)

def theta(S, K, T, r, sigma, option_type):
    d_1 = d1(S, K, T, r, sigma)
    d_2 = d2(S, K, T, r, sigma)
    term1 = -(S * norm.pdf(d_1) * sigma) / (2 * np.sqrt(T))
    if option_type == 'call':
        term2 = r * K * np.exp(-r * T) * norm.cdf(d_2)
        return term1 - term2
    else:
        term2 = r * K * np.exp(-r * T) * norm.cdf(-d_2)
        return term1 + term2

def rho(S, K, T, r, sigma, option_type):
    d_2 = d2(S, K, T, r, sigma)
    if option_type == 'call':
        return K * T * np.exp(-r * T) * norm.cdf(d_2)
    else:
        return -K * T * np.exp(-r * T) * norm.cdf(-d_2)

def compute_greeks(S, K, T, r, sigma, option_type='call'):
    greeks = {
        "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
        "Symbol": ["Δ", "Γ", "ν", "Θ", "ρ"],
        "Value": [round(delta(S, K, T, r, sigma, option_type), 4), round(gamma(S, K, T, r, sigma), 4), 
                round(vega(S, K, T, r, sigma), 4), round(theta(S, K, T, r, sigma, option_type), 4),
                    round(rho(S, K, T, r, sigma, option_type), 4)],
        "Units": [
            "per $1 change",
            "per $1 change",
            "per 1% volatility",
            "per day",
            "per 1% rate change"
        ]
    }

    df=pd.DataFrame([*list(greeks.values())]).T
    df.columns = list(greeks.keys())
    df.set_index("Greek", inplace=True)
    df["Value"] = df["Value"].apply(lambda x: f"{x:.4f}")

    styled_df = df.style.set_properties(**{
    'background-color': '#f9f9f9',
    'color': '#000000',
    'border-color': '#cccccc',
    'text-align': 'center'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#1f77b4'),
                ('color', 'white'),
                ('text-align', 'center')]
    }])
    return styled_df



