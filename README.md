# I. Executive Summary

## Problem

Companies and researchers often need a local, self-contained large language model that can be deployed without API keys or cloud dependencies to protect sensitive data and avoid external service costs. In our earlier case study, deploying a model on a virtual machine and wiring it to an Azure-hosted Flask service created an unnecessarily complicated setup for beginners. Furthermore, Many LLM demos rely on multiple moving parts, Flask backends, separate model servers like vLLM or Ollama, and sometimes databases, which increases operational complexity and raises the barrier to entry for students and new practitioners.

## Solution

This project packages a complete Qwen2.5-1.5B-Instruct chat system into one Docker container. A minimal Flask server serves as the backend, exposing a /api/chat endpoint and /api/health, and a clean HTML frontend provides a professional interface. The Qwen model is loaded directly in the Docker container using HuggingFace Transformers, which run entirely on CPU. This case study produces a reproducible, self-contained LLM microservice that can run locally or on an Azure VM with a single command.

---

# II. System Overview

## Course Concepts Used

1. **Docker** – the entire app (frontend, backend, and model) is containerized.
2. **Local LLM Serving** – Qwen2.5-0.5B-Instruct runs fully locally on CPU.
3. **Flask API** – provides /api/chat endpoint for model inference.
4. **Render Cloud Deployment** – final container deployed using Render Web Services.

## Architecture Diagram
![Untitled presentation](https://github.com/user-attachments/assets/7c513a74-dba5-4c17-8c14-a6209ff90991)

```    
+--------------------------------------------------------------+
|                          Browser UI                          |
|            (HTML / CSS / JavaScript Chat Interface)          |
+--------------------------------------------------------------+
                              |
                              |  POST /api/chat
                              v
+--------------------------------------------------------------+
|                         Flask Backend                        |
|                     (Python 3.11 / Flask 3)                  |
+--------------------------------------------------------------+
                              |
                              |  Uses Transformers API
                              v
+--------------------------------------------------------------+
|           Qwen2.5-0.5B-Instruct Model (FP16, CPU)            |
|   HuggingFace Transformers • Local Model • No External API   |
+--------------------------------------------------------------+
                              |
                              |  Generated JSON
                              v
+--------------------------------------------------------------+
|                       JSON Chat Response                     |
|             (Returned to Browser → Rendered as bubbles)      |
+--------------------------------------------------------------+
```

## **Data / Models / Services**

| Component    | Description    |
|---|---|
| **Model**    | Qwen/Qwen2.5-0.5B-Instruct    |
| **Source**    | https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct    |
| **Size**    | ~3 GB FP32    |
| **Format**    | HuggingFace Transformers (PyTorch)    |
| **License**    | Qwen License 2.0    |

License URL https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/main/LICENSE

Frontend:
– Pure HTML/CSS/JS
– Optional dark/light mode toggle

Backend:
– Python 3.11
– Flask 3.0
– Transformers 4.47
– Torch (CPU-only FP16)

Containerization:
– Base image: python:3.11-slim
– Minimum recommended: 1 CPU / 8–16GB RAM

---

# III. How to Run (Local)

## Docker

### 1. Build the image
```{ssh}
 docker build -t qwen-chat .
```
 
### 2. Run the container
```{ssh}
 docker run --rm -p 8080:8080 qwen-chat
```

### 3. Open in browser

```{ssh}
 "http://localhost:8080"
```

### 4. Optional health check
```{ssh}
 curl http://localhost:8080/health
```


---

# IV. Design Decisions

## Why This Concept?

1. **Security & Independence**  
   Many organizations cannot send sensitive data to API-based LLMs. Running Qwen2.5 locally inside a Docker container eliminates external dependencies and allows full data control.

2. **Beginner-Friendly Deployment**  
   The previous case study required an Azure VM, SSH setup, and multiple running services. This version reduces everything to one container, one Flask API, and one front-end file.

3. **Reproducibility**  
   A Docker image ensures anyone can run the system with a single command, without worrying about Python environments, CUDA conflicts, or dependency drift.

## Tradeoffs

- **Performance:**  
  CPU inference is slow relative to GPU.

- **Cost:**  
  Hosting on cloud providers requires higher RAM; CPU hosting reduces expenses.

- **Complexity:**  
  One container means fewer moving parts.

- **Maintainability:**  
  Model upgrades require rebuilding the container.

## Security & Privacy

- No API keys or secrets required.

- No user data written to disk.

- Only /api/chat exposed.

- Flask input sanitized (simple JSON only).

## Limitations

- Response latency is noticeable on CPU.

- Container size is large (~2–3 GB).

- Cold boot times can be slow on cloud (model load = 20–50 seconds).

- Qwen2.5-1.5B has limited reasoning quality vs larger models.

- No conversation memory unless implemented manually.

---

# V. Results & Evaluation

## The Qwen Chat interface

<img width="1280" height="720" alt="Screenshot 2025-12-01 at 10 03 57 PM" src="https://github.com/user-attachments/assets/9beba4d7-650a-4792-9d6f-38d58180e384" />
<img width="1280" height="720" alt="Screenshot 2025-12-01 at 10 35 39 PM" src="https://github.com/user-attachments/assets/f51dd927-51b1-4b08-983d-ab113b5b0fb3" />

In the UI, user can talk to the Qwen chat bot (dark mode avaliable as well)


Suggested content:

- Screenshot of frontend UI (light + dark mode)

- Model loading time is 5~10 min (deploying locally)

- Average inference latency is 10~20 seconds 

- RAM usage is averagely >= 12GB when running in Docker (locally)

---

# VI. What’s Next

Planned improvements:

- **Multimodal support** (Qwen2.5-VL for image analysis)

- **Chat history persistence** (MongoDB, SQLite, or Redis)

- **System prompt selector** (Tutor / Creative / Coding modes)

- **Streaming tokens** for smoother UI

- **Model dropdown** (Phi-3, TinyLlama, Mistral, etc.)

- **Azure Blob–based memory** for long-term conversation state

# VII. Links 
GitHub Repo: https://github.com/Vienlendank/final-case-study
Public Cloud App (Render): https://qwen25-chat-latest.onrender.com
