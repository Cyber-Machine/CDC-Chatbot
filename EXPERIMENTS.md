# Experiments

In my experimentation, I tested various models including `llama-2-7b`, `Falcon-7b`, and `mistral-7b`. Among them, the mistral-7b-instruct model stood out for its output quality.

**Key Findings:**

`temperature`: I found that **higher temperatures (>0.7)** resulted in better output. This parameter influences creativity, with higher values leading to more diverse responses.

`top_p`: **Increasing top-p (>1.1)** yielded the best results for me. This parameter, known as nucleus sampling, affects the diversity of token selection during generation.

`max_tokens`: I adjusted the max_tokens parameter to avoid truncating output. A value of 650 worked well for me, balancing output length and quality.

## Future Directions

I suggest further exploration in prompt engineering, experimenting with other chat models, refining retrieval strategies, and improving output quality.
