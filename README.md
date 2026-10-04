# Extremal Depth-Weighted Symmetry Trees

Python code for constructing extremal rooted binary tree shapes for the depth-weighted symmetry index studied in the accompanying manuscript:

**Extremal Depth-Weighted Symmetry in Rooted Binary Trees**

The program takes a prescribed number of leaves `n` and returns:

- the unique **minimising tree** for every positive non-increasing depth weight `f`;
- the unique **maximising tree** for reciprocal exponential weights

```text
f_q(d) = q^(-d),   q > 2.
```

The mathematical objects studied in the paper are **finite rooted, unordered, unlabelled full binary tree shapes**. Accordingly, the default output represents every leaf by the symbol `•`, matching the notation used in the manuscript.

For reciprocal exponential weights, the maximising **shape is independent of q** throughout the range `q > 2`.

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

If `n = 1`, the maximiser is a single leaf:

```text
•;
```

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

## Tree-shape notation

By default, the program uses a parenthetic representation of the **unlabelled tree shape**, with `•` denoting a leaf.

Examples:

```text
•;
```

is the one-leaf tree,

```text
(•,•);
```

is the unique rooted binary tree with two leaves, and

```text
((•,•),•);
```

represents the 3-leaf caterpillar.

Because the trees are **unordered**, exchanging the two children of any internal vertex does not produce a different mathematical tree shape. The program therefore uses a canonical ordering of the child representations.

This default notation is intended to mirror the notation used in the accompanying paper.

### Optional labelled Newick output

Some external phylogenetic programs require named tips. For compatibility with such software, the option

```bash
--label-leaves
```

produces standard Newick output with leaves labelled `L1`, `L2`, ..., `Ln`.

For example:

```bash
python extremal_symmetry_trees.py 3 --label-leaves
```

produces a labelled representation of the form

```text
((L1,L2),L3);
```

The labels have no mathematical meaning; they are introduced only for software compatibility.

---

## Requirements

- Python 3.9 or later
- No external Python packages are required

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

To save the two extremal trees:

```bash
python extremal_symmetry_trees.py 14 --q 3 --save-dir trees
```

With the default unlabelled `•` notation, this creates

```text
trees/minimiser_14.tree
trees/maximiser_14.tree
```

If `--label-leaves` is used, the program instead saves standard Newick files:

```text
trees/minimiser_14.newick
trees/maximiser_14.newick
```

---

## Example

Running

```bash
python extremal_symmetry_trees.py 14 --q 3
```

produces

```text
n = 14
output = unlabelled tree-shape notation (• = leaf)

MINIMISER
valid for every positive non-increasing f
(((((((((((((•,•),•),•),•),•),•),•),•),•),•),•),•),•);

MAXIMISER
valid for f_q(d)=q^(-d), q>2
((((•,•),(•,•)),((•,•),•)),(((•,•),(•,•)),((•,•),•)));

q = 3
I_q(min) = 1.88167642316e-06
I_q(max) = 1.44444444444
```

For `n = 14`,

```text
14 = 2 * 7,
```

so the maximiser consists of two copies of the unique optimal 7-leaf tree.

In the notation of the paper,

```text
T*_7 = (F_2, (F_1, •)),
```

and therefore

```text
T_max(14) = (T*_7, T*_7).
```

---

## Features

- Direct construction from the theoretical extremal characterisation.
- Default output for **unlabelled tree shapes** using `•` for leaves.
- Canonical child ordering for unordered trees.
- Optional labelled Newick output for compatibility with external software.
- Optional evaluation of `I_q` for any prescribed `q > 2`.
- Optional saving of the generated trees to files.
- No third-party dependencies.
- Integer arithmetic for the preferred power `p(n)`, avoiding floating-point ambiguity.
- Internal checks on the number of leaves.

---

## Repository structure

A minimal repository can be organised as

```text
.
├── README.md
└── extremal_symmetry_trees.py
```

Generated tree files may optionally be stored in a separate directory:

```text
.
├── README.md
├── extremal_symmetry_trees.py
└── trees/
    ├── minimiser_14.tree
    └── maximiser_14.tree
```

---

## Main functions

### `caterpillar(n)`

Constructs the caterpillar `C_n`, the unique minimiser for every positive non-increasing depth weight.

### `fully_balanced(height)`

Constructs the fully balanced tree `F_h` with `2^h` leaves.

### `preferred_power(n)`

For odd `n >= 3`, computes the unique power of two `p(n)` satisfying

```text
(n+1)/3 < p(n) <= 2(n+1)/3.
```

### `maximiser_exponential(n)`

Constructs the unique maximising tree shape for

```text
f_q(d) = q^(-d),   q > 2.
```

### `iq_value(tree, q)`

Computes

```text
I_q(T) = sum_{v in Sym(T)} q^(-depth_T(v)).
```

### `to_bullet_notation(tree)`

Returns the canonical parenthetic representation of the unlabelled tree shape using `•` for each leaf.

### `to_labelled_newick(tree)`

Returns a standard Newick representation with leaves labelled `L1`, ..., `Ln`.

---

## Scope and limitations

The closed-form maximiser implemented in this repository is proved for

```text
f_q(d) = q^(-d),   q > 2.
```

The program rejects `q <= 2` when the `--q` option is supplied because the structural characterisation used here is not asserted for that range.

For a general positive weight function `f`, the program implements the minimising shape whenever `f` is non-increasing, but it does **not** attempt to determine the maximiser.

The default `•` representation is intended as mathematical tree-shape notation. Use `--label-leaves` when strict compatibility with Newick-based phylogenetic software is required.

---

## Accompanying manuscript

This code accompanies the manuscript:

> **Arnau Mir-Fuentes and Arnau Mir**  
> *Extremal Depth-Weighted Symmetry in Rooted Binary Trees*

The paper introduces the symmetry profile of a rooted binary tree and studies the associated family of depth-weighted symmetry indices. The code in this repository implements the explicit extremal constructions obtained in the paper.

The final bibliographic reference and DOI will be added once the article is published.

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
