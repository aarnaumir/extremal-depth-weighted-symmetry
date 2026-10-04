#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple, Union

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
    if n < 3 or n % 2 == 0:
        raise ValueError("n must be odd and >= 3")
    floor_x = (2 * (n + 1)) // 3
    p = 1 << (floor_x.bit_length() - 1)
    assert n + 1 < 3 * p
    assert 3 * p <= 2 * (n + 1)
    return p


def maximiser_exponential(n: int) -> Tree:
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


def to_bullet_notation(t: Tree) -> str:
    """
    Canonical parenthetic notation with the symbol • for every leaf.
    Example: the 3-leaf caterpillar is (•,(•,•));
    """
    def rec(x: Tree) -> str:
        if x is None:
            return "•"

        a, b = x
        sa = rec(a)
        sb = rec(b)

        if sa > sb:
            sa, sb = sb, sa

        return f"({sa},{sb})"

    return rec(t) + ";"


def to_labelled_newick(t: Tree, prefix: str = "L") -> str:
    """
    Standard Newick with unique leaf labels, for software that requires them.
    """
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
    parser = argparse.ArgumentParser(
        description="Construct extremal rooted binary tree shapes."
    )
    parser.add_argument("n", type=int, help="Number of leaves")
    parser.add_argument(
        "--q",
        type=float,
        default=None,
        help="Optional q>2; if given, also print I_q values",
    )
    parser.add_argument(
        "--label-leaves",
        action="store_true",
        help="Use L1,...,Ln instead of • for compatibility with standard Newick software.",
    )
    parser.add_argument(
        "--save-dir",
        type=Path,
        default=None,
        help="Optional directory for saved tree files",
    )

    args = parser.parse_args()

    if args.n < 1:
        parser.error("n must be >= 1")
    if args.q is not None and args.q <= 2:
        parser.error("The implemented maximiser theorem requires q > 2")

    tmin = caterpillar(args.n)
    tmax = maximiser_exponential(args.n)

    assert leaf_count(tmin) == args.n
    assert leaf_count(tmax) == args.n

    if args.label_leaves:
        out_min = to_labelled_newick(tmin)
        out_max = to_labelled_newick(tmax)
        mode = "labelled Newick"
        extension = "newick"
    else:
        out_min = to_bullet_notation(tmin)
        out_max = to_bullet_notation(tmax)
        mode = "unlabelled tree-shape notation (• = leaf)"
        extension = "tree"

    print(f"n = {args.n}")
    print(f"output = {mode}")

    print("\nMINIMISER")
    print("valid for every positive non-increasing f")
    print(out_min)

    print("\nMAXIMISER")
    print("valid for f_q(d)=q^(-d), q>2")
    print(out_max)

    if args.q is not None:
        print(f"\nq = {args.q:g}")
        print(f"I_q(min) = {iq_value(tmin, args.q):.12g}")
        print(f"I_q(max) = {iq_value(tmax, args.q):.12g}")

    if args.save_dir is not None:
        args.save_dir.mkdir(parents=True, exist_ok=True)
        pmin = args.save_dir / f"minimiser_{args.n}.{extension}"
        pmax = args.save_dir / f"maximiser_{args.n}.{extension}"
        pmin.write_text(out_min + "\n", encoding="utf-8")
        pmax.write_text(out_max + "\n", encoding="utf-8")
        print(f"\nSaved: {pmin}")
        print(f"Saved: {pmax}")


if __name__ == "__main__":
    main()
