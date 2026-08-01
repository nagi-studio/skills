# Deep Report

Use Deep Report only when the user explicitly requests a complete one-shot deep analysis, review, or non-interactive report.

Read the full paper and relevant appendices. Inspect official code, project pages, benchmark definitions, cited work, and intellectual ancestry when they materially affect novelty, implementation, or evidence. Look beyond aggregate scores to cases, distributions, tails, anomalous results, and failure examples when available.

Construct predictions using only the problem, prior work, and proposed method before consulting reported outcomes. Label them `【合理推断】`; do not backfit them. Because the user explicitly selected a report, reveal the ledger and outcomes in the same response.

## Pass 1: Reconstruct the problem

- `研究问题`: target problem, value, and operational success.
- `之前怎么做，为什么不够`: strongest prior approaches and concrete failure modes.
- `作者可能的思考路径`: plausible path from pre-existing ideas and observations, without using the target contribution as a premise.

## Pass 2: Establish predictions

Record a small number of high-information expectations:

- strongest baseline and expected margin;
- component expected to carry the improvement;
- likely failure boundary;
- qualitative error predicted by the mechanism.

## Pass 3: Rebuild the mechanism

- `核心 intuition`
- `具体方法和一个真实例子`
- `数学推导和理论背景`

Derive important objectives, losses, constraints, or guarantees from basic definitions. Define symbols, check dimensions and boundary cases, and explain what each transformation buys.

## Pass 4: Perform an evidence autopsy

Use `问题 -> 实验设计 -> 结果 -> 是否支持 claim` for each central experiment. Compare outcomes with the prediction ledger. Inspect strongest baselines, uncertainty, negative results, qualitative outputs, failure cases, and appendix evidence. Separate established conclusions from underdetermined ones.

## Pass 5: Attempt falsification

- `最脆弱的假设`
- `如果我要反对它`
- matched-control experiments or stress tests that could erase the reported gain;
- tuning asymmetry, metric mismatch, data contamination, hidden compute differences, and overclaiming.

## Pass 6: Update beliefs and transfer

- `Belief update`: `阅读前我以为 -> 论文实际显示 -> 我的判断错在 -> 现在我相信 -> 仍未解决`
- `Takeaways`: durable mechanisms and research lessons.
- `一周最小复现实验`: feasible test of one central claim with minimal data, compute, and code.
- `Follow-up idea`: new problem, importance, method idea, and genuine difficulty.

Use the multimodal composition contract throughout. Do not convert this report into a visualization-only dashboard. Use prose for causal reasoning, formulas for precision, original figures for evidence, and focused UI for mechanisms that benefit from manipulation.
