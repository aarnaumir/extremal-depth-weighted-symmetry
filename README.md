# Extremal Depth-Weighted Symmetry Trees

Python code for constructing extremal rooted binary tree shapes for the depth-weighted symmetry index studied in the accompanying manuscript:

**Extremal Depth-Weighted Symmetry in Rooted Binary Trees**

The program takes a prescribed number of leaves `n` and returns, in **Newick format**:

- the unique **minimising tree** for every positive non-increasing depth weight `f`;
- the unique **maximising tree** for reciprocal exponential weights

```text
f_q(d) = q^(-d),   q > 2.
```

For the reciprocal exponential family, the maximising **shape is independent of q** throughout the range `q > 2`.

---

## Mathematical background

Let `T` be a finite rooted unordered binary tree. An internal vertex `v` is called **symmetric** when its two child subtrees are isomorphic as rooted trees.

Given a positive depth weight

```text
f : N_0 -> (0, infinity),
```

the depth-weighted symmetry index is

```text
I_f(T) = sum_{v in Sym(T)} f(depth_T(v)).
```

The script implements the extremal results proved in the accompanying work.

### Minimum

For every positive non-increasing depth weight `f`, the unique minimiser among rooted binary trees with `n` leaves is the **caterpillar** `C_n`.

### Maximum for reciprocal exponential weights

For

```text
f_q(d) = q^(-d),   q > 2,
```

the unique maximiser is constructed recursively.

If `n = 1`, the maximiser is a single leaf.

If `n` is even,

```text
T_max(n) = (T_max(n/2), T_max(n/2)).
```

If `n >= 3` is odd,

```text
T_max(n) = (F_k(n), T_max(n - p(n))),
```

where `F_k` denotes the fully balanced tree of height `k`, and

```text
k(n) = floor(log2(2(n+1)/3)),
p(n) = 2^k(n).
```

Equivalently, `p(n)` is the unique power of two satisfying

```text
(n+1)/3 < p(n) <= 2(n+1)/3.
```

---

## Features

- Constructs the extremal tree shapes directly from the theoretical characterisation.
- Outputs both trees in standard Newick format.
- Uses only the Python standard library.
- Optionally evaluates `I_q` for a chosen `q > 2`.
- Optionally saves the minimiser and maximiser as `.newick` files.
- Uses integer arithmetic to determine the preferred power `p(n)`, avoiding floating-point ambiguity.
- Includes internal checks for the number of leaves.

---

## Requirements

- Python 3.9 or later
- No external Python packages are required.

---

## Usage

Basic usage:

```bash
python extremal_symmetry_trees.py N
```

where `N` is the desired number of leaves.

For example:

```bash
python extremal_symmetry_trees.py 14
```

To also evaluate the reciprocal exponential index for a particular `q > 2`:

```bash
python extremal_symmetry_trees.py 14 --q 3
```

To save the Newick trees to a directory:

```bash
python extremal_symmetry_trees.py 14 --q 3 --save-dir trees
```

This creates

```text
trees/minimiser_14.newick
trees/maximiser_14.newick
```

---

## Example

For `n = 14`,

```text
14 = 2 * 7.
```

Hence the maximiser consists of two copies of the optimal 7-leaf tree.

The optimal 7-leaf tree has the recursive form

```text
T*_7 = (F_2, (F_1, leaf)).
```

Therefore,

```text
T_max(14) = (T*_7, T*_7).
```

Running

```bash
python extremal_symmetry_trees.py 14 --q 3
```

produces output of the form

```text
n = 14

MINIMISER
valid for every positive non-increasing f
(L1,(L2,(L3,(L4,(L5,(L6,(L7,(L8,(L9,(L10,(L11,(L12,(L13,L14)))))))))))));

MAXIMISER
valid for f_q(d)=q^(-d), q>2
((((L1,L2),(L3,L4)),((L5,L6),L7)),(((L8,L9),(L10,L11)),((L12,L13),L14)));

q = 3
I_q(min) = 1.88167642316e-06
I_q(max) = 1.44444444444
```

The leaf labels `L1`, `L2`, ..., `Ln` are introduced only to produce a valid and readable Newick representation. The mathematical objects studied in the paper are **unlabelled, unordered tree shapes**.

---

## Repository structure

A minimal repository can be organised as

```text
.
├── README.md
└── extremal_symmetry_trees.py
```

If desired, generated Newick files can be kept in a separate directory:

```text
.
├── README.md
├── extremal_symmetry_trees.py
└── trees/
    ├── minimiser_14.newick
    └── maximiser_14.newick
```

---

## Main functions

The script contains the following main routines.

### `caterpillar(n)`

Constructs the caterpillar `C_n`, the unique minimiser for positive non-increasing depth weights.

### `fully_balanced(height)`

Constructs the fully balanced tree `F_h` with `2^h` leaves.

### `preferred_power(n)`

For odd `n >= 3`, computes the unique power of two `p(n)` satisfying

```text
(n+1)/3 < p(n) <= 2(n+1)/3.
```

### `maximiser_exponential(n)`

Constructs the unique maximising tree for

```text
f_q(d) = q^(-d),   q > 2.
```

### `iq_value(tree, q)`

Computes

```text
I_q(T) = sum_{v in Sym(T)} q^(-depth_T(v)).
```

for a given tree.

### `to_newick(tree)`

Converts the internal tree representation into Newick format.

---

## Scope and limitations

The closed-form maximum implemented here is proved for

```text
f_q(d) = q^(-d),   q > 2.
```

The script deliberately rejects `q <= 2` when `--q` is supplied because the structural characterisation of the maximiser used here is not asserted for that range.

For a general positive weight function `f`, the minimiser is implemented whenever `f` is non-increasing, but the present script does **not** attempt to determine the maximiser.

A natural extension of the code is a brute-force enumerator for small `n`, which would allow arbitrary depth weights `f` to be explored computationally.

---

## Newick convention

The Newick strings encode rooted binary tree shapes using arbitrary leaf labels.

For example,

```text
(L1,(L2,L3));
```

represents a 3-leaf caterpillar.

Because the underlying trees are unordered, exchanging the left and right child of any internal node represents the same mathematical tree shape.

---

## Citation

If you use this code in academic work, please cite the accompanying manuscript:

> Arnau Mir-Fuentes and Arnau Mir,  
> *Extremal Depth-Weighted Symmetry in Rooted Binary Trees*.

A complete bibliographic entry can be added here once the article is published.

---

## Authors

**Arnau Mir-Fuentes**  
Topological Models for Fuzzy Information Processing (MOTIBO)  
Universitat de les Illes Balears

**Arnau Mir**  
Soft Computing, Image Processing and Aggregation Research Group (SCOPIA)  
Universitat de les Illes Balears

---

## License

No licence is included by default. Before making the repository public, consider adding an open-source licence such as the MIT License if you want others to be able to reuse and modify the code.
