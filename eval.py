#intended to run seperately but this is just the evaluation component
from rouge_score import rouge_scorer
reference = "Dyslexia is a reading disorder that affects comprehension and speed."
generated = "Dyslexia impacts how people read and understand written language."

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
scores = scorer.score(reference, generated)

for metric, score in scores.items():
    print(f"{metric}: Precision={score.precision:.3f}, Recall={score.recall:.3f}, F1={score.fmeasure:.3f}")