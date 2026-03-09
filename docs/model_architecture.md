# Model Architecture — LLaMA 3.3 70B Versatile

## 1. Overview

| Property | Value |
|----------|-------|
| Model Name | Meta LLaMA 3.3 70B Versatile |
| Developer | Meta AI |
| Served Via | Groq Cloud API |
| Parameters | 70 Billion |
| Model Family | LLaMA 3 (Large Language Model Meta AI) |
| Type | Decoder-only Transformer (Causal LM) |
| Context Window | 128,000 tokens |
| Vocabulary Size | 128,256 tokens |
| License | Meta Llama 3 Community License |

---

## 2. Transformer Architecture (Detailed)

LLaMA 3.3 70B is a **decoder-only transformer** — the same fundamental architecture as GPT, but with several modern improvements.

```
Input Text
    ↓
Tokenization (BPE, vocab = 128,256)
    ↓
Token Embedding Layer  [dim = 8192]
    ↓
┌─────────────────────────────────────────┐
│  Transformer Block × 80   ← HIDDEN LAYERS
│                                         │
│   ┌─────────────────────────────────┐   │
│   │  RMSNorm                        │   │
│   │  ↓                              │   │
│   │  Grouped Query Attention (GQA)  │   │
│   │    Q heads : 64                 │   │
│   │    KV heads: 8                  │   │
│   │    Head dim: 128                │   │
│   │  ↓                              │   │
│   │  Residual Connection            │   │
│   │  ↓                              │   │
│   │  RMSNorm                        │   │
│   │  ↓                              │   │
│   │  Feed-Forward Network (SwiGLU)  │   │
│   │    Hidden dim : 28,672          │   │
│   │  ↓                              │   │
│   │  Residual Connection            │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
    ↓
Final RMSNorm
    ↓
Linear (lm_head)  [8192 → 128,256]
    ↓
Output Token Logits
```

---

## 3. Key Architectural Parameters

| Component | Value |
|-----------|-------|
| **Number of Hidden (Transformer) Layers** | **80** |
| Hidden Dimension (d_model) | 8,192 |
| Attention Heads (Q) | 64 |
| Key-Value Heads (GQA) | 8 |
| Head Dimension | 128 |
| Feed-Forward Hidden Dim | 28,672 |
| Activation Function | SwiGLU |
| Normalization | RMSNorm (no bias) |
| Positional Encoding | RoPE (Rotary Position Embedding) |
| Attention Type | Grouped Query Attention (GQA) |
| Tied Embeddings | No |

---

## 4. What Are Hidden Layers?

In this transformer model, the **hidden layers are the 80 stacked Transformer Blocks**. Each block is called a "hidden layer" because:

- The input layer = token embeddings
- The output layer = the final linear projection (lm_head) to vocabulary
- Everything in between = hidden layers

Each of the 80 hidden layers contains:
1. **Self-Attention sub-layer** — learns which tokens to attend to
2. **Feed-Forward Network (FFN) sub-layer** — learns non-linear feature transformations

So total sub-layers = 80 × 2 = **160 sub-layers** inside the model.

---

## 5. Grouped Query Attention (GQA)

Standard multi-head attention uses Q, K, V heads equally (64 each for a 70B model). GQA reduces K and V heads to 8, while keeping Q heads at 64:

```
Standard MHA:   Q_heads=64   K_heads=64   V_heads=64
GQA (LLaMA 3):  Q_heads=64   K_heads=8    V_heads=8
```

**Why?** Reduces memory (KV cache) by 8× while keeping model quality nearly identical. Enables the large 128K context window.

---

## 6. SwiGLU Activation Function

The FFN uses SwiGLU instead of the standard ReLU:

$$\text{SwiGLU}(x, W, V, b, c) = \text{Swish}(xW + b) \odot (xV + c)$$

$$\text{Swish}(x) = x \cdot \sigma(x)$$

SwiGLU uses a gating mechanism that allows fine-grained control over information flow, significantly improving performance over ReLU at scale.

---

## 7. RoPE Positional Encoding

Instead of adding fixed or learned position embeddings to tokens, LLaMA 3 applies **Rotary Position Embeddings (RoPE)** directly inside the attention calculation:

- Rotates Q and K vectors by an angle proportional to their position
- Naturally encodes relative distances between tokens
- Scales to longer contexts (128K tokens) better than absolute embeddings

---

## 8. RMSNorm

LLaMA 3.3 uses **Root Mean Square Layer Normalization** (Pre-Norm, applied before each sub-layer):

$$\text{RMSNorm}(x) = \frac{x}{\text{RMS}(x)} \cdot \gamma, \quad \text{RMS}(x) = \sqrt{\frac{1}{n}\sum x_i^2}$$

Simpler and faster than LayerNorm — no mean subtraction or bias term.

---

## 9. How This Project Uses the Model

```
User uploads PDF / PPTX / TXT
         ↓
  extractor.py
  • PyPDF2 extracts text
  • Tesseract OCR fallback for scanned PDFs
         ↓
  mcq_generator.py  →  Groq API  →  LLaMA 3.3 70B
  • System prompt: "You are a helpful assistant..."
  • User prompt: text + "generate N MCQs, return JSON"
  • temperature = 0.7   (creative but consistent)
  • max_tokens  = 4000
         ↓
  parse_response()
  • Strips markdown code fences
  • JSON.parse → list of question objects
         ↓
  Frontend renders MCQs with correct answers highlighted
```

### Inference Parameters Used

| Parameter | Value | Effect |
|-----------|-------|--------|
| `temperature` | 0.7 | Moderate creativity — varied but sensible questions |
| `max_tokens` | 4000 | Enough for up to ~50 questions with options |
| `model` | `llama-3.3-70b-versatile` | Best quality/speed balance on Groq |

---

## 10. Why LLaMA 3.3 70B via Groq?

| Reason | Detail |
|--------|--------|
| **Free API** | Groq offers a generous free tier — no cost for this project |
| **Speed** | Groq's LPU hardware runs LLaMA at 800+ tokens/sec (fastest available) |
| **Quality** | 70B parameters → excellent instruction following and JSON output |
| **Context** | 128K token window handles large documents |
| **No GPU needed** | Entirely API-based — runs on any server/free hosting |

---

## 11. Parameter Count Breakdown (approx.)

| Component | Parameters |
|-----------|-----------|
| Token Embeddings | 128,256 × 8,192 ≈ **1.05B** |
| 80 × Attention (Q,K,V,O) | 80 × (64×8192×128 + 8×8192×128 ×2 + 64×128×8192) ≈ **22B** |
| 80 × Feed-Forward (SwiGLU) | 80 × (8192×28672 ×3) ≈ **56B** |
| 80 × RMSNorm | negligible |
| lm_head | 8,192 × 128,256 ≈ **1.05B** |
| **Total** | **~70B** |

---

## 12. ML/DL Features (For Viva/Presentation)

### Attention Mechanism
- **Grouped Query Attention (GQA)** — 64 Query heads, 8 Key-Value heads
- Reduces KV cache memory by 8× while maintaining accuracy
- Scaled dot-product attention:

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

### Activation Function
- **SwiGLU** (Swish-Gated Linear Unit)

$$\text{SwiGLU}(x) = \text{Swish}(xW) \odot (xV), \quad \text{Swish}(x) = x \cdot \sigma(x)$$

- Better gradient flow than ReLU at large scale

### Normalization
- **RMSNorm** — applied **before** each sub-layer (Pre-Norm)

$$\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{n}\sum x_i^2}} \cdot \gamma$$

- No mean subtraction, faster and more stable than LayerNorm

### Positional Encoding
- **RoPE** (Rotary Position Embedding)
- Encodes relative position directly inside attention computation
- Generalizes to longer sequences better than learned absolute embeddings

### Optimization (Training)
- **AdamW optimizer** — Adam + weight decay for regularization
- **Cosine learning rate schedule** with linear warmup
- **Gradient clipping** to prevent exploding gradients

### Regularization
- Weight decay via AdamW
- Dropout in attention layers during training (disabled at inference)
- Pre-Norm architecture improves training stability

### Loss Function
- **Cross-Entropy Loss** (Causal Language Modeling / next-token prediction)

$$\mathcal{L} = -\sum_{t} \log P(x_t \mid x_{<t})$$

### Training Technique
- **Self-supervised learning** — pre-trained on trillions of tokens, no labeled data needed
- **SFT** (Supervised Fine-Tuning) on high-quality instruction datasets
- **RLHF** (Reinforcement Learning from Human Feedback) — fine-tuned for instruction following

### Transfer Learning
- Pre-trained general knowledge → fine-tuned for instructions
- This project uses it via **zero-shot prompting** — no further training or fine-tuning needed

### Tokenization
- **Byte Pair Encoding (BPE)** — vocabulary of 128,256 tokens
- Handles subwords, rare words, and multiple languages efficiently

---

### Quick-Answer Table (if sir asks directly)

| Question | Answer |
|----------|--------|
| Hidden layers? | **80** Transformer blocks |
| Activation function? | **SwiGLU** |
| Normalization? | **RMSNorm** (Pre-Norm) |
| Attention type? | **Grouped Query Attention (GQA)** |
| Positional encoding? | **RoPE** |
| Loss function? | **Cross-Entropy** |
| Optimizer? | **AdamW** |
| Training method? | **Self-supervised + RLHF** |
| Parameters? | **70 Billion** |
| Context window? | **128,000 tokens** |
| Tokenizer? | **BPE (vocab 128,256)** |
| Model type? | **Decoder-only Transformer** |

---

## 13. Summary for Presentation

> **"In this project we use Meta's LLaMA 3.3 70B model, a decoder-only transformer with 80 hidden layers, 70 billion parameters, and a 128,000 token context window. Each hidden layer contains a Grouped Query Attention block (64 Q-heads, 8 KV-heads) and a SwiGLU feed-forward network with hidden dimension 28,672. The model is served via the Groq Cloud API, which provides near-instant inference using custom LPU hardware. Text is first extracted from the uploaded document (with OCR fallback for scanned PDFs), then sent to the model with a structured prompt requesting JSON output. The response is parsed and rendered as interactive MCQs on the frontend."**
