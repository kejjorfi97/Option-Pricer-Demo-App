import plotly.graph_objs as go
import numpy as np
from utils.pricing_models import black_scholes
from utils.greeks import delta, gamma, vega, rho, theta

def draw_payoff_chart(S, K, premium, option_type):
    # Option parameters
    S_range = np.linspace(0.5*S, 1.5*S, 100)  # Underlying prices at expiration

    # Payoff calculation
    if option_type == "call":
        payoff = np.maximum(S_range - K, 0) - premium
        breakeven = K + premium
        current_pnl = max(S - K, 0) - premium
    else:
        payoff = np.maximum(K - S_range, 0) - premium
        breakeven = K - premium
        current_pnl = max(K - S, 0) - premium

    # Create the figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=S_range,
        y=payoff,
        mode='lines',
        name='Net Payoff',
        line=dict(color='royalblue', width=3)
    ))

    # Add horizontal line at y=0 (break-even)
    fig.add_trace(go.Scatter(
        x=[S_range.min(), S_range.max()],
        y=[0, 0],
        mode='lines',
        name='Break-even Line',
        line=dict(color='gray', dash='dash')
    ))

    # Annotate break-even point
    fig.add_vline(
        x=breakeven,
        line=dict(color='green', dash='dot'),
        annotation_text=f'Break-even: {breakeven}',
        annotation_position='top right'
    )

    # Current P&L marker
    fig.add_trace(go.Scatter(
        x=[S],
        y=[current_pnl],
        mode='markers+text',
        name='Current P&L',
        marker=dict(size=10, color='green' if current_pnl >= 0 else 'red'),
        text=[f"P&L: {'+' if current_pnl >= 0 else ''}{round(current_pnl, 2)}"],
        textposition="bottom right"
    ))

    # Layout settings
    fig.update_layout(
        title='Option Payoff Diagram (with Premium)',
        xaxis_title='Stock Price at Expiration',
        yaxis_title='Profit / Loss',
        template='plotly_white',
        showlegend=True
    )

    return fig


def simulate_vol_smile(S, base_vol=0.2):
    strikes = np.linspace(0.8 * S, 1.2 * S, 30)
    vols = [base_vol + 0.05 * abs((K - S) / S) for K in strikes]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strikes, y=vols, mode='lines+markers', name='Vol Smile'))
    fig.update_layout(title="Volatility Smile", xaxis_title="Strike Price", yaxis_title="Implied Volatility")
    return fig

def simulate_delta(S, K, T, r, sigma, option_type='call'):
    S_range = np.linspace(0.5*S, 1.5*S, 100) 
    prices = [black_scholes(S_, K, T, r, sigma, option_type) for S_ in S_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range, y=prices, mode='lines+markers', name='Price Over Time'))
    fig.update_layout(xaxis_title="Stock Price", yaxis_title="Option Price")
    return fig

def simulate_gamma(S, K, T, r, sigma, option_type='call'):
    S_range = np.linspace(0.5*S, 1.5*S, 100) 
    prices = [delta(S_, K, T, r, sigma, option_type) for S_ in S_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_range, y=prices, mode='lines+markers', name='Price Over Time'))
    fig.update_layout(xaxis_title="Stock Price", yaxis_title="Delta")
    return fig

def simulate_vega(S, K, T, r, sigma, option_type='call'):
    vol_range = np.linspace(0.5*sigma, 5*sigma, 100)
    # vol_range = np.linspace(0.5*sigma, 1.5*sigma, 100)
    prices = [black_scholes(S, K, T, r, vol, option_type) for vol in vol_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vol_range, y=prices, mode='lines+markers', name='Price Over Time'))
    fig.update_layout(xaxis_title="Volatility", yaxis_title="Option Price")
    return fig

def simulate_theta(S, K, T, r, sigma, option_type='call'):
    T_range = np.linspace(0.5*T, 1.5*T, 100) if T!=0 else np.linspace(0, 1, 100)
    prices = [black_scholes(S, K, t, r, sigma, option_type) for t in T_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=T_range, y=prices, mode='lines+markers', name='Price Over Time'))
    fig.update_layout(xaxis_title="Time to Maturity (years)", yaxis_title="Option Price")
    return fig

def simulate_rho(S, K, T, r, sigma, option_type='call'):
    r_range = np.linspace(0.5*r, 1.5*r, 100)
    prices = [black_scholes(S, K, T, r_, sigma, option_type) for r_ in r_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=r_range, y=prices, mode='lines+markers', name='Price Over Time'))
    fig.update_layout(xaxis_title="Interest Rate", yaxis_title="Option Price")
    return fig

