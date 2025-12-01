1) Executive Summary

Problem

Companies and researchers often need a local, self-contained large language model that can be deployed without API keys or cloud dependencies to protect sensitive data and avoid external service costs. In our earlier case study, deploying a model on a virtual machine and wiring it to an Azure-hosted Flask service created an unnecessarily complicated setup for beginners. Furthermore, Many LLM demos rely on multiple moving parts, Flask backends, separate model servers like vLLM or Ollama, and sometimes databases, which increases operational complexity and raises the barrier to entry for students and new practitioners.

Solution

This project packages a complete Qwen2.5-1.5B-Instruct chat system into one Docker container. A minimal Flask server serves as the backend, exposing a /api/chat endpoint and /api/health, and a clean HTML frontend provides a professional interface. The Qwen model is loaded directly in the Docker container using HuggingFace Transformers, which run entirely on CPU. This case study produces a reproducible, self-contained LLM microservice that can run locally or on an Azure VM with a single command.

2) System Overview

Course Concepts This Case Study Directly Uses:
    1. Docker
    2. Local LLM Serving
    3. Flask API
    4. Azure Website Deployment

Architecture Diagram: 

Data/Models/Services: 

3) How to Run (Local)


4) Design Decisions
Why this concept:
I wanted a system that demonstrates local-first LLM inference, a single-container microservice, reproducibility across personal laptop and Azure VMs. Therefore, embedding the model directly into the Flask container is simpler than running an external model server such as vLLM or Ollama.

Alternatives Considered
Alternative
Why Not Used
vLLM server
Requires >16GB RAM even for small models; slower startup; unnecessary complexity.
Ollama
Does not support Qwen2.5 yet; not part of course tools.
Multi-container (Flask + Model server)
Higher complexity, more networking, not needed for a single model demo.


Tradeoffs
Performance: CPU inference is slow but predictable and low-cost.

Cost: Runs on the free tier Azure VM (Standard B1s/B2s).

Complexity: One container = fewer moving parts.

Maintainability: Model updates require rebuilding the image.

Security & Privacy
No API keys required.

No data stored on disk.

Only /api/chat is exposed.

Flask input sanitized (simple JSON only).

Limitations
Qwen2.5-1.5B is still large → slow inference on CPU.

Container size ~3GB due to model.

Azure deployment requires 5-10 min cold boot time for loading.

6. What’s Next
Planned improvements:
Image understanding using more advance models such as Qwen2.5-VL-7b

Chat history persistence (MongoDB or SQLite)

Model selection dropdown (Qwen, TinyLlama, Phi-3, etc.)
