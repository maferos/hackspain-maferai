---
aliases: []
type: concept
element_type: concept
topic: "[[Equivariant networks and rotation representations]]"
topics: ["[[Equivariant networks and rotation representations]]"]
created: 2026-09-18
---

## Working definition

An antipodally symmetric probability distribution on unit quaternions used to express uncertainty over 3D rotations, whose mixtures can represent several plausible orientations at once.

## Evidence

- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-002]] — Rotations are modelled by a mixture of anisotropic Bingham distributions, which the authors describe as well suited to quaternion parameterizations.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-009]] — The closest prior work learns orientation end to end with a Bingham distribution but provides no means of dealing with mode collapse.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-014]] — The Unimodal Bingham Network models the pose by a single Bingham distribution whose entropy serves as a measure of prediction uncertainty.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-015]] — The Multimodal Bingham Network predicts a multimodal Bingham distribution to capture different modes lying in the data, thus dissolving ambiguities.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-018]] — The entropy of the predicted Bingham distribution is passed through a sigmoid to give an uncertainty score in the range (0, 1).
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-019]] — The unimodal network is trained by minimizing the negative log-likelihood of the ground-truth rotation under the predicted Bingham distribution.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-053]] — The authors attribute UBN's improvement to the Bingham distribution enabling an anisotropic distance that accounts for uncertainty in directions.
- [[Mohlin2020probabilistic - Probabilistic orientation estimation with matrix Fisher#^mohlin2020probabilistic-007]] — Another prior method used a Bingham distribution over quaternions, whose parameters have to be positive semidefinite.

## Relations

- RELATES_TO → [[Pose ambiguity from symmetry]]
  · type: solves
  · evidence: [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-015]]

## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: extra (2 sources) · topic: Equivariant networks and rotation representations (drafter's packet `p3-equivariance-rotations`, confirmed at the gate)
