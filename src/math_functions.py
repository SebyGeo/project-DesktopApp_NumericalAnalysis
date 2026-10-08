import numpy as np
from scipy.special import comb

def evaluate_func(f_str, x_vals):
    try:
        allowed_names = {
            "x": x_vals, 
            "np": np, 
            "sin": np.sin, 
            "cos": np.cos, 
            "exp": np.exp, 
            "sqrt": np.sqrt,
            "tan": np.tan,
            "log": np.log,
            "abs": np.abs,
            "pi": np.pi,
            "e": np.e
        }
        return eval(f_str, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        raise ValueError(str(e))
    
def bernstein_poly(f_str, a, b, n, x):
    k = np.arange(n + 1)
    nodes = a + (k / n) * (b - a)
    f_vals = evaluate_func(f_str, nodes)
    
    t = (x - a) / (b - a)
    combinations = comb(n, k)
    
    if isinstance(t, np.ndarray):
        t = t[:, np.newaxis]
        term1 = t ** k
        term2 = (1 - t) ** (n - k)
        terms = f_vals * combinations * term1 * term2
        return np.sum(terms, axis=1)
    else:
        term1 = t ** k
        term2 = (1 - t) ** (n - k)
        terms = f_vals * combinations * term1 * term2
        return np.sum(terms)
    
def lagrange_implementation(x_eval, x_nodes, y_nodes):
    if isinstance(x_eval, (int, float)):
        x_eval = np.array([x_eval])
        
    suma = np.zeros_like(x_eval, dtype=float)
    n = len(x_nodes)
    
    for j in range(n):
        elem_produs = np.ones_like(x_eval, dtype=float)
        for i in range(n):
            if i != j:
                elem_produs *= (x_eval - x_nodes[i]) / (x_nodes[j] - x_nodes[i])
        suma += y_nodes[j] * elem_produs
        
    return suma