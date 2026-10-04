#!/usr/bin/env python3
"""
Construct extremal rooted binary trees for the depth-weighted symmetry index.

Minimum:
  For every positive non-increasing depth weight f, the unique minimiser
  with n leaves is the caterpillar C_n.

Maximum:
  For f_q(d)=q^{-d}, q>2, the unique maximiser is independent of q and is
  given recursively by:
      M(1) = leaf,
      M(n) = (M(n/2), M(n/2))              if n is even,
      M(n) = (F_{k(n)}, M(n-p(n)))         if n>=3 is odd,
  where p(n)=2^{k(n)} is the unique power of two satisfying
      (n+1)/3 < p(n) <= 2(n+1)/3.

Output is Newick with leaves labelled L1,...,Ln.
"""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Union, Tuple

Tree = Union[None, Tuple["Tree", "Tree"]]


def caterpillar(n: int) -> Tree:
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return None
    return (None, caterpillar(n - 1))


def fully_balanced(height: int) -> Tree:
    if height < 0:
        raise ValueError("height must be >= 0")
    if height == 0:
        return None
    u = fully_balanced(height - 1)
    return (u, u)


def preferred_power(n: int) -> int:
    """p(n): unique power of two in ((n+1)/3, 2(n+1)/3], for odd n>=3."""
    if n < 3 or n % 2 == 0:
        raise ValueError("n must be odd and >= 3")
    floor_x = (2 * (n + 1)) // 3
    p = 1 << (floor_x.bit_length() - 1)
    assert n + 1 < 3 * p
    assert 3 * p <= 2 * (n + 1)
    return p


def maximiser_exponential(n: int) -> Tree:
    """Unique maximiser for f_q(d)=q^{-d}, q>2."""
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return None
    if n % 2 == 0:
        u = maximiser_exponential(n // 2)
        return (u, u)
    p = preferred_power(n)
    k = p.bit_length() - 1
    return (fully_balanced(k), maximiser_exponential(n - p))


def leaf_count(t: Tree) -> int:
    if t is None:
        return 1
    a, b = t
    return leaf_count(a) + leaf_count(b)


def canonical_shape(t: Tree) -> str:
    """Canonical unordered rooted-tree shape, used to test isomorphism."""
    if t is None:
        return "L"
    a, b = t
    sa = canonical_shape(a)
    sb = canonical_shape(b)
    if sa > sb:
        sa, sb = sb, sa
    return f"({sa},{sb})"


def iq_value(t: Tree, q: float, depth: int = 0) -> float:
    if q <= 0:
        raise ValueError("q must be > 0")
    if t is None:
        return 0.0
    a, b = t
    root = q ** (-depth) if canonical_shape(a) == canonical_shape(b) else 0.0
    return root + iq_value(a, q, depth + 1) + iq_value(b, q, depth + 1)


def to_newick(t: Tree, prefix: str = "L") -> str:
    counter = 0

    def rec(x: Tree) -> str:
        nonlocal counter
        if x is None:
            counter += 1
            return f"{prefix}{counter}"
        a, b = x
        return f"({rec(a)},{rec(b)})"

    return rec(t) + ";"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="Number of leaves")
    parser.add_argument("--q", type=float, default=None,
                        help="Optional q>2; if given, also prints I_q values")
    parser.add_argument("--save-dir", type=Path, default=None,
                        help="Optional folder for .newick files")
    args = parser.parse_args()

    if args.n < 1:
        parser.error("n must be >= 1")
    if args.q is not None and args.q <= 2:
        parser.error("The implemented maximiser theorem requires q>2")

    tmin = caterpillar(args.n)
    tmax = maximiser_exponential(args.n)

    assert leaf_count(tmin) == args.n
    assert leaf_count(tmax) == args.n

    nw_min = to_newick(tmin)
    nw_max = to_newick(tmax)

    print(f"n = {args.n}")
    print("\nMINIMISER")
    print("valid for every positive non-increasing f")
    print(nw_min)

    print("\nMAXIMISER")
    print("valid for f_q(d)=q^(-d), q>2")
    print(nw_max)

    if args.q is not None:
        print(f"\nq = {args.q:g}")
        print(f"I_q(min) = {iq_value(tmin, args.q):.12g}")
        print(f"I_q(max) = {iq_value(tmax, args.q):.12g}")

    if args.save_dir is not None:
        args.save_dir.mkdir(parents=True, exist_ok=True)
        pmin = args.save_dir / f"minimiser_{args.n}.newick"
        pmax = args.save_dir / f"maximiser_{args.n}.newick"
        pmin.write_text(nw_min + "\n", encoding="utf-8")
        pmax.write_text(nw_max + "\n", encoding="utf-8")
        print(f"\nSaved: {pmin}")
        print(f"Saved: {pmax}")


if __name__ == "__main__":
    main()
