from huggingface_hub import InferenceClient
from io import BytesIO
from PIL import Image
import base64

class Caption:
    def __init__(self, api_key: str):
        self.client = InferenceClient(api_key=api_key)

    def preprocess_large_image(self, image_bytes: bytes, max_size: int = 1024, quality: int = 85) -> bytes:
        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            image.save(buffer, format="JPEG", quality=quality)
            buffer.seek(0)
            return buffer.read()
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")

    def generate_caption(self, image_bytes: bytes) -> str:
        try:
            processed_image_bytes = self.preprocess_large_image(image_bytes)
            image_base64 = base64.b64encode(processed_image_bytes).decode("utf-8")

            messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": "Caption the image in 15 to 25 words."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ],
                }
            ]
            completion = self.client.chat.completions.create(
                model="meta-llama/Llama-3.2-11B-Vision-Instruct",
                messages=messages,
                max_tokens=100
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error generating caption: {str(e)}")