# Magic Square Generator

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: GPL v2](https://img.shields.io/badge/license-GPLv2-lightgrey.svg)](LICENSE)

Builds **magic squares of order N** — every row, column and both diagonals add up to the same
constant — with a **two-phase evolutionary algorithm with local rectification** (a memetic
algorithm), following T. Xie and L. Kang [1]. Project for the *Metaheuristic Search* course of
the MSc in Artificial Intelligence, Universidad Politécnica de Madrid.

The whole development — each operator, the experiments and why the simple approach fails — is
explained step by step in the notebook: [`MagicSquareGenerator_Notebook.ipynb`](MagicSquareGenerator_Notebook.ipynb).

## Results

| Order N | Search space (N²!) | **Time** |
|:---:|:---:|:---:|
| 8 | 1.2 × 10⁸⁹ | **2.6 s** |
| 10 | 9.3 × 10¹⁵⁷ | **8.8 s** |
| 15 | 5.9 × 10⁴³² | **41.5 s** |
| 20 | 6.4 × 10⁸⁶⁸ | **4 min 15 s** |
| 30 | 1.4 × 10²²⁷⁴ | **22 min** |
| 40 | 2.1 × 10⁴⁴³² | **4 h 15 min** |

For N = 40, exhaustive search would take about 6.6 × 10⁴⁴¹² years even at 10¹² combinations per
second — the age of the universe is 1.38 × 10¹⁰ years.

## Quick start

```bash
git clone https://github.com/alvarogmendez/magic_square_generator.git
cd magic_square_generator
pip install -r requirements.txt

python MagicSquareGenerator.py              # order 10 (a few seconds)
python MagicSquareGenerator.py -n 20        # choose the order
python MagicSquareGenerator.py -h           # all options
```

| Option | Default | Meaning |
|---|---|---|
| `-n`, `--size` | 10 | Order N of the square |
| `--seed` | 25 | Random seed |
| `--max-iterations` | 200000 | Generation limit |
| `-o`, `--output` | `matriz.txt` | Where the square is saved |
| `--no-plot` | off | Do not show the fitness plots at the end |

## How it works

A simple evolution strategy (individual = matrix + per-cell mutation step σ, fitness = total
deviation of rows, columns and diagonals from the magic constant c = n(n²+1)/2) only succeeds for
orders 3–4 at a very high cost. Splitting the problem makes it tractable:

1. **Phase 1 — rows and columns.** The fitness only counts rows and columns. Mutation acts on the
   cells that break the magic sum (sets S₁ and S₂) through three permutation operators whose
   probabilities depend on the number of wrong rows and columns; σ adapts to a global deviation.
   Result: a *semi-magic* square.
2. **Phase 2 — diagonals.** Only whole rows and columns are swapped, so row and column sums are
   preserved while both diagonals are driven to c.
3. **Local rectification.** When evolution stagnates, deterministic swaps of one or two pairs of
   cells fix two rows/columns — or both diagonals — at once. This is what makes large orders
   feasible.

## Possible improvements

A compiled language instead of Python, parallel evaluation of individuals, profiling the
operators, evolutionary-computation libraries (DEAP, PyGAD) and comparing other metaheuristics
(simulated annealing, ant colony optimisation).

## References

[1] T. Xie and L. Kang, "An evolutionary algorithm for magic squares," *The 2003 Congress on
Evolutionary Computation (CEC '03)*, Canberra, Australia, 2003, vol. 2, pp. 906–913.
doi: [10.1109/CEC.2003.1299763](https://doi.org/10.1109/CEC.2003.1299763)

[2] X. Cui, X. Cheng and G. Bu, "Research on Magic Square Construction Based on Genetic
Algorithm," *Academic Journal of Computing & Information Science*, vol. 5, no. 2, pp. 77–80,
2022. doi: [10.25236/AJCIS.2022.050212](https://doi.org/10.25236/AJCIS.2022.050212)

## Author

Álvaro González Méndez — [alvarogmendez.es](https://alvarogmendez.es) · [LinkedIn](https://www.linkedin.com/in/alvarogmendez/)

Released under the [GNU GPL v2](LICENSE).
