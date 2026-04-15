import os
import sys
import logging
import time
import psutil

# 1. Silence Hugging Face and OpenMP warnings
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["KMP_WARNINGS"] = "0"
# This hides the 'some weights were not used' or 'naming' logs
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("optimum").setLevel(logging.ERROR)


from transformers import T5Tokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util

embedder_path = "./models/embedding_model"
embedder = SentenceTransformer(embedder_path)

arch = os.getenv("ARCH", "amd64").lower()

if arch == "amd64":
    MODEL_DIRS = ["./models/t5-small-onnx", "./models/t5-small-onnx-quantized-amd64"]
else:
    MODEL_DIRS = ["./models/t5-small-onnx", "./models./t5-smalll-onnx-quantized-arm64"]

print(f"🚀 Performing Benchmark comparison for {arch.upper()} models in F32 and then INT8")

if len(sys.argv) < 2:
    print("Usage: python app.py \"<text to summarize>\"")
    sys.exit(1)

text = " ".join(sys.argv[1:])

input_text = "summarize: " + text
summaries = []
embeddings = []
process = psutil.Process(os.getpid())
process.cpu_percent(interval=None)


for MODEL_DIR in MODEL_DIRS:
    if MODEL_DIR.endswith("quantized-amd64") or MODEL_DIR.endswith("quantized-arm64"):
        print(f"\n📊 Benchmarking quantized model (INT8)")
    else:
        print(f"\n📊 Benchmarking full precision model (F32)")

    tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR, legacy=False)
    model = ORTModelForSeq2SeqLM.from_pretrained(MODEL_DIR, provider="CPUExecutionProvider")
    inputs = tokenizer(input_text, return_tensors="pt")

    process.cpu_percent(interval=None)

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
    usage = process.cpu_percent(interval=None)
    per_core = psutil.cpu_percent(interval=None, percpu=True)
    
    print(f"CPU Usage: {usage}%")
    print(f"Per-core CPU Usage: {per_core}")
    print(f"Latency: {end - start:.2f}s")
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Summary: ", summary)
    summaries.append(summary)

for summary in summaries:
    embeddings.append(embedder.encode(summary, convert_to_tensor=True))

cos_sim = util.cos_sim(embeddings[0], embeddings[1])

print(f"\n🔍 Cosine Similarity between summaries: {cos_sim.item():.4f}")
