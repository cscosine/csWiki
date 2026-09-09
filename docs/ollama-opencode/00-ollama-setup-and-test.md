<!-- TOC BEGIN -->
## Table Of Contents
- [← Back : ollama-opencode](ollama-opencode.md)
- [Ollama Local Model Testing](#ollama-local-model-testing)
<!-- TOC END -->

# Ollama Local Model Testing

## Hardware

* Ubuntu 22.04.5 LTS
* Intel i7-11850H — 8 cores / 16 threads
* 31 GiB RAM
* NVIDIA RTX A3000 Laptop GPU — 6 GiB VRAM
* NVIDIA driver 580.173.02
* CUDA 13.0

---

## Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Check:

```bash
ollama --version
```

Tested:

```text
0.33.3
```

Check the Ollama API:

```bash
curl http://127.0.0.1:11434/api/tags
```

---

## Pull Models

### Qwen 2.5 Coder 3B

```bash
ollama pull qwen2.5-coder:3b
```

Observed size:

```text
~2.2 GB
```

Run:

```bash
ollama run qwen2.5-coder:3b
```

### Qwen 2.5 Coder 7B

```bash
ollama pull qwen2.5-coder:7b
```

Observed size:

```text
~5.1 GB
```

Run:

```bash
ollama run qwen2.5-coder:7b
```

### Qwen3 8B

```bash
ollama pull qwen3:8b
```

Run:

```bash
ollama run qwen3:8b
```

Model information:

```bash
ollama show qwen3:8b
```

Observed:

```text
Architecture:     qwen3
Parameters:       8.2B
Quantization:     Q4_K_M
Context:          40960
Capabilities:     completion, tools, thinking
```

---

## Monitor GPU / Memory

In another terminal:

```bash
watch -n 1 nvidia-smi
```

Also:

```bash
ollama ps
```

Watch:

* GPU VRAM usage
* GPU utilization
* CPU/GPU split
* model memory usage
* context size

---

## Basic Timing Test

Run a model:

```bash
time ollama run qwen2.5-coder:3b
```

Then ask a simple coding question, for example:

```text
Write a Python program that prints Hello World.
```

Repeat for each model.

Record:

* total response time
* whether the model fits completely in VRAM
* CPU/GPU split
* amount of reasoning
* response quality

---

## Observed Results

### Qwen2.5 Coder 3B

```text
Size:       ~2.2 GB
GPU:        100%
Context:    4096
Time:       ~4 seconds
```

Fits completely in the 6 GB GPU.

**Very fast.**

---

### Qwen2.5 Coder 7B

```text
Size:       ~5.1 GB
GPU:        ~27%
CPU:        ~73%
Context:    4096
Time:       ~36 seconds
```

Does not fit completely in VRAM at runtime.

**Much slower because of CPU/GPU offloading.**

---

### Qwen3 8B

```text
Parameters: 8.2B
Quantization: Q4_K_M
Context: 40960
Capabilities: completion, tools, thinking
```

Native tool-calling test produced a real:

```text
tool_calls
```

response when using the Ollama API with:

```json
"think": false
```

The model can therefore produce native tool calls, but thinking mode can make responses considerably more verbose.

---

## Native Tool-Calling Test

Test Qwen3 directly through the Ollama OpenAI-compatible API:

```bash
curl -s http://127.0.0.1:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:8b",
    "messages": [
      {
        "role": "user",
        "content": "Create greeting.txt containing exactly Hello. Use the write_file tool."
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "write_file",
          "description": "Write content to a file",
          "parameters": {
            "type": "object",
            "properties": {
              "path": {"type": "string"},
              "content": {"type": "string"}
            },
            "required": ["path", "content"]
          }
        }
      }
    ],
    "think": false
  }' | python3 -m json.tool
```

Look for:

```text
"tool_calls"
```

A successful response contains a tool call similar to:

```json
{
  "name": "write_file",
  "arguments": {
    "path": "greeting.txt",
    "content": "Hello"
  }
}
```

The important distinction is that `tool_calls` should appear as an API field, rather than the model simply printing JSON as normal text.
