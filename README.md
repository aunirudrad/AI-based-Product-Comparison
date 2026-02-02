# 📊 AI Market Price Predictor

An intelligent product pricing analysis application powered by Google's Gemini AI and Python. This tool helps users predict the current market value of their used products based on condition, usage, and market trends.

## 🎯 Project Overview

AI Market Price Predictor is a Flask-based web application that combines traditional depreciation algorithms with AI-powered market insights to provide accurate price predictions for various consumer electronics and gadgets. The application analyzes product condition, usage duration, warranty status, and market trends to calculate fair market values.

## 🚀 Features

### Core Features
- **AI-Powered Price Analysis** - Leverages Google Gemini 2.0 Flash for intelligent market insights
- **Real-time Price Prediction** - Instant calculation based on product attributes
- **Multi-Product Support** - Supports iPhones, MacBooks, laptops, tablets, cameras, smartwatches, headphones, and gaming consoles
- **Condition-Based Pricing** - Adjusts prices based on product condition (New, Like New, Good, Fair, Poor)
- **Depreciation Tracking** - Calculates monthly depreciation and total value loss
- **Market Comparison** - Provides price ranges for online, retail, and wholesale channels

### Advanced Capabilities
- **Warranty Value Assessment** - Factors in remaining warranty for accurate pricing
- **Market Insights** - AI-generated recommendations and selling tips
- **Platform Suggestions** - Recommends best platforms to sell for optimal price
- **Interactive Chat Interface** - User-friendly conversational interface
- **RESTful API** - Backend API for programmatic access

### Analytics & Reporting
- Estimated market price with confidence levels
- Price loss analysis (amount and percentage)
- Monthly depreciation rate
- Market comparison across different selling channels
- Selling recommendations based on retained value

## 🛠️ Technologies Used

### Backend
- **Python 3.x** - Core programming language
- **Flask 2.3.3** - Web application framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **Google Generative AI 0.3.0** - Gemini API integration
- **python-dotenv 1.0.0** - Environment variable management
- **Werkzeug 2.3.7** - WSGI utilities

### Frontend
- **HTML5** - Structure and markup
- **CSS3** - Styling and responsive design
- **JavaScript (Vanilla)** - Client-side interactivity
- **Responsive Design** - Mobile-friendly interface

### AI/ML
- **Google Gemini 2.0 Flash** - Advanced language model for market analysis
- **Custom Depreciation Algorithm** - Product-specific value calculation

## 📋 Prerequisites

- Python 3.7 or higher
- Google Gemini API key
- Modern web browser

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-based-Product-Comparison
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5000`

## 🎮 Usage

### Web Interface

1. Open the application in your browser
2. Fill in the product details:
   - **Product Name**: e.g., iPhone 13, MacBook Pro
   - **Condition**: Select from New, Like New, Good, Fair, or Poor
   - **Usage Months**: Number of months the product has been used
   - **Warranty**: Whether the product still has warranty (Yes/No)
   - **Original Price**: The original purchase price in dollars

3. Click "Analyze Price" to get:
   - Estimated market price
   - Price comparison across channels
   - Depreciation analysis
   - AI-powered market insights
   - Selling recommendations

### API Endpoints

#### Predict Price
```http
POST /api/predict
Content-Type: application/json

{
  "productName": "iPhone 13",
  "condition": "Good",
  "usageMonths": 12,
  "warranty": "Yes",
  "originalPrice": 799.99
}
```

#### Get Supported Products
```http
GET /api/products
```

#### Health Check
```http
GET /api/health
```

## 📊 Supported Products

- **Smartphones**: iPhone 14, iPhone 13, iPhone 12, iPhone SE
- **Laptops**: MacBook Pro, MacBook Air, Dell, HP, Lenovo, ASUS
- **Tablets**: iPad, iPad Pro, Samsung Tab
- **Cameras**: DSLR, Mirrorless, Action Camera
- **Smartwatches**: Apple Watch, Samsung Watch, Fitbit
- **Headphones**: AirPods, Sony, Bose, JBL
- **Gaming**: PlayStation, Xbox, Nintendo

## 🔧 Configuration

### Depreciation Rates
Product-specific depreciation rates can be customized in `app.py`:
- iPhone: 15% annual base depreciation
- MacBook: 12% annual base depreciation
- Laptop: 15% annual base depreciation
- Camera: 10% annual base depreciation
- Gaming: 16% annual base depreciation

### Condition Multipliers
- New: 95%
- Like New: 85%
- Good: 70%
- Fair: 50%
- Poor: 30%

## 📁 Project Structure

```
AI-based-Product-Comparison/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── static/
│   ├── script.js         # Frontend JavaScript
│   └── style.css         # Application styles
└── templates/
    └── index.html        # Main HTML template
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent market analysis
- Flask community for the excellent web framework
- All contributors and users of this project

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Note**: This tool provides estimates based on algorithmic calculations and AI analysis. Actual market prices may vary based on local conditions, demand, and other factors.
