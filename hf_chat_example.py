import os
import json
import sys
from huggingface_hub import InferenceClient

# Use HF_TOKEN for the Python client (matches your snippet)
token = os.environ.get("HF_TOKEN")
if not token:
    print("Set HF_TOKEN in your environment, e.g. export HF_TOKEN=\"<your-token>\"", file=sys.stderr)
    raise SystemExit(1)

# If this model is hosted on the official Hugging Face Inference API, omit provider.
# If you must use a third-party provider (e.g. "hyperbolic"), set provider accordingly.
# client = InferenceClient(provider="hyperbolic", api_key=token)  # uncomment if needed
client = InferenceClient(api_key=token)

model_id = "deepseek-ai/DeepSeek-V3-0324"

try:
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ],
        # You can set other params (temperature, max_new_tokens) here if supported
        # params={"temperature": 0.2, "max_new_tokens": 128},
    )
except Exception as e:
    print("API call failed:", e, file=sys.stderr)
    raise

# Print raw response to inspect structure
print("RAW RESPONSE:")
try:
    print(json.dumps(completion, default=lambda o: getattr(o, "__dict__", str(o)), indent=2))
except Exception:
    print(repr(completion))

# Helper to extract text robustly from common response shapes
def extract_text(resp):
    # resp may be a mapping-like object or an SDK wrapper
    try:
        choices = resp.get("choices") if isinstance(resp, dict) else getattr(resp, "choices", None)
    except Exception:
        choices = None

    if not choices:
        # Try checking ‘data’ or just stringifying
        if isinstance(resp, dict) and "generated_text" in resp:
            return resp["generated_text"]
        return str(resp)

    first = choices[0]
    # message may be dict or attr
    msg = first.get("message") if isinstance(first, dict) else getattr(first, "message", None)
    if isinstance(msg, str):
        return msg

    # message content might be in different keys
    if isinstance(msg, dict):
        for k in ("content", "text", "value"):
            if k in msg:
                c = msg[k]
                if isinstance(c, str):
                    return c
                if isinstance(c, list):
                    # combine string blocks
                    return "".join([b.get("text") if isinstance(b, dict) and "text" in b else str(b) for b in c])
    # fallback to the first choice text fields
    for k in ("text", "message", "content"):
        if isinstance(first, dict) and k in first and isinstance(first[k], str):
            return first[k]
    # Last resort
    return json.dumps(first, default=str)

print("\nEXTRACTED TEXT:")
print(extract_text(completion))