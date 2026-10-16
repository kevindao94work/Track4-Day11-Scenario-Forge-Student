"""Part C: estimate a rare probability honestly. TODO 4, 6 and 7."""
from __future__ import annotations

import math

import numpy as np

from avsim import space
from .search import proposal_logpdf


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """TODO 4. Wilson score interval for k successes in n trials. Must behave at k = 0 (lower bound 0,
    upper bound > 0) where the plain normal interval collapses to [0, 0]. Return (0, 1) for n = 0."""
    if n == 0:
        return 0.0, 1.0
    if n < 0 or k < 0 or k > n:
        raise ValueError("Wilson interval requires n > 0 and 0 <= k <= n")
    if not math.isfinite(z) or z < 0:
        raise ValueError("z must be a finite non-negative value")

    p = k / n
    z2 = z * z
    d = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / d
    half = z * math.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n)) / d
    lo = 0.0 if k == 0 else max(0.0, center - half)
    hi = 1.0 if k == n else min(1.0, center + half)
    return lo, hi


def log_weights(Z, Bn, nat: space.Natural, prop: dict, beta: float = 0.2) -> np.ndarray:
    """TODO 6. log p(u) - log q(u) for each row, where q is the DEFENSIVE MIXTURE
    q = (1 - beta) * proposal + beta * natural.

    nat.logpdf(Z, Bn) gives log p; proposal_logpdf(prop, Z, Bn) gives log of the CEM proposal.
    Use np.logaddexp so a weight of 1e-30 does not underflow to 0."""
    if not 0.0 <= beta <= 1.0:
        raise ValueError("beta must be in [0, 1]")
    log_p = nat.logpdf(Z, Bn)
    log_q_prop = proposal_logpdf(prop, Z, Bn)
    if beta == 0.0:
        return log_p - log_q_prop
    if beta == 1.0:
        return np.zeros_like(log_p)
    log_q_mix = np.logaddexp(np.log1p(-beta) + log_q_prop, np.log(beta) + log_p)
    return log_p - log_q_mix


def is_estimate(logw: np.ndarray, y: np.ndarray, z: float = 1.96) -> dict:
    """TODO 7. Importance-sampling estimate of P(y = 1) under the natural distribution.

    w = exp(logw); p = mean(w * y)  (NOT normalised by sum(w): that version is biased for small n);
    se = std(w * y, ddof=1) / sqrt(n); CI = [max(0, p - z se), p + z se];
    Kish effective sample size ess = (sum w)^2 / sum(w^2).
    Return dict(p=, lo=, hi=, se=, ess=, n=)."""
    logw = np.asarray(logw, dtype=float).reshape(-1)
    y = np.asarray(y, dtype=float).reshape(-1)
    if logw.shape != y.shape:
        raise ValueError("logw and y must contain the same number of samples")
    n = len(logw)
    if n == 0:
        return dict(p=0.0, lo=0.0, hi=0.0, se=0.0, ess=0.0, n=0)

    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        w = np.exp(logw)
        wy = w * y
        p = float(np.mean(wy))
        se = float(np.std(wy, ddof=1) / math.sqrt(n)) if n > 1 else 0.0

    max_logw = np.max(logw)
    if np.isneginf(max_logw):
        ess = 0.0
    elif np.isposinf(max_logw):
        n_inf = int(np.isposinf(logw).sum())
        ess = float(n_inf)
    else:
        scaled_w = np.exp(logw - max_logw)
        ess = float(np.sum(scaled_w) ** 2 / np.sum(scaled_w ** 2))
    return dict(p=p, lo=max(0.0, p - z * se), hi=p + z * se, se=se, ess=ess, n=n)


def rule_of_three(n_eff: float) -> float:
    """Given: 95% upper bound on a probability when 0 events were seen in n_eff independent tries."""
    return 3.0 / max(n_eff, 1.0)
