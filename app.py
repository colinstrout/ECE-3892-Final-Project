import sys
from transformers import T5Tokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM

MODEL_DIR = "t5-small-onnx"
tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
model = ORTModelForSeq2SeqLM.from_pretrained(MODEL_DIR)

if len(sys.argv) < 2:
    print("Usage: python app.py \"<text to summarize>\"")
    sys.exit(1)

text = sys.argv[1]

input_text = "summarize: " + text

inputs = tokenizer(input_text, return_tensors="pt")

summary_ids = model.generate(
    inputs["input_ids"],
    max_length=60,
    min_length=30,
    num_beams=4,
    length_penalty=2.0,
    early_stopping=True,
    use_cache=False
)

summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("Summary: ", summary)
