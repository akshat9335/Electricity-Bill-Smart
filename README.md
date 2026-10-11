# Electricity Bill Smart – Bill Predictor

A beginner-friendly Machine Learning project for predicting next month's household electricity consumption (in kWh) and estimating the monthly electricity bill using historical monthly data.

## 📌 Features
- **Cyclical Seasonal Modeling:** Encodes months using Sine and Cosine transformations so that December (month 12) and January (month 1) are treated as adjacent points on the calendar cycle.
- **Lag Features:** Incorporates previous month consumption (Lag 1) and same month last year consumption (Lag 12).
- **Linear Regression Model:** Simple, explainable ML algorithm without black-box complexity.
- **Bill Estimation:** Calculates estimated bill using user-defined unit tariff rate (₹/unit) and optional fixed charges.
- **Savings Simulator:** Interactive 10% energy reduction simulator displaying cost savings.
- **Clean Student UI:** Minimalist Streamlit interface with simple Matplotlib trend graph.

---

## 🛠️ Project Structure
```
summerTraining/
│
├── data/
│   └── electricity_data.csv    # 48 months of synthetic historical electricity data
├── app.py                      # Streamlit web application
├── train_model.py              # Standalone training and evaluation script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🚀 How to Run the Project

### 1. Install Dependencies
Open your terminal / command prompt in this project folder and run:
```bash
pip install -r requirements.txt
```

### 2. (Optional) Run the Training Script
To evaluate the model's Mean Absolute Error (MAE) and view baseline comparison:
```bash
python train_model.py
```

### 3. Launch the Web Application
Start the Streamlit interface:
```bash
streamlit run app.py
```
After running this command, your browser will automatically open the app at `http://localhost:8501`.
