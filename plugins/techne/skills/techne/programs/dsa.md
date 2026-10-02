---
id: dsa
title: DSA
version: 2
activity_kinds: code, oral, writing
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=30, review=5, placement=15
red_thread: no
survey_ceiling: discovered
---

# DSA

## Outcome and boundary

For a TypeScript developer who wants to pass the algorithms and data structures rounds of technical
interviews comfortably: read an unseen problem, recognise which structure or pattern it calls for, state an
approach and its complexity before coding, write a correct solution from a blank file in about 30 minutes,
and test it out loud. Understanding comes first: every structure is implemented by hand before the built-in
one is used, and every complexity is justified, not recited.

All code is TypeScript, run with `node --test`. JavaScript has no built-in heap, deque or balanced tree, so
the learner writes them; by the end, the exercises form the learner's own tested library of structures.

The spine follows MIT 6.006 (Spring 2020). Lessons draw on Open Data Structures and Runestone's *Problem
Solving with Algorithms and Data Structures*; deeper material on CP-Algorithms; exercises and assessments on
the MIT problem sets and exams and on Berkeley CS61B. Implementations from TheAlgorithms are shown only after
the learner's own implementation passes its tests, as a comparison, never before. Python examples from the
sources are transposed to TypeScript.

Deliberately out of scope: competitive-programming speed and contest-only techniques (heavy-light
decomposition, suffix automata, flows, geometry), formal proofs beyond what an interview asks for (an
invariant, an exchange argument, a recurrence), and system design. Number theory and a few advanced trees
are surveyed only, because they rarely come up in interviews.

The program stands alone: a stranger can follow it without any other. It keeps its own evidence; what was
demonstrated in another program does not count here.

## Sequence

### Unit 1 — Complexity and the cost model

- The word-RAM cost model, what counts as one step, hand-tracing a loop.
- Big-O, Big-Θ, Big-Ω; logarithms, arithmetic and geometric sums; reading the complexity off nested loops.
- Space complexity, including the call stack.
- Amortised analysis on a dynamic array: why `push` is O(1) amortised. Implement a growable array.

### Unit 2 — Arrays, strings and the interview method

- Array and string operations and their costs in JavaScript; strings are immutable.
- The interview method: clarify, write examples, state a brute force with its cost, optimise, code, test by
  hand. Practised on every problem from here on.
- Two pointers on sorted arrays and from both ends; in-place partitioning.

### Unit 3 — Hashing

- Hash functions, chaining, open addressing, load factor and resizing. Implement a hash map.
- `Map` and `Set` in JavaScript and why a plain object is not the same thing.
- Patterns: frequency counting, complement lookup, grouping by a computed key, deduplication.

### Unit 4 — Sliding window and prefix sums

- Fixed and variable sliding windows, with a hash map for window contents.
- Prefix sums, difference arrays, and prefix sums combined with a hash map (subarray sum equals k).

### Unit 5 — Linked structures

- Singly and doubly linked lists, sentinel nodes. Implement both.
- Reversal, merging, fast and slow pointers (middle, cycle detection), removing the n-th from the end.

### Unit 6 — Stacks, queues and deques

- Stack, queue and deque as interfaces; implementations on an array, a circular buffer and a linked list.
- Balanced brackets, expression evaluation, monotonic stack (next greater element), queue built from two
  stacks.

### Unit 7 — Recursion

- Base case, recursive case, the call stack; recursion versus iteration.
- Recurrences and their solutions (linear, halving, branching); a working version of the master theorem.
- Divide and conquer as a shape of recursion.

### Unit 8 — Binary search

- Binary search on a sorted array with an explicit invariant; lower and upper bounds.
- Binary search on the answer (minimum feasible value), on rotated arrays, and on a monotone predicate.

### Unit 9 — Sorting

- Insertion and selection sort; merge sort and quicksort with their recurrences; stability; the
  comparison lower bound.
- Counting sort and radix sort. The JavaScript `sort` comparator and its pitfalls with numbers.
- Sorting as a preprocessing step that unlocks two pointers or greedy.

### Unit 10 — Trees and binary search trees

- Binary trees: recursive and iterative traversals (pre, in, post order), level-order with a queue, height,
  diameter, lowest common ancestor.
- Binary search trees: search, insert, delete, successor, validation. Implement one.
- Balance: why an unbalanced BST degrades, AVL rotations, what a balanced tree guarantees.

### Unit 11 — Heaps and priority queues

- Binary heap in an array: sift up, sift down, heapify in O(n). Implement a priority queue with a
  comparator.
- Heapsort. Patterns: top-k, k-way merge, running median with two heaps, scheduling.

### Unit 12 — Greedy and intervals

- When a greedy choice is safe; the exchange argument.
- Interval problems: merge, insert, minimum rooms, activity selection; sweep line.

### Unit 13 — Backtracking

- The choose / explore / unchoose shape; subsets, permutations, combinations.
- Pruning; constraint problems (N-queens, word search on a grid).

### Unit 14 — Graph traversal

- Representations: adjacency list, adjacency matrix, implicit graphs and grids.
- BFS and unweighted shortest paths; DFS, connected components, cycle detection in directed and undirected
  graphs; topological sort (DFS and Kahn's algorithm); bipartite check.

### Unit 15 — Weighted graphs and disjoint sets

- Shortest paths: relaxation, DAG shortest paths, Dijkstra with a heap, Bellman-Ford and negative cycles.
- Disjoint set union with union by rank and path compression. Implement it.
- Minimum spanning tree: Kruskal and Prim.

### Unit 16 — Dynamic programming

- Subproblems, relation, topological order, base cases, original problem, time (MIT's SRTBOT); memoisation
  versus tabulation.
- One-dimensional DP (climbing stairs, house robber, coin change); grid DP; knapsack; longest increasing
  subsequence; longest common subsequence and edit distance; DP on intervals.
- Reconstructing the solution, not only its value; reducing memory.

### Unit 17 — Advanced structures and strings

- Trie: insert, search, prefix queries, autocomplete.
- Fenwick tree and segment tree for range queries with point updates.
- String matching: KMP prefix function and Rabin-Karp rolling hash.

### Unit 18 — Interview simulation

- Timed mixed problems with the pattern unannounced: the learner must recognise it.
- Full mock interviews: written approach first, then code, then hand-testing and complexity, then a
  follow-up question that changes a constraint.

## Subject catalogue

### Complexity — `algcx.*`

`cost-model`, `hand-tracing`, `asymptotic-notation`, `math-for-complexity`, `nested-loop-analysis`,
`space-complexity`, `amortised-analysis`, `dynamic-array`

### Arrays, strings and patterns — `algpat.*`

`array-operations`, `string-operations`, `interview-method`, `two-pointers`, `in-place-partition`,
`sliding-window-fixed`, `sliding-window-variable`, `prefix-sums`, `difference-arrays`

### Hashing — `alghash.*`

`hash-functions`, `chaining`, `open-addressing`, `load-factor-resizing`, `hash-map-implementation`,
`js-map-set`, `frequency-counting`, `complement-lookup`, `grouping-by-key`

### Linear structures — `alglin.*`

`singly-linked-list`, `doubly-linked-list`, `sentinel-nodes`, `list-reversal`, `fast-slow-pointers`,
`stack`, `queue`, `deque`, `circular-buffer`, `bracket-matching`, `monotonic-stack`

### Recursion and search — `algrec.*`

`recursion-basics`, `recurrences`, `master-theorem`, `divide-and-conquer`, `binary-search`,
`binary-search-bounds`, `binary-search-on-answer`, `backtracking`, `pruning`

### Sorting — `algsort.*`

`elementary-sorts`, `merge-sort`, `quicksort`, `stability`, `comparison-lower-bound`, `counting-sort`,
`radix-sort`, `js-sort-comparator`, `sort-as-preprocessing`

### Trees and heaps — `algtree.*`

`binary-tree-traversals`, `level-order`, `tree-recursion`, `lowest-common-ancestor`, `bst-operations`,
`bst-validation`, `avl-rotations`, `binary-heap`, `heapify`, `priority-queue`, `heapsort`, `top-k`,
`two-heaps`, `trie`, `fenwick-tree`, `segment-tree`

### Greedy — `alggreedy.*`

`greedy-choice`, `exchange-argument`, `interval-merging`, `interval-scheduling`, `sweep-line`

### Graphs — `alggraph.*`

`graph-representation`, `grid-graphs`, `bfs`, `dfs`, `connected-components`, `cycle-detection`,
`topological-sort`, `bipartite-check`, `relaxation`, `dag-shortest-paths`, `dijkstra`, `bellman-ford`,
`disjoint-set-union`, `kruskal`, `prim`

### Dynamic programming — `algdp.*`

`subproblem-design`, `memoisation`, `tabulation`, `one-dimensional-dp`, `grid-dp`, `knapsack`,
`longest-increasing-subsequence`, `sequence-alignment`, `interval-dp`, `solution-reconstruction`,
`memory-reduction`

### Strings — `algstr.*`

`kmp-prefix-function`, `rabin-karp`

### Interview craft — `algiv.*`

`pattern-recognition`, `approach-before-code`, `hand-testing`, `complexity-justification`,
`follow-up-adaptation`, `timed-solving`

### Survey — `algsurvey.*`

`bit-manipulation`, `gcd-euclid`, `sieve-of-eratosthenes`, `modular-exponentiation`,
`all-pairs-shortest-paths`, `bitmask-dp`, `red-black-trees`, `skip-lists`, `a-star`

## Sources

| Source | Role |
| --- | --- |
| https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ | order of the units; problem sets, solutions and exams for exercises and assessments |
| https://www.opendatastructures.org/ | lessons on structures and their implementation |
| https://runestone.academy/ns/books/published/pythonds3/index.html | gentler explanations for lessons, especially complexity, recursion, sorting |
| https://cp-algorithms.com/ | deeper material: DSU, Fenwick, segment tree, strings, shortest paths, survey subjects |
| https://people.eecs.berkeley.edu/~jrs/61b/ | exercise and exam bank |
| https://github.com/TheAlgorithms/TypeScript | comparison implementations, shown after the learner's passes |

## Problem bank

Free LeetCode problems to base exercises on, at `https://leetcode.com/problems/<slug>/`. All slugs were verified to exist and not be paid-only on 2026-09-17. Pick by topic and observed level; the bank is a starting point, not an exhaustive list or a fixed order.

| Topic | Easy | Medium |
| --- | --- | --- |
| Arrays, iteration | `move-zeroes`, `majority-element`, `best-time-to-buy-and-sell-stock` | `merge-intervals` |
| Hashing, `Map`/`Set`, frequency counting | `two-sum`, `contains-duplicate`, `valid-anagram`, `first-unique-character-in-a-string` | `group-anagrams`, `top-k-frequent-elements` |
| Strings | `valid-palindrome`, `find-the-index-of-the-first-occurrence-in-a-string` | `longest-substring-without-repeating-characters` |
| Two pointers | `valid-palindrome`, `move-zeroes` | `two-sum-ii-input-array-is-sorted`, `container-with-most-water` |
| Sliding window | `maximum-average-subarray-i` | `minimum-size-subarray-sum`, `longest-substring-without-repeating-characters` |
| Stack, queue | `valid-parentheses`, `implement-queue-using-stacks` | `min-stack`, `daily-temperatures` |
| Binary search | `binary-search`, `sqrtx` | `search-in-rotated-sorted-array` |
| Recursion | `fibonacci-number`, `climbing-stairs` | — |
| Linked lists | `reverse-linked-list`, `merge-two-sorted-lists` | — |
| Trees, BST | `maximum-depth-of-binary-tree`, `invert-binary-tree` | `validate-binary-search-tree`, `lowest-common-ancestor-of-a-binary-search-tree`, `binary-tree-level-order-traversal` |
| Heaps | `kth-largest-element-in-a-stream`, `last-stone-weight` | `kth-largest-element-in-an-array` |
| Graphs, BFS/DFS | — | `number-of-islands`, `clone-graph` |
| Topological order | — | `course-schedule`, `course-schedule-ii` |

## Adaptation rules

- Every structure is implemented by hand, with tests, before the built-in or a library equivalent is
  allowed in later problems.
- From the interview method onwards, every problem starts with a written approach and its complexity in an
  `APPROACH.md` file next to the exercise, before any code. This is the program's oral work: the learner
  writes what they would say aloud, since questions belonging to an exercise never go through the chat.
- Within a unit, a lesson is followed by an implementation exercise, then by two or three interview problems
  from easy to medium; a hard problem closes the unit once the subject is independent.
- A subject already demonstrated in this program goes straight to a harder problem that uses it.
- Transfer is the unannounced pattern: a problem from an earlier unit reappears inside a later one without
  being named. Recognised and solved without help, it counts as transferred.
- After the trees unit, one timed problem from an earlier unit is mixed into each session.
- Interview simulation is open once graphs and dynamic programming have their bases, and returns
  regularly after that rather than waiting for its unit.
- Survey subjects attach to the lessons of neighbouring units and never get a unit of their own.
