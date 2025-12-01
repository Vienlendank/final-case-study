import os
from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


#load Qwen2.5-1.5B-Instruct 
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")
DEVICE = "cpu"   

#enhance to model speed
os.environ["TOKENIZERS_PARALLELISM"] = "false"
torch.set_grad_enabled(False)

print(f"[info] Loading model: {MODEL_NAME} on CPU (FP32)...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32, 
    trust_remote_code=True
)

model.to(DEVICE)
model.eval()

print("[info] Model loaded successfully.")


#flask app
app = Flask(__name__, template_folder="templates")

#home
@app.get("/")
def home():
    return render_template("index.html")

#health check
@app.get("/health")
def health():
    return jsonify({"status": "ok", "model": MODEL_NAME}), 200


#this function generate  chat reply using Qwen2.5 chat template.
def generate_reply(user_text: str, max_new_tokens=128):
    messages = [
        {"role": "system", "content": "You are a concise helpful assistant."},
        {"role": "user", "content": user_text},
    ]

    #Qwen2.5 chat template
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9
        )

    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    text = tokenizer.decode(generated_ids, skip_special_tokens=True)
    return text.strip()

#Qwen chat
@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_text = (data.get("text") or "").strip()

    if not user_text:
        return jsonify({"reply": "(empty prompt)"}), 200

    try:
        reply = generate_reply(user_text)
        return jsonify({"reply": reply}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
