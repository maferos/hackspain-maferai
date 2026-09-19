---
aliases: []
type: "source"
title: "Efficient Analytical Derivatives of Rigid-Body Dynamics using Spatial Vector Algebra"
citekey: "Singh2021efficient"
doi: "10.48550/arXiv.2105.05102"
arxiv: "2105.05102"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2105.05102"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Shubham Singh", "Ryan P. Russell", "Patrick M. Wensing"]
sha256: ["190b2a918d3b2e9bbaefb5c5cd70535655865ae6c525ea7c59ba4327b82bbcf2"]
pdf: "Content/Papers/Singh2021efficient.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Singh2021efficient.pdf]]

> [!abstract] One-sentence summary
> The paper derives closed-form first-order partial derivatives of inverse dynamics for multi-DoF, floating-base rigid-body systems and turns them into the O(Nd) IDSVA algorithm, which outperforms chain-rule methods and Pinocchio's derivative code.

## Abstract

An essential need for many model-based robot control algorithms is the ability to quickly and accurately compute partial derivatives of the equations of motion. State of the art approaches to this problem often use analytical methods based on the chain rule applied to existing dynamics algorithms. Although these methods are an improvement over finite differences in terms of accuracy, they are not always the most efficient. In this paper, we contribute new closed-form expressions for the first-order partial derivatives of inverse dynamics, leading to a recursive algorithm. The algorithm is benchmarked against chain-rule approaches in Fortran and against an existing algorithm from the Pinocchio library in C++. Tests consider computing the partial derivatives of inverse and forward dynamics for robots ranging from kinematic chains to humanoids and quadrupeds. Compared to the previous open-source Pinocchio implementation, our new analytical results uncover a key computational restructuring that enables efficiency gains. Speedups of up to 1.4x are reported for calculating the partial derivatives of inverse dynamics for the 50-dof Talos humanoid. (arXiv)

## 🧠 Key ideas (atomic)

- Robotics libraries such as Crocoddyl and Drake require partial derivatives of rigid-body dynamics with respect to the state and control variables. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-001
- Calculating the derivatives of rigid-body dynamics represents the majority of the CPU time required in many optimal control applications. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-002
- Finite-difference derivatives of rigid-body dynamics suffer in accuracy, despite being simple to implement and trivially parallelized. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-003
- The complex-step method is accurate to machine precision but requires all functions to be computed in the complex plane, adding overhead. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-004
- Automatic differentiation accumulates chain-rule expressions for an algorithm's partials through either operator overloading or source code transformation. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-005
- The earlier chain-rule derivation on the [[Recursive Newton-Euler algorithm|two-pass RNEA]] has O(Nd) complexity, with N bodies and d the depth of the kinematic tree. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-006
- The Pinocchio 2.6.0 code differs from its published algorithm, using a more efficient O(N) forward pass coupled with an O(Nd) backward pass. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-007
- The authors state that derivative algorithms directly carrying out the chain rule on an existing algorithm may not always be the most efficient. (Singh et al., 2021) `ev:asserted` p. 1 ^singh2021efficient-008
- An earlier recursive method for serial chains with single-DoF joints gave an O(N^2) algorithm for the partials of forward dynamics. (Singh et al., 2021) `ev:cited` p. 1 ^singh2021efficient-009
- The main contribution extends previous analytical results on inverse-dynamics partial derivatives to generic multi-DoF joint robots with a fixed or floating base. (Singh et al., 2021) `ev:asserted` p. 1 ^singh2021efficient-010
- To the authors' knowledge, their closed-form first-order inverse-dynamics derivatives are the first for general rigid-body systems with multi-DoF joints. (Singh et al., 2021) `ev:asserted` p. 2 ^singh2021efficient-011
- The new expressions lead immediately to an O(Nd) algorithm that naturally generalizes the earlier single-DoF algorithm of Jain and Rodriguez. (Singh et al., 2021) `ev:asserted` p. 2 ^singh2021efficient-012
- The authors describe their method as fundamentally different from the straight chain-rule approach presented by Carpentier and Mansard. (Singh et al., 2021) `ev:asserted` p. 2 ^singh2021efficient-013
- The distinct algorithm in the Pinocchio code ends up being directly related to the computations required in the proposed algorithm. (Singh et al., 2021) `ev:asserted` p. 2 ^singh2021efficient-014
- The partial derivatives of forward dynamics are ultimately calculated with complexity O(N^2) using the relationship between forward and inverse dynamics. (Singh et al., 2021) `ev:asserted` p. 2 ^singh2021efficient-015
- Table I rates special-purpose analytical methods, including this paper's, as hard to implement yet high in accuracy. (Singh et al., 2021) `ev:asserted` p. 2 ^singh2021efficient-016
- Partials of forward dynamics with respect to the state equal the negative inverse mass matrix times the corresponding partials of inverse dynamics. (Singh et al., 2021) `ev:cited` p. 2 ^singh2021efficient-017
- The [[Recursive Newton-Euler algorithm|RNEA]] and the Articulated-Body Algorithm are the most efficient O(N) algorithms for calculating inverse and forward dynamics respectively. (Singh et al., 2021) `ev:cited` p. 2 ^singh2021efficient-018
- Pinocchio's state-of-the-art forward-dynamics derivatives first compute inverse-dynamics derivatives, then compute the inverse mass matrix and apply Eq. 5. (Singh et al., 2021) `ev:cited` p. 2 ^singh2021efficient-019
- The considered systems are open-chain kinematic trees with serial or branched connectivity, whose N links are joined by joints with up to 6 DoF. (Singh et al., 2021) `ev:reported` p. 3 ^singh2021efficient-020
- The derivative of the joint motion subspace matrix due to the axis changing in local coordinates is assumed to be zero. (Singh et al., 2021) `ev:reported` p. 3 ^singh2021efficient-021
- Instead of treating gravity as an external force, the base is accelerated upwards opposite the gravitational acceleration. (Singh et al., 2021) `ev:reported` p. 3 ^singh2021efficient-022
- For multi-DoF joints such as a floating base, the directional derivatives along each joint free mode are more formally Lie derivatives. (Singh et al., 2021) `ev:asserted` p. 4 ^singh2021efficient-023
- The partial derivatives of joint torques with respect to joint velocities depend only on the Coriolis terms of the equations of motion. (Singh et al., 2021) `ev:computed` p. 5 ^singh2021efficient-024
- Algorithm 1 (IDSVA) returns the inverse-dynamics partials with computational complexity O(Nd), expressing all spatial vectors in ground frame coordinates. (Singh et al., 2021) `ev:reported` p. 5 ^singh2021efficient-025
- When a joint has a single DoF, the forward-pass steps of IDSVA are the same as in Jain and Rodriguez's Algorithm 2. (Singh et al., 2021) `ev:asserted` p. 5 ^singh2021efficient-026
- Lines 17-20 of the IDSVA backward pass restructure a second inner loop of the earlier single-DoF algorithm into matrix multiplies. (Singh et al., 2021) `ev:asserted` p. 5 ^singh2021efficient-027
- Directly multiplying the inverse-dynamics partials by the inverse mass matrix is an O(N^3) operation, named Direct Matrix Multiplication (DMM). (Singh et al., 2021) `ev:asserted` p. 5 ^singh2021efficient-028
- The ABA-Zero-Algorithm (AZA) forms inverse-mass-matrix products by running ABA with zero joint rates and zero gravity on each column vector. (Singh et al., 2021) `ev:reported` p. 6 ^singh2021efficient-029
- Across the repeated ABA calls in AZA, the kinematic variables and articulated inertias are calculated only once and saved for reuse. (Singh et al., 2021) `ev:reported` p. 6 ^singh2021efficient-030
- Forward-dynamics partials from ABACR, FDSVA and FDCR were checked against a Fortran complex-step implementation for accuracy. (Singh et al., 2021) `ev:reported` p. 6 ^singh2021efficient-031
- For N = 100, the ABACR method gave a term-by-term root-mean-square relative error of 10−13 against the complex-step reference. (Singh et al., 2021) `ev:measured` p. 6 ^singh2021efficient-032
- For N = 100, both FDSVA and FDCR gave a root-mean-square relative error of approximately 10−12 against the complex-step reference. (Singh et al., 2021) `ev:measured` p. 6 ^singh2021efficient-033
- The root-mean-square relative error of all tested methods grows linearly with DoF on a log-log scale. (Singh et al., 2021) `ev:measured` p. 6 ^singh2021efficient-034
- The Fortran benchmarks used N-link serial or branched kinematic trees with all revolute joints about their local z-axis. (Singh et al., 2021) `ev:reported` p. 6 ^singh2021efficient-035
- The Fortran 90 algorithms were built with the Intel Fortran compiler and run on a 3.07 GHz Intel Xeon processor. (Singh et al., 2021) `ev:reported` p. 6 ^singh2021efficient-036
- Average run times were obtained by running each algorithm 10,000 times with randomized inputs for the state and control variables. (Singh et al., 2021) `ev:reported` p. 6 ^singh2021efficient-037
- For N = 100, the Fortran implementation of IDSVA achieved a speedup of 15× over the chain-rule RNEACR method. (Singh et al., 2021) `ev:measured` p. 6 ^singh2021efficient-038
- In the Fortran benchmarks on serial chains, the FDSVA method outperforms FDCR for all values of N ≥2. (Singh et al., 2021) `ev:measured` p. 6 ^singh2021efficient-039
- Ground-coordinate algorithms avoid repeated transformation of quantities between local body frames in the backward pass, at the cost of ground-frame kinematics. (Singh et al., 2021) `ev:asserted` p. 6 ^singh2021efficient-040
- Ground-coordinate IDSVA gave speedups between 1.3 to 1.9 over body-coordinate IDSVA for N = 2 to N = 500. (Singh et al., 2021) `ev:measured` p. 6 ^singh2021efficient-041
- IDSVA in ground coordinates was implemented in C++ within the Pinocchio framework to compare directly with Pinocchio's original inverse-dynamics derivatives. (Singh et al., 2021) `ev:reported` p. 6 ^singh2021efficient-042
- For a serial chain with N = 100, IDSVA C++ gave a speedup of 2× over Pinocchio ID Derivs using the gcc-9.0 compiler. (Singh et al., 2021) `ev:measured` p. 6 ^singh2021efficient-043
- With the gcc-9.0 compiler, IDSVA C++ improves upon Pinocchio ID Derivs for all N ≥2 on serial and branched trees. (Singh et al., 2021) `ev:measured` p. 7 ^singh2021efficient-044
- For the 50 link floating-base Talos humanoid, IDSVA has a speedup of 1.4x over Pinocchio ID Derivs using gcc-9.0. (Singh et al., 2021) `ev:measured` p. 7 ^singh2021efficient-045
- The multi-DoF C++ benchmarks covered the UR3, HyQ, Baxter, ATLAS and Talos models with gcc-9.0 and LLVM Clang-10 compilers. (Singh et al., 2021) `ev:reported` p. 7 ^singh2021efficient-046
- The authors attribute the speedups to IDSVA using a subtree matrix-matrix multiplication instead of Pinocchio's O(d) innermost backward pass over ancestors. (Singh et al., 2021) `ev:asserted` p. 7 ^singh2021efficient-047
- The authors report that this backward-pass restructuring has been included in more recent releases of the Pinocchio library. (Singh et al., 2021) `ev:asserted` p. 7 ^singh2021efficient-048
- An open source Pinocchio implementation of IDSVA is publicly available, with a separate MATLAB version in the spatial_v2_extended repository. (Singh et al., 2021) `ev:reported` p. 7 ^singh2021efficient-049
- The crossover N below which DMM outperforms AZA depends on the hardware and compiler optimization settings used for implementation. (Singh et al., 2021) `ev:asserted` p. 7 ^singh2021efficient-050
- For high N, the O(N^2) AZA is efficient because it avoids the expensive matrix-matrix product required by DMM. (Singh et al., 2021) `ev:asserted` p. 7 ^singh2021efficient-051
- In the Pinocchio C++ framework with gcc-9.0, the DMM versus AZA comparison shows the cross-over N at 50. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-052
- The speedup of AZA over DMM grows linearly with n on a log-log scale for the tested kinematic trees. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-053
- With autovectorization off, the cross-over N above which AZA beats DMM is 80 for the clang-10 compiler. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-054
- With autovectorization on, the cross-over N above which AZA beats DMM rises to 450 for gcc-9.0. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-055
- With autovectorization on, the cross-over N above which AZA beats DMM is 350 for the clang-10 compiler. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-056
- The FDSVA C++ runtime curve changes order from O(N^3) to O(N^2) at N = 50, where DMM switches to AZA. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-057
- FDSVA C++ outperforms Pinocchio FD Derivs for the first-order forward-dynamics partials at all N on serial and branched trees. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-058
- The conclusions report a 1.2× speedup for the TALOS humanoid model over Pinocchio when using the Clang-10 compiler. (Singh et al., 2021) `ev:measured` p. 8 ^singh2021efficient-059
- The authors state the reduced runtime for partial derivatives enables faster optimization algorithms for both on-line and off-line applications. (Singh et al., 2021) `ev:asserted` p. 8 ^singh2021efficient-060
- The authors suggest these improved timings can ultimately lead to better motion planning of legged and industrial robots. (Singh et al., 2021) `ev:asserted` p. 8 ^singh2021efficient-061

## 🎯 Contributions

## 📖 Glossary

- **Inverse dynamics (ID)** — computes the joint torques needed for given positions, velocities and accelerations.
- **Forward dynamics (FD)** — computes joint accelerations produced by given torques at a fixed state.
- **RNEA** — Recursive Newton-Euler Algorithm; O(N) two-pass recursion for inverse dynamics.
- **ABA** — Articulated-Body Algorithm; O(N) recursion computing forward dynamics.
- **Spatial Vector Algebra (SVA)** — 6D vector formalism combining linear and angular motion or force quantities.
- **Motion subspace matrix** — maps a joint's rates to the spatial velocity it allows.
- **IDSVA** — the paper's recursive algorithm for first-order inverse-dynamics partials using SVA.
- **FDSVA** — forward-dynamics partials via IDSVA, inverse mass matrix, and DMM or AZA.
- **AZA** — ABA-Zero-Algorithm: ABA with zero velocity and gravity to multiply by inverse mass matrix.
- **DMM** — Direct Matrix Multiplication of inverse mass matrix and inverse-dynamics partials, O(N^3).
- **Complex-step method** — derivative technique evaluating functions with complex perturbations, accurate to machine precision.
- **Kinematic tree depth (d)** — the maximum number of bodies on a path from base to leaf.

## ❓ Open questions

- Can the closed-form approach extend to second-order partial derivatives of inverse and forward dynamics?
- How do IDSVA and FDSVA handle closed kinematic loops or contact constraints, which the open-chain treatment excludes?
- How does IDSVA compare with automatic-differentiation or code-generation pipelines (e.g. CasADi, Drake AD) on the same hardware?
- What is the end-to-end effect of the speedup inside an MPC or trajectory-optimization loop, rather than on isolated derivative calls?
- Can the DMM/AZA cross-over be chosen automatically for a given compiler and hardware configuration?

## 📝 Notes on reading

Read the arXiv v3 (10 Jan 2022), which carries the IEEE RA-L copyright notice and DOI 10.1109/LRA.2022.3141194; the packet identifier is the arXiv DOI.

Figures 2-7 are runtime and speedup plots whose values were only described, not claimed; the axis tick labels in the extraction are unreadable as data. Fig. 4b's speedup axis spans roughly 1.2 to 2.2 and Fig. 6b's roughly 2 to 4; per-robot runtimes in Fig. 5 (UR3, HyQ, Baxter, ATLAS, Talos) were not claimed.

Inconsistency: the body (p. 7) and abstract attribute the 1.4x Talos speedup to Pinocchio ID Derivs (inverse dynamics), while the conclusions (p. 8) state it is over the 'state-of-the-art Pinocchio FD derivatives'.

Section VI, 'Implementation Considerations', has a heading but no text in this version. On p. 4 the main-text derivation refers to 'Eq. 80', which is an appendix equation; the main text numbering jumps. The p. 6 text misspells Pinocchio as 'Pinochhio'. The intro cites the Jain and Rodriguez O(Nd) ID-partials algorithm; that half of the sentence was not claimed separately.

The equations (closed-form partials, Eqs. 25-32, and appendix identities J1-J9) are partly garbled by extraction; their content is summarised only at the level of complexity and structure.

## Suggested new concepts

- Analytical derivatives of rigid-body dynamics — a recurring need for MPC, trajectory optimisation and differentiable simulation, with several competing method families.
- Spatial Vector Algebra — the Featherstone 6D formalism underlying RNEA, ABA and most efficient dynamics code.
- Pinocchio — widely used C++ rigid-body dynamics library that several vault sources benchmark against.
- Recursive Newton-Euler Algorithm — the core O(N) inverse-dynamics recursion that derivative methods build on.
- Articulated-Body Algorithm — the O(N) forward-dynamics recursion, reused here for inverse-mass-matrix products.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H1.** Derivadas cerradas y recursivas de la dinámica inversa para juntas que son grupos de Lie, necesarias para DDP y ajuste por gradiente.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
