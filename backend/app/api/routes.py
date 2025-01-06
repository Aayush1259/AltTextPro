from flask import Blueprint, request, jsonify
from app.services import context
from app.services import enhanced_context
from app.services import sentiment
from app.services import caption
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

bp = Blueprint('api', __name__, url_prefix='/api')

sentiment_service = sentiment.Sentiment()

# Retrieve API key from environment variables
api_key = os.getenv("API_KEY")
caption_generator = caption.Caption(api_key)
context_generator = context.Context(api_key)
enhanced_context_generator = enhanced_context.Enhanced_context(api_key)


@bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working"})

@bp.route('/generate-context', methods=['POST'])
def generate_context():
    try:
        data = request.get_json()
        caption_text = data.get('caption')
        if not caption_text:
            return jsonify({"error": "Caption is required"}), 400
        
        context_result = context_generator.generate_context(caption_text)
        enhanced_context = enhanced_context_generator.enhance_context(context_result)
        
        return jsonify({
            "original_context": context_result,
            "enhanced_context": enhanced_context
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    image_bytes = file.read()

    try:
        caption_text = caption_generator.generate_caption(image_bytes)
        context_result = context_generator.generate_context(image_bytes)
        enhanced_context = enhanced_context_generator.generate_enhanced_context(context_result)
        sentiment_result = sentiment_service.analyze_sentiment(enhanced_context)

        response_data = {
            "caption": caption_text,
            "original_context": context_result,
            "enhanced_context": enhanced_context,
            "sentiment_analysis": sentiment_result
        }

        return jsonify(response_data), 200
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": str(e)}), 500