# mzanzi-ai

This repository contains the Mzanzi AI chatbot integration and a minimal backend that proxies requests to Hugging Face models.

Quickstart (development)
1. Copy `.env.example` to `.env` and set values (HUGGINGFACE_API_TOKEN, HF_MODEL_ID).
2. Install dependencies:
   - `npm install`
3. Start backend:
   - `npm run dev` (requires nodemon) or `npm start`

API
- POST /api/chat
  - Body: For chat-capable HF models:
    ```json
    {
      "inputs": {
        "messages": [
          {"role":"user","content":"Hello!"}
        ],
        "max_new_tokens": 256
      }
    }
    ```
  - Body: For text-gen HF models:
    ```json
    {
      "inputs": "Write a friendly greeting in Xhosa."
    }
    ```
  - Response:
    ```json
    {
      "result": <Hugging Face inference response>
    }
    ```

Local testing examples
- Chat-style request (example):
  ```bash
  curl -X POST http://localhost:3000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"inputs": {"messages":[{"role":"user","content":"Hello"}]}}'
  ```
- Plain-text request example:
  ```bash
  curl -X POST http://localhost:3000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"inputs":"Write a short poem in isiZulu."}'
  ```

Deployment
- A Dockerfile is included to build a container.
- A GitHub Actions workflow is included as an example to build and push to GHCR:
  - Add the repository secret HUGGINGFACE_API_TOKEN before running deployments.
  - The workflow uses the built repository owner/name to tag the image as ghcr.io/{owner}/{repo}:latest.

Notes
- This proxy avoids exposing your Hugging Face token client-side.
- Make sure to set environment variables (HUGGINGFACE_API_TOKEN and HF_MODEL_ID) as secrets in GitHub if you use Actions.

Security reminders
- Never commit your HUGGINGFACE_API_TOKEN to the repo.
- In CI use the repository secret HUGGINGFACE_API_TOKEN (Settings → Secrets and variables → Actions).
- Consider rate-limiting or authentication on /api/chat before exposing publicly.