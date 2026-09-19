---
aliases: []
type: "source"
title: "Merging Models with Fisher-Weighted Averaging"
citekey: "Matena2021merging"
doi: "10.48550/arXiv.2111.09832"
arxiv: "2111.09832"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2111.09832"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Michael Matena", "Colin Raffel"]
sha256: ["d9d5882c924963c46eb38805e7d39b198bc677d71f29f28f21246c35eed59735"]
pdf: "Content/Papers/Matena2021merging.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 69
---

📄 PDF: [[Matena2021merging.pdf]]

> [!abstract] One-sentence summary
> Frames parameter averaging as maximizing the joint likelihood of Gaussian approximate posteriors and introduces Fisher merging, a Fisher-weighted average that beats plain averaging for ensembling and robust fine-tuning and cheaply rivals gradient-based intermediate-task and domain-adaptive transfer.

## Abstract

Averaging the parameters of models that have the same architecture and initialization can provide a means of combining their respective capabilities. In this paper, we take the perspective that this "merging" operation can be seen as choosing parameters that approximately maximize the joint likelihood of the posteriors of the models' parameters. Computing a simple average of the models' parameters therefore corresponds to making an isotropic Gaussian approximation to their posteriors. We develop an alternative merging procedure based on the Laplace approximation where we approximate each model's posterior as a Gaussian distribution whose precision matrix corresponds to its Fisher information. We first show that our "Fisher merging" technique provides a performance boost in settings where simple parameter averaging is currently used -- specifically, robust fine-tuning and model ensembling. Then, we compare merging to standard gradient-based transfer learning and demonstrate that merging enables a fundamentally different method for transferring capabilities across models. Specifically, we show that Fisher merging is competitive with gradient-based transfer learning approaches (while being significantly cheaper) in intermediate-task training and domain-adaptive pre-training. We also show that our merging procedure makes it possible to combine models in previously unexplored ways. We release our code to facilitate future research into methods for merging models. (arXiv)

## 🧠 Key ideas (atomic)

- The authors frame model merging as choosing parameters that approximately maximize the joint likelihood of the models' parameter posteriors. (Matena & Raffel, 2021) `ev:asserted` p. 2 ^matena2021merging-001
- Approximating each posterior as an isotropic Gaussian centred on the model's parameters makes the likelihood maximizer equal to the simple parameter average. (Matena & Raffel, 2021) `ev:computed` p. 3 ^matena2021merging-002
- Fisher merging uses the diagonal of each model's Fisher information as the precision matrix of a Gaussian approximate posterior. (Matena & Raffel, 2021) `ev:reported` p. 3 ^matena2021merging-003
- Fisher merging sets each merged parameter to a weighted average of the models' values, weighted by each parameter's Fisher information. (Matena & Raffel, 2021) `ev:computed` p. 4 ^matena2021merging-004
- The authors add a scalar weight λi per model, nonnegative and summing to one, as hyperparameters setting each model's relative importance. (Matena & Raffel, 2021) `ev:reported` p. 3 ^matena2021merging-005
- The Laplace approximation gives a Gaussian posterior whose precision is the Fisher information matrix at trained parameters assumed to be a local posterior maximum. (Matena & Raffel, 2021) `ev:cited` p. 4 ^matena2021merging-006
- The Fisher information matrix coincides with the Hessian at modes of the distribution, which explains its use in the Laplace approximation. (Matena & Raffel, 2021) `ev:cited` p. 4 ^matena2021merging-007
- Because the full Fisher matrix takes O(|θ|2) memory, the authors follow common practice and use only its diagonal. (Matena & Raffel, 2021) `ev:reported` p. 4 ^matena2021merging-008
- The diagonal Fisher is estimated by averaging squared log-likelihood gradients over N examples drawn from the dataset used to train the model. (Matena & Raffel, 2021) `ev:reported` p. 4 ^matena2021merging-009
- Computing the diagonal Fisher has roughly the same computational cost as training on N examples, since it needs N gradients. (Matena & Raffel, 2021) `ev:asserted` p. 4 ^matena2021merging-010
- The authors note that Fisher merging might be less performant for models whose parameters are far apart in parameter space. (Matena & Raffel, 2021) `ev:asserted` p. 4 ^matena2021merging-011
- The authors therefore limit their focus to models that were trained from the same initialization, as the Fisher is a local property. (Matena & Raffel, 2021) `ev:reported` p. 4 ^matena2021merging-012
- When the Fisher is close to zero for a parameter across all models, the merged value defaults to that parameter in a privileged target model. (Matena & Raffel, 2021) `ev:reported` p. 4 ^matena2021merging-013
- The authors report that the choice of default value for these near zero Fisher parameters had little impact on performance. (Matena & Raffel, 2021) `ev:measured` p. 4 ^matena2021merging-014
- Parameters absent from some models, such as task specific classification heads, are kept unchanged rather than passed through the merging procedure. (Matena & Raffel, 2021) `ev:reported` p. 5 ^matena2021merging-015
- The authors acknowledge that keeping the task specific heads unchanged may lead to a distribution shift in the classification head inputs. (Matena & Raffel, 2021) `ev:asserted` p. 5 ^matena2021merging-016
- For ensembling, the authors merge five fine-tuned BERT-Base checkpoints per dataset from the Hugging Face hub on RTE, MRPC and SST-2. (Matena & Raffel, 2021) `ev:reported` p. 5 ^matena2021merging-017
- Each ensemble member receives an equal merging weight λi = 1/5, since no member was expected to deserve a larger weight. (Matena & Raffel, 2021) `ev:reported` p. 5 ^matena2021merging-018
- On validation sets, Fisher merging significantly outperforms isotropic merging for ensembling on RTE, MRPC and SST-2 in all cases. (Matena & Raffel, 2021) `ev:measured` p. 5 ^matena2021merging-019
- Fisher merged ensembles attain performance comparable to prediction ensembling, which averages the output probabilities of all five models. (Matena & Raffel, 2021) `ev:measured` p. 5 ^matena2021merging-020
- Inference after merging is M times cheaper than prediction ensembling, suggesting merging can provide a cheaper alternative to standard ensembling. (Matena & Raffel, 2021) `ev:asserted` p. 5 ^matena2021merging-021
- Wortsman et al. found that fine-tuning a pre-trained vision model tends to decrease accuracy on the original pre-training task. (Matena & Raffel, 2021) `ev:cited` p. 5 ^matena2021merging-022
- For robust fine-tuning, the authors use the WiSE-FT codebase and setup exactly, simply replacing isotropic merging with Fisher merging. (Matena & Raffel, 2021) `ev:reported` p. 6 ^matena2021merging-023
- WiSE-FT is applied to the ImageNet pre-trained ViT-B/16 model with five out-of-domain datasets, including ImageNet-A, ImageNet-R and ObjectNet. (Matena & Raffel, 2021) `ev:reported` p. 6 ^matena2021merging-024
- The pre-trained model's weight λ1 is varied from 0 to 1 in 0.1 increments, with the fine-tuned weight correspondingly decreasing. (Matena & Raffel, 2021) `ev:reported` p. 6 ^matena2021merging-025
- Fisher merging produces a significantly better trade-off between IID ImageNet accuracy and average OOD accuracy than isotropic merging does. (Matena & Raffel, 2021) `ev:measured` p. 6 ^matena2021merging-026
- At the λ1 producing the best average OOD accuracy, Fisher merging yields about 1% higher IID accuracy than isotropic merging. (Matena & Raffel, 2021) `ev:measured` p. 6 ^matena2021merging-027
- The authors state that, to their knowledge, no prior work has considered parameter averaging as a way of performing intermediate-task transfer learning. (Matena & Raffel, 2021) `ev:asserted` p. 6 ^matena2021merging-028
- Intermediate-task experiments are limited to the BERT and RoBERTa language models, since such training has mainly been considered in NLP. (Matena & Raffel, 2021) `ev:reported` p. 6 ^matena2021merging-029
- The authors mostly explored merging pairs of models to enable comparison with past work, leaving merges of more models for future work. (Matena & Raffel, 2021) `ev:reported` p. 6 ^matena2021merging-030
- STS-B is turned into a classification task by partitioning its continuous label into 25 buckets, to simplify computing the Fisher. (Matena & Raffel, 2021) `ev:reported` p. 7 ^matena2021merging-031
- Each GLUE checkpoint's diagonal Fisher is computed using up to 4096 examples from the corresponding training set. (Matena & Raffel, 2021) `ev:reported` p. 7 ^matena2021merging-032
- Merging weights λi are chosen by a grid search with 50 points, scored on the first 2048 validation examples. (Matena & Raffel, 2021) `ev:reported` p. 7 ^matena2021merging-033
- Congruent with past work, intermediate-task training gave the most notable performance boost when RTE was the target among GLUE dataset pairs. (Matena & Raffel, 2021) `ev:measured` p. 7 ^matena2021merging-034
- With BERT-base and RTE as target, gradient-based intermediate-task training hurts accuracy for some of the GLUE donor datasets. (Matena & Raffel, 2021) `ev:measured` p. 7 ^matena2021merging-035
- With BERT-base and RTE as target, merging with a GLUE donor model always helps compared with no intermediate-task training. (Matena & Raffel, 2021) `ev:measured` p. 7 ^matena2021merging-036
- Fisher merging gets comparable or better RTE accuracy than isotropic merging, with the largest gap observed when MNLI is the intermediate task. (Matena & Raffel, 2021) `ev:measured` p. 7 ^matena2021merging-037
- Merging performs worse than standard gradient-based intermediate-task training when MNLI is the donor task for RTE with BERT-base. (Matena & Raffel, 2021) `ev:measured` p. 7 ^matena2021merging-038
- Fisher merging a BERT-base model fine-tuned on MNLI then RTE with GLUE donors boosts accuracy over gradient-based intermediate-task training for all tasks. (Matena & Raffel, 2021) `ev:measured` p. 7 ^matena2021merging-039
- A boost is still conferred when merging with an MNLI-trained donor, which the authors suggest shows merging is a complementary transfer path. (Matena & Raffel, 2021) `ev:measured` p. 7 ^matena2021merging-040
- For RoBERTa-large, the donors were the original RoBERTa-large checkpoint fine-tuned on MRPC, RTE, STS-B and SST-2, not on MNLI. (Matena & Raffel, 2021) `ev:reported` p. 8 ^matena2021merging-041
- Merging provides a boost in RTE performance even for the more performant RoBERTa-large model fine-tuned from an MNLI intermediate checkpoint. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-042
- The largest RoBERTa-large boost, 2.2 points, came from Fisher merging with another RTE checkpoint, which resembles using merging for ensembling. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-043
- Adding another intermediate task in sequential gradient-based training significantly harmed RTE performance compared with intermediate-task training on MNLI alone. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-044
- The authors hypothesize this harm relates to catastrophic forgetting, where MNLI capabilities are forgotten while training on the next intermediate task. (Matena & Raffel, 2021) `ev:asserted` p. 8 ^matena2021merging-045
- Fine-tuning BERT-base on RTE for 10 epochs would require about 5.5e14 FLOPs, estimated with the heuristics of Kaplan et al. (Matena & Raffel, 2021) `ev:computed` p. 8 ^matena2021merging-046
- Computing the merged checkpoint, evaluating it and estimating the Fisher require about 4.0e8, 2.0e12 and 9.1e13 FLOPs respectively. (Matena & Raffel, 2021) `ev:computed` p. 8 ^matena2021merging-047
- By this FLOP estimate, Fisher merging has a roughly 6× lower total cost than fine-tuning BERT-base on RTE. (Matena & Raffel, 2021) `ev:computed` p. 8 ^matena2021merging-048
- By the same FLOP estimate, isotropic merging has a 275× lower total cost than fine-tuning BERT-base on RTE. (Matena & Raffel, 2021) `ev:computed` p. 8 ^matena2021merging-049
- The Fisher matrix only needs to be computed once and can be reused for later merges, amortizing the most expensive step. (Matena & Raffel, 2021) `ev:asserted` p. 8 ^matena2021merging-050
- Using the full training set to estimate the Fisher gave 73.4% RTE accuracy for Fisher merging BERT-base with an MNLI donor. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-051
- Using only 256 examples to estimate the Fisher gave 72.7% accuracy, a mild degradation that still outperformed the isotropic merging baseline. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-052
- In the Fisher sample size study, isotropic merging averaged 72.2 RTE accuracy, while the original RTE checkpoints averaged 63.7. (Matena & Raffel, 2021) `ev:measured` p. 16 ^matena2021merging-053
- Domain adaptation experiments use RoBERTa-base with CHEMPROT for the biomedical domain, plus ACL-ARC and SCIERC for computer science. (Matena & Raffel, 2021) `ev:reported` p. 8 ^matena2021merging-054
- These domains were chosen because their classification tasks saw the largest gains from domain-adaptive pre-training in Gururangan et al. (Matena & Raffel, 2021) `ev:cited` p. 8 ^matena2021merging-055
- Domain-adaptive pre-training ran on RoBERTa-base for 32,768 steps with batch size 32, using Adam at learning rate 1e-5. (Matena & Raffel, 2021) `ev:reported` p. 14 ^matena2021merging-056
- The domain-adaptive pre-training data were the BIOMED and CS splits of the public S2ORC dataset, unlike the internal version Gururangan et al. used. (Matena & Raffel, 2021) `ev:reported` p. 14 ^matena2021merging-057
- The Fisher for the DAPT checkpoints was computed on 131,072 examples, using one sample from the logits per example. (Matena & Raffel, 2021) `ev:reported` p. 15 ^matena2021merging-058
- DAPT merging coefficients were chosen by a grid search of 75 values, using F1 on the first 2048 test examples. (Matena & Raffel, 2021) `ev:reported` p. 15 ^matena2021merging-059
- Among the three domain adaptation tasks, merging provided its largest boost on the ACL-ARC citation intent task. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-060
- On ACL-ARC, merging with the DAPT checkpoint outperformed traditional fine-tuning that started from the DAPT checkpoint. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-061
- The authors observed only a minor improvement from merging on CHEMPROT and SCIERC in the domain adaptation experiments. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-062
- Their gains from gradient-based domain-adaptive fine-tuning were smaller than Gururangan et al. reported, likely because of public data and fewer steps. (Matena & Raffel, 2021) `ev:measured` p. 8 ^matena2021merging-063
- [[Elastic weight consolidation]] also uses the Laplace approximation to the posterior, creating a regularizer to prevent catastrophic forgetting in continual learning. (Matena & Raffel, 2021) `ev:cited` p. 8 ^matena2021merging-064
- The authors argue that [[Elastic weight consolidation|EWC]] keeps a model from losing acquired knowledge, whereas merging directly adds new knowledge to a model. (Matena & Raffel, 2021) `ev:asserted` p. 9 ^matena2021merging-065
- The authors argue methods that directly combine parameters have the potential to be more powerful than distillation or output ensembling. (Matena & Raffel, 2021) `ev:asserted` p. 9 ^matena2021merging-066
- The authors note their merging procedure has an efficient closed-form solution, whereas distillation requires iterative gradient descent-based training. (Matena & Raffel, 2021) `ev:asserted` p. 9 ^matena2021merging-067
- The authors believe they are the first to demonstrate cross-task transfer from checkpoint averaging and explore it for transfer learning. (Matena & Raffel, 2021) `ev:asserted` p. 9 ^matena2021merging-068
- The authors conclude Fisher merging attains comparable and sometimes better performance than traditional gradient-based transfer learning at significantly lower costs. (Matena & Raffel, 2021) `ev:asserted` p. 9 ^matena2021merging-069

## 🎯 Contributions

## 📖 Glossary

- **Model merging** — Averaging parameters of models sharing an architecture and initialization into one model.
- **Isotropic merging** — Plain parameter averaging, equivalent to isotropic Gaussian posterior approximations.
- **Fisher merging** — Parameter average weighted per parameter by each model's diagonal Fisher information.
- **Laplace approximation** — Gaussian posterior from a second-order Taylor expansion of log density at a mode.
- **Fisher information matrix** — Expected outer product of log-likelihood gradients; coincides with the Hessian at modes.
- **WiSE-FT** — Robust fine-tuning that averages pre-trained and fine-tuned weights.
- **Intermediate-task training** — Fine-tuning on a donor task before training on the target task.
- **DAPT** — Domain-adaptive pre-training: continued pre-training on unlabeled domain-specific data.
- **Donor model** — Model whose capabilities are merged into a recipient model.

## ❓ Open questions

- Do better Fisher approximations (Kronecker-factored, full-block) improve merging over the diagonal?
- How well does Fisher merging scale to more than two models in transfer settings?
- How does Fisher merging behave for models that do not share an initialization?
- Can the merging coefficients λi be set without a grid search on held-out data?
- Does the unmerged-head distribution shift hurt on tasks beyond those tested?
- Can federated learning ideas (e.g. matched averaging) improve model merging?

## 📝 Notes on reading

- Version read is arXiv v2 (26 Aug 2022, marked Preprint, under review); the metadata year is 2021 (v1).
- Figures 2 to 7 are plots only; exact per-bar/per-point values are not in the text and were not claimed.
- Tables 1 and A1–A4: the extraction fused means with their standard-deviation subscripts (e.g. 82.70.3 for 82.7 ± 0.3), so per-cell values were not claimed.
- Table 1 appears to show isotropic merging (81.7) above Fisher merging (81.3) on SciERC, and above fine-tuning; the text speaks only of a minor improvement.
- Text on p. 8 says the full training set gave the best Fisher estimate (73.4%), but Table A4 shows 73.5 for 32768 MNLI / 2490 RTE examples; also Table A1 reports 73.2 for MNLI→RTE Fisher merging.
- 'Significantly' outperforms (ensembling, WiSE-FT) is stated without a reported statistical test.
- DAPT merging coefficients were selected on the first 2048 test examples (Appendix D), not validation examples.
- Low-resource GLUE fine-tuning runs with poor performance were discarded (Appendix C).

## Suggested new concepts

- Fisher merging — a named weight-merging method central to later model-merging work.
- Model merging — the general practice of combining trained models by parameter averaging, with several applications here.
- Laplace approximation — the posterior approximation that justifies Fisher weighting.
- Intermediate-task transfer learning — the transfer setting merging is compared against.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H4.** Fusiona modelos o adaptadores de tarea con una media ponderada por la Fisher, útil para combinar LoRA por subtarea del laboratorio.
