---
name: modelscope-image
description: Generate images using ModelScope (魔搭) API with intelligent aspect ratio calculation. Automatically triggered when users need to generate images, create visual content, or request "生成图片", "图片生成", "ModelScope", or "魔搭". Supports Z-Image-Turbo (default) and Qwen-Image models with automatic API key management and smart dimension calculation (long edge ≤2048px).
---

# ModelScope Image Generator

Generate high-quality images using ModelScope API with automatic aspect ratio calculation and configuration management.

## Quick Start

When a user asks to generate an image:

1. **Check configuration** (first-time setup)
2. **Generate image** with appropriate parameters
3. **Return the generated image** path and details

## First-Time Setup

Before generating images, verify API key configuration:

```bash
python scripts/config_manager.py check
```

**If not configured:**

1. Guide the user to obtain an API key:
   - Visit: https://modelscope.cn/my/myaccesstoken
   - Copy the API Token

2. Save the API key:
   ```bash
   python scripts/config_manager.py set api_key USER_API_KEY
   ```

3. Verify configuration:
   ```bash
   python scripts/config_manager.py check
   ```

## Generating Images

### Basic Usage

```bash
python scripts/image_generator.py "prompt" \
  --aspect-ratio "16:9" \
  --output "output.png"
```

### Parameters

**Required:**
- `prompt`: Image description (text prompt)

**Optional:**
- `--aspect-ratio` / `-a`: Aspect ratio (default: `1:1`)
  - Presets: `2.35:1`, `21:9`, `16:9`, `3:2`, `1:1`, `9:16`, etc.
  - Custom: Any format like `"4:3"` or `"2.35:1"`
- `--long-edge` / `-l`: Long edge pixel length (64-2048, default: 2048)
- `--model` / `-m`: Model selection
  - `z-image` (default): Tongyi-MAI/Z-Image-Turbo
  - `qwen-image`: Qwen/Qwen-Image-2512
- `--output` / `-o`: Output file path (auto-generated if omitted)
- `--timeout` / `-t`: Timeout in seconds (default: 300)
- `--polling-interval` / `-p`: Polling interval in seconds (default: 5)

### Aspect Ratio Calculation

The skill automatically calculates pixel dimensions based on aspect ratio and long edge:

**Algorithm:**
1. Parse aspect ratio (e.g., `16:9` → width ratio: 16, height ratio: 9)
2. Determine orientation:
   - **Landscape/Square** (width ≥ height): Long edge → width
   - **Portrait** (width < height): Long edge → height
3. Calculate the other dimension proportionally
4. Clamp dimensions to 64-2048 range

**Examples:**
- `16:9` with long edge 2048 → `2048×1152`
- `9:16` with long edge 2048 → `1152×2048`
- `1:1` with long edge 1024 → `1024×1024`
- `21:9` with long edge 2048 → `2048×878`

## Usage Examples

### Example 1: Standard Generation

```bash
python scripts/image_generator.py "一只金色的猫坐在天鹅绒垫子上" \
  --aspect-ratio "1:1"
```

### Example 2: Widescreen Image

```bash
python scripts/image_generator.py "赛博朋克城市夜景，霓虹灯闪烁" \
  --aspect-ratio "21:9" \
  --long-edge 2048 \
  --output "cyberpunk_city.png"
```

### Example 3: Portrait with Custom Model

```bash
python scripts/image_generator.py "古风美人肖像" \
  --aspect-ratio "9:16" \
  --model qwen-image \
  --output "portrait.png"
```

### Example 4: Quick Square Image

```bash
python scripts/image_generator.py "山水画，中国风" \
  --aspect-ratio "1:1" \
  --long-edge 1024
```

## User Interaction Flow

### When User Requests Image Generation

**Step 1: Configuration Check**

```python
# Check if configured
python scripts/config_manager.py check
```

If not configured, guide the user through setup (see "First-Time Setup" above).

**Step 2: Parameter Selection**

Ask the user (or infer from context):
- **Prompt**: What image to generate?
- **Aspect ratio**: What orientation? (default: 1:1)
  - Suggest based on content:
    - Landscape photos: `16:9` or `21:9`
    - Portraits: `9:16` or `2:3`
    - Social media: `1:1` or `4:5`
- **Model**: Use default (`z-image`) unless user specifies

**Step 3: Generate**

```bash
python scripts/image_generator.py "USER_PROMPT" \
  --aspect-ratio "RATIO" \
  --output "OUTPUT_PATH"
```

**Step 4: Return Results**

Provide the user with:
- ✅ Generated image path
- 📐 Final dimensions
- ⏱️ Generation time
- 🎨 Model used

## Configuration Management

### View Current Configuration

```bash
# View all settings (API key masked)
python scripts/config_manager.py get all

# View specific setting
python scripts/config_manager.py get default_model
```

### Update Configuration

```bash
# Change default model
python scripts/config_manager.py set default_model "Qwen/Qwen-Image-2512"

# Change base URL
python scripts/config_manager.py set base_url "https://api-inference.modelscope.cn/"
```

### Reset Configuration

```bash
python scripts/config_manager.py reset
```

## Supported Aspect Ratios

| Ratio | Orientation | Example Dimensions (long edge=2048) |
|-------|-------------|-------------------------------------|
| 2.35:1 | Ultra-wide | 2048×871 |
| 21:9 | Cinematic | 2048×878 |
| 16:9 | Widescreen | 2048×1152 |
| 3:2 | Photo | 2048×1365 |
| 1:1 | Square | 2048×2048 |
| 2:3 | Photo Portrait | 1365×2048 |
| 9:16 | Mobile Portrait | 1152×2048 |

## Error Handling

### Common Errors

**1. API Key Not Configured**
```
❌ 错误: 未配置 API Key！
请访问 https://modelscope.cn/my/myaccesstoken 获取 API Key
```
→ Run setup: `python scripts/config_manager.py set api_key YOUR_KEY`

**2. Invalid Aspect Ratio**
```
❌ 无效的宽高比格式: xyz
```
→ Use format like `16:9` or `2.35:1`

**3. Timeout**
```
❌ 任务超时（300秒）
```
→ Increase timeout: `--timeout 600`

**4. API Error**
```
❌ 图片生成失败: insufficient quota
```
→ Check API quota at ModelScope dashboard

## Technical Details

### Configuration Location

```
~/.modelscope-image/
└── config.json
    {
      "api_key": "YOUR_API_KEY",
      "base_url": "https://api-inference.modelscope.cn/",
      "default_model": "Tongyi-MAI/Z-Image-Turbo"
    }
```

### API Workflow

1. **Submit Task** (POST `/v1/images/generations`)
   - Headers: `Authorization`, `X-ModelScope-Async-Mode: true`
   - Body: `{ model, prompt, size }`
   - Returns: `task_id`

2. **Poll Status** (GET `/v1/tasks/{task_id}`)
   - Headers: `Authorization`, `X-ModelScope-Task-Type: image_generation`
   - Poll until: `task_status` → `SUCCEED` or `FAILED`

3. **Download Image** (GET `output_images[0]`)
   - Save to specified path or auto-generate filename

### Dependencies

```python
requests  # HTTP requests
Pillow    # Image processing
```

Install with: `pip install requests Pillow`

## Best Practices

1. **Always check configuration first** before generating images
2. **Suggest appropriate aspect ratios** based on content type:
   - Landscape/scenery: `16:9`, `21:9`
   - Portraits: `9:16`, `2:3`
   - Product photos: `1:1`, `4:5`
3. **Use default model (z-image)** unless user requests otherwise
4. **Set appropriate long edge**:
   - High quality: 2048 (default)
   - Faster generation: 1024
   - Testing: 512
5. **Handle errors gracefully** and provide actionable guidance

## Notes

- **Long edge limit**: Maximum 2048 pixels (API constraint)
- **Dimension clamping**: All dimensions constrained to 64-2048 range
- **Timeout**: Default 300s, increase for complex prompts
- **Polling**: Default 5s interval, adjust based on generation speed
- **LoRA support**: Available but not exposed in basic usage (see script source)
