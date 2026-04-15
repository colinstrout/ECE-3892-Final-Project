# ECE-3892-Reproducible-AI-Extended

Github Repository for Docker Container as an extension of ECE 3892 Project 3 for the final project of the course

## Outline

Case study comparing both F32 and INT8 on PC and Raspberry PI Zero 2W.

- Compare Accuracy/Response quality
- Latency (ms)
- Model Size (MB)
- CPU Utilization

## Setup Instructions

Please follow the [Detailed Step-by-Step Directions](container-instructions.md) to configure your environment.

## Results

**Comparison of T5-Small Performance: Desktop (AMD64) vs. Edge (ARM64)**

- This extension study evaluates the trade-offs between full-precision ($F32$) and quantized ($INT8$) models across two distinct hardware architectures.
- As mentioned above, this study utilizes the t5-small model by Google for this analysis, as this model was used in the assignment that inspired this study.
- The notebook used to export the models in ONNX format can be seen [here](./benchmarking/onnx_format_generation.ipynb)

---

## 🏗️ Hardware Specifications

| Feature         | Desktop PC (AMD64)                | Raspberry Pi Zero 2W (ARM64) |
| :-------------- | :-------------------------------- | :--------------------------- |
| **Processor**   | AMD Ryzen 9 (8 Cores, 16 threads) | Broadcom BCM2710A1 (4-Core)  |
| **RAM**         | 16GB DDR4                         | 512MB LPDDR2                 |
| **Environment** | Windows/WSL2 Docker               | Raspberry Pi OS (Docker)     |

---

## 📦 Model Size & Quantization Efficiency

The transition from $F32$ to $INT8$ quantization resulted in a significant reduction in disk and memory footprint. This was the primary driver for successful deployment on the Pi Zero 2W's $512MB$ RAM limit.

| Model Component       | F32 Size (MB)   | INT8 Size (MB)  | Compression Ratio |
| :-------------------- | :-------------- | :-------------- | :---------------- |
| **Encoder**           | $134.86 MB$     | $33.89 MB$      | $3.98 \times$     |
| **Decoder**           | $221.72 MB$     | $55.78 MB$      | $3.97 \times$     |
| **Decoder (w/ Past)** | $209.70 MB$     | $52.75 MB$      | $3.98 \times$     |
| **Total Archive**     | **$566.28 MB$** | **$142.42 MB$** | **$3.98 \times$** |

### Engineering Impact

1. **Memory Mapping:** The $F32$ model requires over $566MB$ just for the weights, which exceeds the Pi's physical RAM before the OS or Docker even load.
2. **Quantization Benefit:** By reducing the weights to $INT8$, the entire model fits into $~142MB$ of memory. This leaves enough "headroom" in the $512MB$ RAM for the Python runtime and OS overhead, significantly reducing the system's reliance on slow SD-card swap space.

---

## 📈 Comparative Analysis

| Architecture | Precision | Avg Latency | Peak CPU % | Semantic Preservation | Status          |
| :----------- | :-------- | :---------- | :--------- | :-------------------- | :-------------- |
| **AMD64**    | **F32**   | $1.81s$     | $1565\%$   | $1.000$ (Reference)   | ✅ Success      |
| **AMD64**    | **INT8**  | $1.54s$     | $1576\%$   | $0.9175$              | ✅ Success      |
| **ARM64**    | **INT8**  | $33.52s$    | $163.3\%$  | $0.9666$              | ✅ Success      |
| **ARM64**    | **F32**   | $N/A$       | $N/A$      | $N/A$                 | ❌ **OOM Kill** |

---

## 🔍 Technical Observations

### 1. The "OOM Kill" Threshold

The Raspberry Pi Zero 2W failed to run the $F32$ full-precision model. Kernel logs confirmed a **SIGKILL** by the Linux Out-of-Memory (OOM) Killer:

> `[ 232.231030] Out of memory: Killed process 1219 (python) total-vm:2630348kB`
> The $2.6GB$ virtual memory footprint overwhelmed the $512MB$ physical RAM. To achieve successful execution of the **INT8** model, a $2GB$ swapfile was required to handle the memory mapping overhead.

### 2. Quantization Trade-offs (INT8)

- **Latency Speedup:** On AMD64, quantization resulted in a $15\%$ reduction in inference time. On ARM64, quantization was the mechanical necessity that allowed the model to run at all.
- **Accuracy (Cosine Similarity):**
  - **RAVEN Summary:** Maintained a high similarity of **$0.9975$**, indicating nearly zero semantic loss.
  - **ZEUS-X1 Summary:** Dropped to **$0.8375$** during $F32 \rightarrow INT8$ transition. This illustrates that technical nuances (like specific voltage/thermal delta triggers) are more susceptible to quantization "noise" than general descriptive text.

### 3. CPU Core Utilization

- **AMD64:** Distributed the workload across all 16 cores ($>1500\%$), showing the T5 ONNX runtime is highly optimized for multi-threaded desktop environments.
- **ARM64:** Capped at $~163\%$ (utilizing roughly 1.6 cores of the 4 available). This suggests the bottleneck shifted from raw computation to **Memory I/O** and **SD-Card Swap Bandwidth**.
