import os
import sys
import logging
import time

# 1. Silence Hugging Face and OpenMP warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["KMP_WARNINGS"] = "0"
# This hides the 'some weights were not used' or 'naming' logs
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("optimum").setLevel(logging.ERROR)

from transformers import T5Tokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM


precision = os.getenv("PRECISION", "f32").lower()
arch = os.getenv("ARCH", "amd64").lower()

if precision == "f32":
    MODEL_DIR = "./models/t5-small-onnx"
else:
    MODEL_DIR = f"./models/t5-small-onnx-quantized-{arch}"

print(f"🚀 Loading {precision.upper()} model optimized for {arch.upper()} from: {MODEL_DIR}")

tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR, legacy=False)
model = ORTModelForSeq2SeqLM.from_pretrained(MODEL_DIR, provider="CPUExecutionProvider")

if len(sys.argv) < 2:
    print("Usage: python app.py \"<text to summarize>\"")
    sys.exit(1)

text = " ".join(sys.argv[1:])

input_text = "summarize: " + text

inputs = tokenizer(input_text, return_tensors="pt")

start = time.time()
summary_ids = model.generate(
    inputs["input_ids"],
    max_length=60,
    min_length=30,
    num_beams=4,
    length_penalty=2.0,
    early_stopping=True,
    use_cache=True
)
end = time.time()

summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("Summary: ", summary)

print(f"Latency: {end - start:.2f}s")
