---
aliases: ["EWC"]
type: concept
element_type: method
topic: "[[Information geometry and natural-gradient optimization]]"
topics: ["[[Information geometry and natural-gradient optimization]]"]
created: 2026-09-19
---

## Working definition

A continual-learning regularizer that adds a quadratic penalty anchoring each weight to its value after earlier tasks, with a stiffness set by the diagonal Fisher information, so weights important to old tasks change slowly while the rest stay free to learn.

## Evidence

- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-006]] — Elastic weight consolidation slows down learning on certain weights based on how important they are to previously seen tasks.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-008]] — EWC implements its constraint as a quadratic penalty, imagined as a spring anchoring parameters to the previous task's solution.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-009]] — The stiffness of the EWC spring should be greater for parameters that matter most to performance on the previous task.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-015]] — For a third task, EWC keeps parameters close to both previous solutions, via two penalties or one combined quadratic penalty.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-021]] — With EWC, the network can learn task B well without forgetting task A in the permuted MNIST experiment.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-024]] — EWC allows a large number of permuted MNIST tasks to be learned in sequence, with only modest growth in error rates.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-032]] — The authors state that the EWC approach uses a single network with fixed capacity and has minimal computational overhead.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-042]] — By using EWC, the Atari agents do learn to play multiple games within the sequential training schedule.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-054]] — EWC has a run time which is linear in both the number of parameters and the number of training examples.
- [[Kirkpatrick2016overcoming - Overcoming catastrophic forgetting in neural networks#^kirkpatrick2016overcoming-055]] — The authors call the point estimate of the posterior's variance, as in a Laplace approximation, a significant weakness of EWC.
- [[Matena2021merging - Merging Models with Fisher-Weighted Averaging#^matena2021merging-064]] — Elastic weight consolidation also uses the Laplace approximation to the posterior, creating a regularizer to prevent catastrophic forgetting in continual learning.
- [[Matena2021merging - Merging Models with Fisher-Weighted Averaging#^matena2021merging-065]] — The authors argue that EWC keeps a model from losing acquired knowledge, whereas merging directly adds new knowledge to a model.

## Relations


## Open questions

## History

- 2026-09-19 · Eki Gonzalez Flamarique · created: top-down (2 sources) · topic: Information geometry and natural-gradient optimization (drafter's packet `q4-geometric-finetuning`, confirmed at the gate)
