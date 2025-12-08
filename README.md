# Magic Square Generator

### Author: Álvaro González Méndez

I will attempt to generate Magic Squares of order N using evolutionary algorithms following the design proposed in T. Xie and L. Kang's paper, "An Evolutionary Algorithm for Magic Squares" [1].

This project is part of an assignment for the *Busqueda Basada in Metaheuristicas* course.

All the content of this file has been written while impplementig in the jupyter notebook XXXX, to explore more in depth read the notebook. A runnable version of the project can be found aund used following the setup instructions

***
## Setup 
This project works with [Poetry](https://python-poetry.org/) for dependency management.

1.  **Clone repo:**
    ```bash
    git clone [https://github.com/alvarogmendez/Magic-Square-Generator](https://github.com/alvarogmendez/Magic-Square-Generator)
    cd Magic-Square-Generator
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```
3. **Run the code**

   To check all the options you can use
   ```bash
    poetry run python MagicSquareGenerator.py -h
    ```
4. **Feel free to modify all the parameters on the code**

***

## Simple Evolutionary Algorithm

Now, I will follow T. Xie [1] paper and first I will implement an Evolutionary Algorithim based on **Evolution Estrategies** that will try to find a magic square of size NxN in one simple algorithm. According to the publication, this would be able to generate **High-Quality Magic Squares** but with a very high cost and with order under 10.


### Individuals
An individual will be denoted *I*, It will consist of two difernt matrix, *M* containing the values of the Magic Square to be constructed, and *Δ* containing all the mutation variance values **σ**.
$${I = (M,Δ)}$$


### Fitness Function
Considering we are working only with Natural numbers and *c* is:
$${c = \frac{n(n²+1)}{2}}$$
And *a* is an element of the square which can be represented by a squared matrix *M* of size *n*:

$${M = \begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\
a_{21} & a_{22} & \dots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & \dots & a_{nn}
\end{bmatrix}}$$

To consider an square a  **High-Quality Magic Square** we must ensure that the following conditions are met.

$${\sum^n_{i=1}a_{ij}=c ,
\sum^n_{j=1}a_{ij}=c,
\sum^n_{i=1}a_{ii}=c,
\sum^n_{i=1}a_{i(n-i+1)}=c}$$

So we can define the next fitness function using this last restrictions:

$${f(M)= \sum^n_{i=1}\lvert c-\sum^n_{k=1}a_{ik}\rvert+
\sum^n_{j=1}\lvert c- \sum^n_{k=1}a_{kj}\rvert+
\lvert c-\sum^n_{i=1}a_{ii}\rvert+
\lvert c-\sum^n_{i=1}a_{i(n-i+1)}\rvert}$$

### Selection Operator

We may use the **rulette method** or **stochastic universal sampling** for selecting the individuals that will be having offspring.

In this operator we must calculate the probability of each individual to get selected base on the evaluation of all the individuals and the fitness function. Following the method used by X. Cui et al. [2], we will use the next formula to calcullate each of:

$${p(I_n)= \frac{\frac{1}{f(M_n)}}{∑^n_{m=1}\frac{1}{f(M_m)}}}$$

Taking into account that if we get an *f = 0* we have found a magic square, the we should stop the execution of the algorithm and return this one

Once we have the all the probabilities *p* for each individual, we shall calculate the distance between selected individuals and a random starting point.

### Mutation Operator

As we are using an Evoluitonary Estrategy, we do not have a crossover operator, so the only way we can explore/explote new solutions in our space is by mutation. This leads to kind of a random search.

We will call *I'* to the offspring of *I* we will also have *M'* and *Δ'* :

$${I=(M,Δ)→I'=(M',Δ')}$$

Both *M'* and *Δ'* will have the updated values of each value *a* and its correspondig mutation variance. In each generation some individuals will randomly be selected to mutate based on `p_mutation` which is the probability to be selected to enter the mutation operator.

Once an Individual is selected to mutate, randomply the algorithm will select a value a and will change the offspring's value based on the following calculation:

$${a'_{ij} = a_{ij}+rand(-σ_{ij},σ_{ij})}$$

Being *rand(a,b)* a funtion that calculates a natural number between *a* and *b*. Also we have to take care about generating numbers out of range, so if any number is bellow 1, we shound use:

$${a'_{ij} = rand(1,n)}$$

In the same way, if we reach a value above n^2 we must:

$${a'_{ij} = n^2 - rand(0,n)}$$

Next we will have to search the new generated value and sustitude its value with *a*'s original value so we can still have all diferent numbers.

Finally, we will have to udate the values of our *σ*, the way of doing this is by:

$${σ'_{ij} = σ_{ij} + rand(-1,1)}$$
$${σ'_{ij} < 1 → σ'_{ij}=1}$$

## Conclusions of the Simple Evolutionary Algorithm

Now, we have every operator implemented, we have tried to solve small **High-Quality Magic Squares**. And we have not succeed at all.

Observing the algorithm behavior we can asume the next things:

*   If we increase the probability of a mutation to happen, the averge and minimun values of the fitness for each epoch behavior is more erratic and we will search in our solution space randomly, so we must choose a small mutation probability.
*   At this moment it has an extreme cost to generate low order high-quality magic squares.
*   Our individuals' fitness indicates that we are searching almost in a random way, so we are far away from the objective.

After a coulple of experiments, we can asume this algorithm can generate magic squares, but at a extreme cost and only in squares of low order (3 and 4)In T. Xie's paper the author says:

> A simple evolutionary algorithm hardly succeeds in
constructing magic squares of orders more than 10, and
the evolving efficiency and the success rate are also
extremely low. [1]

We must search for another method tha can generate bigger squares. The way of doing this will be on separating the problem in multiple steps that are simplier.

## Improved Evolutionary Algorithm

Both papers T. Xie [1] and X. Cui [2] propose a two step algorithm that first find a **Inferior Magic Square**(only the sum of each colum and each row is the same) using a very similar algorithm to the one already implemented in this file which alters the fitness function, and later using another Genetic Algorithm it make permutation to transform the output of the first part into an **High-Quality Magic Square**.

In order to make this algorithm to work we will add two parameters to each individual `n_cols` and `n_rows` this two indicates the number of columns and rows respectively that do not satisfy the magic sum. this change has already been added in the first implementation, but not the method to update these values.

### First Evolution Fitness Function

In this stem we basically take the model implemented previously and change the fitness funtion in order to only satisfy the first two conditions of the magic squares, making our constrains be:

$${\sum^n_{i=1}a_{ij}=c ,
\sum^n_{j=1}a_{ij}=c}$$

Making a fitness funciton based on these two rules:

$${f(M)= \sum^n_{i=1}\lvert c-\sum^n_{k=1}a_{ik}\rvert+
\sum^n_{j=1}\lvert c- \sum^n_{k=1}a_{kj}\rvert}$$

### First Evolution Mutation Operator
As the seletion operator still the same, I will not implement it again. But the mutation operator is subject to change.

Looking at our old mutation operator we observe that most of the time the operator choose to change numbers that are in a correct position, so we need to make our operator to mutate over the numbers that do not satisfy our objective. We can clasify our values contained in *M* as three diferent types:


*   **Type 1** → Elements that do not satisfy both condition
*   **Type 2** → Elements that do not satisfy any condition
*   **Type 3** → Elements that satisfy both conditions

The mathematical way of representing this types as sets S numbers is:

```math
S_1 = \{ a_{ij} : \sum_{k=1}^{n}a_{ik} \neq c, \sum_{k=1}^{n}a_{kj} \neq c, 1 \leq i,j \leq n \}
```

```math
$${S_2 = \left\{ a_{i*}: \sum^n_{k=1}a_{ik}\neq c,1 \leq i\leq n\right\} \cup \left\{ a_{*j}: \sum^n_{k=1}a_{kj}\neq c,1 \leq j\leq n\right\}}$$
```

```math
$${S_3 = \left\{ a_{i*}: \sum^n_{k=1}a_{ik}= c,1 \leq i\leq n\right\} \cap \left\{ a_{*j}: \sum^n_{k=1}a_{kj}= c,1 \leq j\leq n\right\}}$$
```

Istead of creating a method that creates the first two set by giving an individual, we will update the `ns_update_pre` mehtod and create `ns_update`, that apart from updating `n_rows` and `n_cols` also returns *S1* and *S2* lists

Depending on the sets *S1* and *S2* the individual can perfon 3 diferent permutations as our mutation operator, each permutation with a diferent probability based on `n_rows` and `n_cols`.

#### First Permutation
The algorithm chooses a random number in the *S1* set and mutates the same way we did in the single mutation operator. If the value given by the mutation is contained in *S2* the algorithm swaps them, if not, the mutated value will be replaced by the nearest element in *S2*. The probability of this permutation to happend is:

$${p_{m} = \frac{1}{n_{row}n_{col}}}$$

#### Second Permutation
The procedure in the second permutation is the same as the first but instead of choosing our value to mutate from *S1* we take it from *S2* and the same way, swaping it with the nearest of the mutated from *S3*. The probability of this permutation to happend is per row:

$${p_{m} = \frac{1}{nn_{col}} + \frac{1}{nn_{row}}}$$

#### Third Permutation
Quite similar to the last two, but this time we choose a number from *S2* mutate it, then swap it with the number obtained no mater if it is not contained in *S1* or *S2*. The probability of this permutation to happend the same as the second permutation:

$${p_{m} = \frac{1}{nn_{col}} + \frac{1}{nn_{row}}}$$

#### Updating σ Values

As we did in the Simple Evolutionary Algorithm we must change the values of our diferent σ but altering this last behaivour. In all three permutations we will update them the same way. Also we will be adding as a parameter global deviation σₜ.

$${σ'_{ij} = σ_{ij} + rand(-1,1)}$$
$${σ'_{ij} < 1 → σ'_{ij}=rand(1,σ_t)}$$
$${σ'_{ij} > σ_t → σ'_{ij}=rand(1,σ_t)}$$

And later we must calculate our global deviation σₜ:

$${σ_t = \frac{1}{n_{col}+n_{row}}\left(\sum^n_{i=1}\lvert c-\sum^n_{k=1}a_{ik}\rvert+
\sum^n_{j=1}\lvert c- \sum^n_{k=1}a_{kj}\rvert\right)}$$

### Selection Operator

We will use a selector that gets only the best n solution's eliminating the stochastic method by this deterministic.

Once this first part is tested we must implement the second one, but we can observe that the cost is quite big compared to T. Xie et al. paper[1]. Diggin up in their implementation, they allso add a method that do some extra permutations when the solution converges. They call this mechanism 'Local Rectification'
### Local Rectification of Rows and Columns
As it is said in the paper mentioned [1]:



> At the late stage of an evolutionary algorithm, evolution usually stagnates or periodically oscillates. If the heuristics of magic square can be used to locally rectify the intermediate configuration in the late stages of both the two phases, the locally searching efficiency can be greatly improved.

>By a process of analyzing all rows and columns, a local
rectification is made if two rows or columns can meet the
magic sum when more than one pair of numbers is
interchanged.

So lets make this change in our algorithm.

The first type of local rectification over columns and rows is **swapping one pair of values** that are in the same column/row that are the values needed in the other column/row:

Being *k* and *l* two rows and *s* a column that contains two numbers that can be swapped.

$${\sum^n_{i=1}a_{ki}-c =c-\sum^n_{j=1}a_{lj} = a_{ks}-a_{ls}}$$

Happens the same with *k* and *l* as columns and *s* as a row.

$${\sum^n_{i=1}a_{ik}-c =c-\sum^n_{j=1}a_{jl} = a_{sk}-a_{sl}}$$

Furthermore, we can make another type of swap for our rows and columns, these can **swap two pair of values**.

The same way, this two pairs must be in the rows *k* and *l* and will correspond to the columns *s* and *t*.

$${\sum^n_{i=1}a_{ki}-c =c-\sum^n_{j=1}a_{lj} = a_{ks}+a_{kt}-a_{ls}-a_{lt}}$$

And with the cols *k* and *l* with columns *s* and *t*.

$${\sum^n_{i=1}a_{ik}-c =c-\sum^n_{j=1}a_{jl} = a_{sk}+a_{tk}-a_{sl}-a_{tl}}$$

Yet on the point we are right now, we can obtain **Low-Quality Magic Squares** under order of **30** almost all the times we execute the code. As I do not want to keep improving we can move to the second part of the algorithm.

### Second Evolution
Now we need to add our last two restirctions to the magic squares in order to find a **High-Quality** or **Full Magic Square**

$${\sum^n_{i=1}a_{ii}=c,
\sum^n_{i=1}a_{i(n-i+1)}=c}$$

In this part we will not use any random number mutation because this can lead to break the previous non **High-Quality Magic Squares** which are the base of the final ones.

As said before we must declare a new fitness funtion for the diagonals, this is:

$${f(M)= \lvert c-\sum^n_{i=1}a_{ii}\rvert+
\lvert c- \sum^n_{k=i}a_{i,(n-i+1)}\rvert}$$

Also we need to add to our individual implementation `d1` and `d2` which determines if the squares diagonals sum up to *c* in the way:

$${\sum^n_{i=1}a_{ii}=c → d_1 = 0, \sum^n_{i=1}a_{ii}\neq c → d_1 = 1}$$

$${\sum^n_{i=1}a_{i(n-i+1)}=c → d_2 = 0, \sum^n_{i=1}a_{i(n-i+1)}\neq c → d_2 = 1}$$

### Second Evolution Mutation Operator
This operator is simplier than the first mutation operator, as we want to keep the sum values for our rows and columns, we will search the diagonals by permuting rows and columns so each elemnt will stay in the same row/column even if we move it.

As told, we have two new permutations that will make the mutation operator work.
* Row Permutation → As it is named, this method will permutate two rows of the individual's matrix *M*.
* Column Permutation → Basically it is the same as the row permutation but with columns.

Our operator will randomly choose two rows/columns and swap them in the individual's genoma (matrix).

This operator will be used while:

$${n_{col} + n_{row} = 0,\space d_1 + d_2 \geq 1}$$

### Local Rectification of Diagonals
Also it is posible to implement local rectification for our diagonals as we did for the columns and rows. We have the next 5 rectifications:

#### 1. Row Swap to Correct Diagonals
Row $i$ is swapped with row $j$ if the resulting change in both diagonals exactly matches the error they need to correct.

$$(a_{ii}+a_{jj})-(a_{ij}+a_{ji}) = \sum_{k=1}^{n}a_{kk}-c \quad \text{and}$$

$$(a_{i,n-i+1}+a_{j,n-j+1})-(a_{i,n-j+1}+a_{j,n-i+1}) = \sum_{k=1}^{n}a_{n-k+1,k}-c$$

#### 2. Column Swap to Correct Diagonals
Similarly, column $i$ is swapped with column $j$ if the following conditions for both diagonals are met.

$$(a_{ii}+a_{jj})-(a_{ij}+a_{ji}) = \sum_{k=1}^{n}a_{kk}-c \quad \text{and}$$

$$(a_{n-i+1,i}+a_{n-j+1,j})-(a_{n-j+1,i}+a_{n-i+1,j}) = \sum_{k=1}^{n}a_{n-k+1,k}-c$$

#### 3. Symmetrical Row Swap
Row $i$ is swapped with its symmetrical row $(n-i+1)$ if the change in the main diagonal equals its error, and this error is opposite to that of the inverse diagonal.

$$(a_{ii}+a_{n-i+1,n-i+1})-(a_{i,n-i+1}+a_{n-i+1,i}) = \sum_{k=1}^{n}a_{kk}-c = c-\sum_{k=1}^{n}a_{n-k+1,k}$$

#### 4. 4-Point Swap (Main Diagonal)
A localized swap of four numbers is performed to correct the main diagonal if the following equality is met.

$$(a_{ii}+a_{jj})-(a_{ij}+a_{ji}) = \sum_{k=1}^{n}a_{kk}-c$$

#### 5. 4-Point Swap (Inverse Diagonal)
Analogously, another four-number swap is performed to correct the inverse diagonal if this condition is met.

$$(a_{i,n-i+1}+a_{n-j+1,j})-(a_{ij}+a_{n-j+1,n-i+1}) = \sum_{k=1}^{n}a_{n-k+1,k}-c$$


## Conclusions
Following the recipe written in 2003 of T. Xie [1] we did not get results as good as the author but, indeed, we ended up with a more than suficient implementation of a Magic Square Generator.

We successfully generated squares of order 40 in approximately 4 hours and 15 minutes. While this might seem time-consuming, comparing it to a brute force search reveals it is infinitely more efficient. For a 40x40 square, there are $1600!$ (factorial of 1600) possible combinations.

$$1600! \approx 2.09 \times 10^{4432}$$

To put this number into perspective, let us make an exceedingly optimistic assumption about computational speed. Let us assume a hypothetical supercomputer capable of evaluating one trillion ($10^{12}$) combinations per second. The total time required in years would be calculated as:

$$\text{Time (years)} = \frac{2.09 \times 10^{4432} \text{ combinations}}{10^{12} \text{ comb/s} \times 31,536,000 \text{ s/year}} \approx 6.6 \times 10^{4412} \text{ years}$$

For context, the estimated age of the universe is approximately 13.8 billion years.

$$\text{Age of Universe (years)} \approx 1.38 \times 10^{10}$$

Therefore, the time necessary to find a 40x40 magic square by brute force is exponentially greater than the age of the universe, rendering such an approach computationally infeasible.

### Performance Comparison

| Order ($N$) | Search Space ($N^2!$) | Brute Force Time (Est.) | **My Algorithm Time** |
|:---:|:---:|:---:|:---:|
| **8** | $1.2 \times 10^{89}$ | $> 10^{80}$ years | **2.6 s** |
| **10** | $9.3 \times 10^{157}$ | $> 10^{140}$ years | **8.8 s** |
| **15** | $5.9 \times 10^{432}$ | $> 10^{410}$ years | **41.5 s** |
| **20** | $6.4 \times 10^{868}$ | $> 10^{850}$ years | **4 min 15 s** |
| **30** | $1.4 \times 10^{2274}$ | $> 10^{2250}$ years | **22 min** |
| **40** | $2.1 \times 10^{4432}$ | $> 10^{4400}$ years | **4 h 15 min** |

---

However, in related literature, some authors mention the ability to create squares of order 100. Without doubting their research, the important points where my implementation could be improved are:

* **Language:** Implement the algorithm in a compiled language such as C, C++, or Java instead of Python (interpreted).
* **Debugging:** Perform a deep search for potential bottlenecks or logic errors in the current implementation.
* **Optimization:** Refine the fitness function and mutation operators for more efficient computing.
* **Concurrency:** Implement parallel processing to evaluate multiple individuals simultaneously.
* **Libraries:** Utilize dedicated evolutionary computation libraries such as *DEAP*, *PyGAD*, or *EvoPy* instead of a custom implementation.
* **Metaheuristic:** Beyond comparing to T. Xie et al., research different metaheuristics (e.g., Simulated Annealing, Ant Colony) that might solve this specific combinatorial problem more efficiently.
