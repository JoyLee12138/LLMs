"""


使用 GPT-4.1 Vision（经 n1n 中转，chat.completions 兼容写法）
解析汽车电路图 PDF，提取电路元器件名称（不依赖 OCR）

作者视角：资深汽车电路工程师
"""

import json
import base64
import io
from pathlib import Path

import fitz            
import cv2             
import numpy as np
from PIL import Image
from openai import OpenAI


# =========================================================
# 一、配置区（⚠️ 只改这里）
# =========================================================

DPI = 300              # PDF 渲染精度（300 对电路图最稳）
TILE_SIZE = 2048       # 单次送入模型的图像尺寸
OVERLAP = 200          # 分块重叠，防止元器件被切断

OPENAI_API_KEY = "sk"
BASE_URL = "https://api.n1n.ai/v1"

MODEL_NAME = "gpt-4.1"   # n1n 可用的 Vision 模型名


SYSTEM_PROMPT = """
你是一名资深汽车电路工程师。

你正在查看整车线束电路图，请严格遵守以下规则：
1. 只识别并输出【电路元器件名称】
2. 元器件包括但不限于：
   - ECU / BCM / VCU / ABS / EBS 等控制器
   - 继电器（如：继电器K1、K12）
   - 保险（如：保险F3、F23）
   - 插接器 / 接插件（如：C101、C3-12）
   - 各类传感器、电磁阀、电机、执行器
3. 忽略标题栏、版本号、日期、图号
4. 忽略导线编号、端子编号、线号
5. 如果不确定是不是元器件名称，请忽略
6. 不要解释说明，只输出 JSON 数组
"""

USER_PROMPT = "请从这张汽车电路图中，识别所有元器件名称。"


# =========================================================
# 二、PDF → 图片
# =========================================================

def pdf_to_images(pdf_path: Path, out_dir: Path, dpi: int):
    out_dir.mkdir(exist_ok=True)
    doc = fitz.open(pdf_path)

    images = []
    for i, page in enumerate(doc):
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img_path = out_dir / f"page_{i+1}.png"
        pix.save(img_path)
        images.append(img_path)

    return images


# =========================================================
# 三、图片分块
# =========================================================

def split_image(image_path: Path, tile_size: int, overlap: int):
    img = cv2.imread(str(image_path))
    h, w, _ = img.shape
    tiles = []

    step = tile_size - overlap
    for y in range(0, h, step):
        for x in range(0, w, step):
            tile = img[y:y + tile_size, x:x + tile_size]
            if tile.size > 0:
                tiles.append(tile)

    return tiles


# =========================================================
# 四、GPT-4.1 Vision Client（n1n 稳定写法）
# =========================================================

class GPT41VClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=BASE_URL
        )

    def _image_to_data_url(self, image: np.ndarray) -> str:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)

        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")

        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"

    def chat(self, system: str, user: str, image: np.ndarray) -> str:
        image_url = self._image_to_data_url(image)

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content


# =========================================================
# 五、VLM Agent
# =========================================================

class VLMAgent:
    def __init__(self, client: GPT41VClient):
        self.client = client

    def extract_components(self, image: np.ndarray):
        try:
            text = self.client.chat(
                system=SYSTEM_PROMPT,
                user=USER_PROMPT,
                image=image
            )

            data = json.loads(text)
            if isinstance(data, list):
                return data
        except Exception as e:
            print(f"[WARN] 解析失败，已跳过：{e}")

        return []


# =========================================================
# 六、主解析流程
# =========================================================

def parse_circuit_pdf(pdf_path: str):
    pdf_path = Path(pdf_path)
    assert pdf_path.exists(), "PDF 文件不存在"

    print(f"[INFO] 开始解析 PDF: {pdf_path.name}")

    pages_dir = Path("pages")
    images = pdf_to_images(pdf_path, pages_dir, DPI)
    print(f"[INFO] 共生成 {len(images)} 页")

    agent = VLMAgent(GPT41VClient())
    all_components = set()

    # for page_idx, img_path in enumerate(images, start=1):
    for page_idx, img_path in enumerate(images[5:6], start=6): 
        print(f"[INFO] 解析第 {page_idx} 页")

        tiles = split_image(img_path, TILE_SIZE, OVERLAP)

        for tile in tiles:
            components = agent.extract_components(tile)
            for c in components:
                c = c.strip()
                if c:
                    all_components.add(c)

    return sorted(all_components)


# =========================================================
# 七、程序入口
# =========================================================

if __name__ == "__main__":

    pdf_file = r"D:\Code\ML\LLMs\class6Agent\test\test_pic.pdf"

    components = parse_circuit_pdf(pdf_file)

    print("\n========== 解析到的元器件 ==========")
    for c in components:
        print(c)
