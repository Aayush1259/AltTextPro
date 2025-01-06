from huggingface_hub import InferenceClient

class Enhanced_context:
    def __init__(self, api_key: str):
        self.client = InferenceClient(api_key=api_key)

    def generate_enhanced_context(self, context: str) -> str:
        if not context:
            raise ValueError("No context provided for generating enhanced context.")

        try:
            messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": "Generate the enhanced context from context, with high vocab and don't include headings in jsust 175 to 200 words."},
                        {"type": "text", "text": context}
                    ],
                }
            ]

            completion = self.client.chat.completions.create(
                model="meta-llama/Llama-3.2-11B-Vision-Instruct",
                messages=messages,
                max_tokens=500
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error generating context: {str(e)}")