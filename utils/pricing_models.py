from math import log, sqrt, exp
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    if T!=0:
        d1 = (log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)

        if option_type == 'call':
            price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
        else:
            price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        price = max(S - K, 0) if option_type=='call' else max(K - S, 0)
    return round(price, 4)
