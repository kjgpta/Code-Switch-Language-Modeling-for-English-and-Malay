models:
	model.txt describes each model's training text
	lm_{a, b, c, d}.gz

normalized_data_for_lm:
	removed <malay> </malay> tags

ppls:
	perplexity results of LMs in models on val and test in normalized_data_for_lm

scripts:
	scripts to build LM and evaluate requires SRILM installation


RESULTS:
	lm_a: 143.2646 val, 144.1598 test