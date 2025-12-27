# AgroSmart - AI-Powered Crop Recommendation System

[![Django](https://img.shields.io/badge/Django-3.2.16-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modern, AI-powered agricultural platform that provides intelligent crop recommendations using machine learning. Built with Django, featuring a responsive Bootstrap 5 UI and containerized deployment.

## 🌟 Key Features

### 🤖 AI-Powered Crop Recommendation
- **Random Forest Classifier** trained on 2,200+ agricultural samples
- **99.55% Test Accuracy** with 5-fold cross-validation (99.32% mean)
- **22 Crop Types** supported (rice, maize, jute, cotton, coconut, papaya, etc.)
- **7 Soil Parameters**: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall

### 📊 Advanced Analytics
- **Feature Importance Analysis**: Humidity (21.85%), Rainfall (21.64%) as key factors
- **Comprehensive Model Evaluation**: Precision, Recall, F1-Score metrics
- **Confusion Matrix & Visualization**: Detailed performance analysis
- **Cross-Validation**: Robust model validation with minimal variance

### 🎨 Modern UI/UX
- **Responsive Design**: Bootstrap 5 with custom CSS
- **Gradient Backgrounds**: Beautiful visual design
- **Interactive Elements**: Hover effects and animations
- **Mobile-First**: Optimized for all devices

### 🔧 Technical Features
- **REST API**: JSON-based crop prediction endpoint
- **User Management**: Registration, authentication, profiles
- **Docker Support**: Containerized deployment
- **MySQL Database**: Production-ready data storage

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Docker (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agrosmart.git
   cd agrosmart
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```sql
   CREATE DATABASE agrosmart;
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py create_admin  # Create admin user
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - **Web App**: http://localhost:8000
   - **API Endpoint**: http://localhost:8000/api/predict-crop/
   - **Admin Panel**: http://localhost:8000/admin/

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📈 ML Model Performance

### Accuracy Metrics
- **Test Accuracy**: 99.55%
- **Cross-Validation Mean**: 99.32%
- **Standard Deviation**: ±0.48%

### Feature Importance Ranking
1. **Humidity**: 21.85%
2. **Rainfall**: 21.64%
3. **Potassium**: 18.96%
4. **Phosphorus**: 14.57%
5. **Nitrogen**: 10.44%
6. **Temperature**: 7.43%
7. **pH**: 5.11%

### Supported Crops
Rice, Maize, Jute, Cotton, Coconut, Papaya, Orange, Apple, Muskmelon, Watermelon, Grapes, Mango, Banana, Pomegranate, Lentil, Blackgram, Mungbean, Mothbeans, Pigeonpeas, Kidneybeans, Chickpea, Coffee

## 🔌 API Usage

### Crop Prediction Endpoint

**POST** `/api/predict-crop/`

**Request Body:**
```json
{
  "nitrogen": 90,
  "phosphorus": 42,
  "potassium": 43,
  "temperature": 20.8,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}
```

**Response:**
```json
{
  "prediction": "rice",
  "input_data": {
    "nitrogen": 90,
    "phosphorus": 42,
    "potassium": 43,
    "temperature": 20.8,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 202.9
  },
  "probabilities": {
    "rice": 0.85,
    "maize": 0.12,
    // ... other crops
  }
}
```

## 🏗️ Project Structure

```
agrosmart/
├── app/
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL patterns
│   ├── templates/         # HTML templates
│   │   ├── index.html
│   │   ├── visitor/
│   │   └── admin/
│   └── static/            # CSS, JS, images
├── project2/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py
├── Machine Learning/
│   ├── Crop_recommendation.csv
│   └── [model files]
├── evaluate_model.py      # ML evaluation script
├── train_model.py         # Model training script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
└── README.md
```

## 🧪 Testing the ML Model

```bash
# Run model evaluation
python evaluate_model.py

# This will generate:
# - Performance metrics
# - Confusion matrix plot
# - Feature importance analysis
# - Model comparison charts
```

## 🚀 Deployment

### AWS ECS Deployment

1. **Build ECR Repository**
   ```bash
   aws ecr create-repository --repository-name agrosmart-repo --region us-east-1
   ```

2. **GitHub Actions**
   - Automatic deployment on push to main branch
   - Requires AWS credentials in GitHub secrets

### Environment Variables

```env
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_NAME=agrosmart
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=your-db-host
DATABASE_PORT=3306
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Varshasri R V** - *Initial work and ML implementation*

## 🙏 Acknowledgments

- Dataset source: [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
- UI Framework: Bootstrap 5
- ML Library: scikit-learn
- Icons: Font Awesome

---

**Made with ❤️ for sustainable agriculture**
