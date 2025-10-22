from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import math

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
genai.configure(api_key=GEMINI_API_KEY)

# Product database for market reference
PRODUCT_DATABASE = {
    'iphone': {
        'categories': ['iPhone 14', 'iPhone 13', 'iPhone 12', 'iPhone SE'],
        'baseDepreciation': 0.15,
        'marketFactor': 0.85
    },
    'macbook': {
        'categories': ['MacBook Pro', 'MacBook Air', 'MacBook'],
        'baseDepreciation': 0.12,
        'marketFactor': 0.80
    },
    'laptop': {
        'categories': ['Dell', 'HP', 'Lenovo', 'ASUS'],
        'baseDepreciation': 0.15,
        'marketFactor': 0.75
    },
    'tablet': {
        'categories': ['iPad', 'Samsung Tab', 'iPad Pro'],
        'baseDepreciation': 0.14,
        'marketFactor': 0.78
    },
    'camera': {
        'categories': ['DSLR', 'Mirrorless', 'Action Camera'],
        'baseDepreciation': 0.10,
        'marketFactor': 0.82
    },
    'smartwatch': {
        'categories': ['Apple Watch', 'Samsung Watch', 'Fitbit'],
        'baseDepreciation': 0.18,
        'marketFactor': 0.72
    },
    'headphones': {
        'categories': ['AirPods', 'Sony', 'Bose', 'JBL'],
        'baseDepreciation': 0.20,
        'marketFactor': 0.70
    },
    'gaming': {
        'categories': ['PlayStation', 'Xbox', 'Nintendo'],
        'baseDepreciation': 0.16,
        'marketFactor': 0.76
    }
}

# Condition multipliers
CONDITION_MULTIPLIERS = {
    'New': 0.95,
    'Like New': 0.85,
    'Good': 0.70,
    'Fair': 0.50,
    'Poor': 0.30
}

def get_product_depreciation(product_name):
    """Get depreciation rate for product type"""
    product_lower = product_name.lower()
    
    for key, value in PRODUCT_DATABASE.items():
        if key in product_lower:
            return value['baseDepreciation']
    
    return 0.15  # Default depreciation

def calculate_market_price(product_name, condition, usage_months, warranty, original_price):
    """Calculate market price based on condition and usage"""
    
    # Base depreciation per month
    depreciation_rate = get_product_depreciation(product_name) / 12
    
    # Calculate price based on condition
    condition_price = original_price * CONDITION_MULTIPLIERS.get(condition, 0.70)
    
    # Apply depreciation for usage months
    depreciated_price = condition_price * math.pow(1 - depreciation_rate, usage_months)
    
    # Warranty bonus
    warranty_bonus = 1.05 if warranty == 'Yes' else 1.0
    
    # Final market price
    market_price = depreciated_price * warranty_bonus
    
    # Ensure minimum value (10% of original)
    market_price = max(market_price, original_price * 0.1)
    
    # Calculate loss
    price_loss = original_price - market_price
    percentage_loss = (price_loss / original_price) * 100
    
    return {
        'estimatedMarketPrice': round(market_price, 2),
        'marketComparison': {
            'online': round(market_price * 0.95, 2),
            'retail': round(market_price * 1.05, 2),
            'wholesale': round(market_price * 0.80, 2)
        },
        'depreciation': {
            'priceLoss': round(price_loss, 2),
            'percentageLoss': round(percentage_loss, 2),
            'monthlyDepreciation': round(depreciation_rate * 100, 2)
        }
    }

def get_recommendation(market_price, original_price):
    """Get selling recommendation"""
    retained_value = (market_price / original_price) * 100
    
    if retained_value > 70:
        return 'Excellent - Strong market demand'
    elif retained_value > 50:
        return 'Good - Reasonable resale value'
    elif retained_value > 30:
        return 'Fair - Moderate depreciation'
    else:
        return 'Poor - High depreciation rate'

def prepare_analysis_prompt(product_data, prediction):
    """Prepare detailed analysis prompt for Gemini"""
    
    prompt = f"""Analyze the pricing data for this product and provide market insights.

Product: {product_data['productName']}
Condition: {product_data['condition']}
Usage Duration: {product_data['usageMonths']} months
Warranty: {product_data['warranty']}
Original Price: ${product_data['originalPrice']:.2f}

Calculated Market Data:
- Estimated Market Price: ${prediction['estimatedMarketPrice']:.2f}
- Online Price Range: ${prediction['marketComparison']['online']:.2f}
- Retail Price Range: ${prediction['marketComparison']['retail']:.2f}
- Wholesale Price: ${prediction['marketComparison']['wholesale']:.2f}
- Total Depreciation: {prediction['depreciation']['percentageLoss']}%
- Monthly Depreciation Rate: {prediction['depreciation']['monthlyDepreciation']}%

Please provide:
1. Market analysis summary (2-3 sentences)
2. Key factors affecting the price (3 points)
3. Selling recommendations (2-3 tips)
4. Price comparison with market trends
5. Best platforms to sell for optimal price

Keep the response concise and practical."""
    
    return prompt

def get_gemini_analysis(prompt):
    """Get analysis from Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return f"Error fetching AI insights: {str(e)}"

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_price():
    """API endpoint for price prediction"""
    try:
        data = request.json
        
        # Validate input
        required_fields = ['productName', 'condition', 'usageMonths', 'warranty', 'originalPrice']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        product_data = {
            'productName': data['productName'].strip(),
            'condition': data['condition'],
            'usageMonths': int(data['usageMonths']),
            'warranty': data['warranty'],
            'originalPrice': float(data['originalPrice'])
        }
        
        # Validate values
        if product_data['originalPrice'] <= 0:
            return jsonify({'error': 'Original price must be greater than 0'}), 400
        
        if product_data['usageMonths'] < 0:
            return jsonify({'error': 'Usage months cannot be negative'}), 400
        
        if product_data['condition'] not in CONDITION_MULTIPLIERS:
            return jsonify({'error': 'Invalid condition'}), 400
        
        # Calculate market price
        prediction = calculate_market_price(
            product_data['productName'],
            product_data['condition'],
            product_data['usageMonths'],
            product_data['warranty'],
            product_data['originalPrice']
        )
        
        # Add recommendation
        prediction['recommendation'] = get_recommendation(
            prediction['estimatedMarketPrice'],
            product_data['originalPrice']
        )
        
        # Prepare analysis prompt
        analysis_prompt = prepare_analysis_prompt(product_data, prediction)
        
        # Get AI insights
        ai_insights = get_gemini_analysis(analysis_prompt)
        
        # Return results
        return jsonify({
            'success': True,
            'productData': product_data,
            'prediction': prediction,
            'aiInsights': ai_insights,
            'timestamp': datetime.now().isoformat()
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get list of supported product types"""
    products = []
    for key, value in PRODUCT_DATABASE.items():
        products.append({
            'type': key,
            'categories': value['categories']
        })
    return jsonify({'products': products})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_configured': bool(GEMINI_API_KEY)
    })

if __name__ == '__main__':
    print("🚀 Starting AI Price Prediction Server...")
    print(f"✅ Gemini API Key: {'Configured' if GEMINI_API_KEY else 'Not found'}")
    print("📊 Available Products: ", list(PRODUCT_DATABASE.keys()))
    app.run(debug=True, host='0.0.0.0', port=5000)