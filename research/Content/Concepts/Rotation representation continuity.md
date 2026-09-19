---
aliases: ["rotation continuity"]
type: concept
element_type: concept
topic: "[[Equivariant networks and rotation representations]]"
topics: ["[[Equivariant networks and rotation representations]]"]
created: 2026-09-18
---

## Working definition

Whether the map from a rotation to the vector a network predicts is continuous, a property no representation of 3D rotations in four or fewer dimensions (Euler angles, axis-angle, quaternions) can have, and whose absence hampers learning when rotations are the network output.

## Evidence

- [[Zhou2019continuity - On the Continuity of Rotation Representations in Neural#^zhou2019continuity-009]] — The authors argue continuous rotation representations are a better choice when real-world tasks require networks to output the full range of rotations.
- [[Zhou2019continuity - On the Continuity of Rotation Representations in Neural#^zhou2019continuity-014]] — The authors argue that discontinuous representations can be harder for neural networks to fit than continuous representations.
- [[Zhou2019continuity - On the Continuity of Rotation Representations in Neural#^zhou2019continuity-022]] — The authors conclude that no continuous representation of 3D rotations exists in real Euclidean spaces of four or fewer dimensions.
- [[Mohlin2020probabilistic - Probabilistic orientation estimation with matrix Fisher#^mohlin2020probabilistic-005]] — Earlier work on rotation continuity shows that any rotation representation with four or fewer dimensions is discontinuous, making network generalization over rotations difficult.
- [[Mohlin2020probabilistic - Probabilistic orientation estimation with matrix Fisher#^mohlin2020probabilistic-010]] — The authors state that their convex loss with bounded gradient magnitudes results in stable training, unlike discontinuous rotation losses.
- [[Geist2024learning - Learning with 3D rotations, a hitchhiker's guide to SO(3)#^geist2024learning-006]] — Table 1 lists Euler angles, exponential coordinates, unit quaternions, and axis-angle as having a discontinuous map g from SO(3).
- [[Geist2024learning - Learning with 3D rotations, a hitchhiker's guide to SO(3)#^geist2024learning-016]] — The discontinuities imply points in feature space where the target function's Lipschitz constant blows up, which also blows up the loss gradient.
- [[Geist2024learning - Learning with 3D rotations, a hitchhiker's guide to SO(3)#^geist2024learning-049]] — The authors conclude that three- or four-parameter representations impede learning by inevitably introducing discontinuities when rotations are the model output.
- [[Geist2024learning - Learning with 3D rotations, a hitchhiker's guide to SO(3)#^geist2024learning-050]] — When rotations appear in the inputs of the regression task, the authors conclude that discontinuities do not hinder learning.
- [[Deng2020deep - Deep Bingham Networks Dealing with Uncertainty and#^deng2020deep-064]] — With the continuous 6D rotation representation, MBN averages 0.67 correct relocalization poses at 20°/0.3m, versus 0.35 for a plain MDN.
- [[Murphy2021implicit - Implicit-PDF Non-Parametric Representation of Probability#^murphy2021implicit-013]] — Rotations are input as 3 × 3 rotation matrices, which the authors found best to avoid discontinuities of other representations.
- [[Sundermeyer2021contact - Contact-GraspNet Efficient 6-DoF Grasp Generation in#^sundermeyer2021contact-018]] — The authors state that their rotation representation, in contrast to axis-angle representations, has neither ambiguities nor discontinuities.

## Relations


## Open questions

## History

- 2026-09-18 · Eki Gonzalez Flamarique · created: promoted at the bar from 6 sources · topic: Equivariant networks and rotation representations (drafter's packet `p3-equivariance-rotations`, confirmed at the gate)
