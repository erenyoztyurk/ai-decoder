import os
import requests
import logging
from io import BytesIO
from PIL import Image
from typing import Optional, Tuple
from datetime import datetime
from slugify import slugify

class ImageAutomationEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key: str = api_key or os.getenv("OPENAI_API_KEY", "")
        self.api_url: str = "https://api.openai.com/v1/images/generations"
        self.output_dir: str = "public/assets/admin/generated"
        self._ensure_output_dir()
        self._setup_logger()

    def _ensure_output_dir(self) -> None:
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def _setup_logger(self) -> None:
        self.logger = logging.getLogger("ImageGen")
        self.logger.setLevel(logging.INFO)

    def generate_cover_image(self, prompt: str, title: str) -> Optional[str]:
        try:
            if not self.api_key:
                raise ValueError("API anahtarı bulunamadı.")

            headers: dict = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            data: dict = {
                "model": "dall-e-3",
                "prompt": f"Professional blog cover style, minimalist, modern, high quality: {prompt}",
                "n": 1,
                "size": "1024x1024",
                "response_format": "url"
            }

            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            image_url: str = response.json()["data"][0]["url"]
            return self._process_and_save_image(image_url, title)

        except Exception as e:
            self.logger.error(f"Görsel üretim hatası: {str(e)}")
            return None

    def _process_and_save_image(self, url: str, title: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            img: Image.Image = Image.open(BytesIO(response.content))
            
            filename: str = f"{slugify(title)}_{datetime.now().strftime('%Y%m%d%H%M')}.webp"
            filepath: str = os.path.join(self.output_dir, filename)

            img.save(filepath, "WEBP", quality=80, method=6)
            
            self.logger.info(f"Görsel başarıyla kaydedildi: {filepath}")
            return f"/assets/admin/generated/{filename}"

        except Exception as e:
            self.logger.error(f"Görsel işleme hatası: {str(e)}")
            return None

    def optimize_existing_image(self, input_path: str, target_width: int = 1200) -> bool:
        try:
            if not os.path.exists(input_path):
                return False

            with Image.open(input_path) as img:
                ratio: float = target_width / float(img.size[0])
                target_height: int = int(float(img.size[1]) * float(ratio))
                
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                base_name: str = os.path.splitext(input_path)[0]
                output_path: str = f"{base_name}_optimized.webp"
                
                img.save(output_path, "WEBP", quality=85)
                return True

        except Exception as e:
            self.logger.error(f"Optimizasyon hatası: {str(e)}")
            return False

if __name__ == "__main__":
    engine = ImageAutomationEngine()
    test_title = "Yapay Zeka Otomasyon Sistemleri"
    test_prompt = "Futuristic AI server room with glowing blue lines"
    result = engine.generate_cover_image(test_prompt, test_title)
    print(f"Sonuç: {result}") 
