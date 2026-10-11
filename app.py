import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Page Configuration
st.set_page_config(
    page_title="BijliSmart - Electricity Bill & Consumption Predictor",
    page_icon="⚡",
    layout="wide"
)

# Clean, professional student CSS styling
st.markdown("""
    <style>
    .main-header {
        font-size: 26px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 14px;
        color: #475569;
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .result-title {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .result-value {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
    }
    .result-sub {
        font-size: 12px;
        color: #64748B;
        margin-top: 4px;
    }
    .note-box {
        background-color: #EFF6FF;
        border-left: 4px solid #2563EB;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 13px;
        color: #1E293B;
        line-height: 1.5;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ BijliSmart – Electricity Bill Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">A smart, beginner-friendly tool to calculate and forecast household electricity consumption and monthly bills.</div>', unsafe_allow_html=True)

# Common Sidebar Settings: Tariffs
st.sidebar.header("⚙️ Electricity Tariff Settings")
rate_per_unit = st.sidebar.number_input("Rate per Unit (₹/kWh)", min_value=1.0, max_value=20.0, value=7.50, step=0.50, help="Average cost per unit of electricity in your city.")
fixed_charges = st.sidebar.number_input("Fixed Monthly Charges (₹)", min_value=0.0, max_value=1000.0, value=100.0, step=10.0, help="Meter rent or fixed connection fee.")
simulate_savings = st.sidebar.checkbox("Simulate 10% Energy Savings", value=False)

# Navigation Tabs
tab1, tab2 = st.tabs(["🏠 Household Appliance Calculator", "📈 Historical Data Forecast (ML Model)"])

# ==============================================================================
# TAB 1: HOUSEHOLD APPLIANCE CALCULATOR
# ==============================================================================
with tab1:
    st.subheader("Estimate Bill from Household Appliances")
    st.write("Enter the number of appliances and their daily usage to calculate your estimated monthly bill.")

    col_app1, col_app2, col_app3 = st.columns(3)

    with col_app1:
        st.markdown("##### ❄️ Cooling & Heating")
        num_ac = st.number_input("Air Conditioners (1.5 Ton)", min_value=0, max_value=10, value=1, step=1)
        ac_hours = st.slider("AC Usage (Hours/Day)", min_value=0, max_value=24, value=6 if num_ac > 0 else 0)
        
        num_cooler = st.number_input("Air Coolers", min_value=0, max_value=5, value=0, step=1)
        cooler_hours = st.slider("Cooler Usage (Hours/Day)", min_value=0, max_value=24, value=8 if num_cooler > 0 else 0)

        num_geyser = st.number_input("Geysers / Water Heaters", min_value=0, max_value=5, value=1, step=1)
        geyser_hours = st.slider("Geyser Usage (Hours/Day)", min_value=0.0, max_value=6.0, value=1.0 if num_geyser > 0 else 0.0, step=0.5)

    with col_app2:
        st.markdown("##### 🌀 Daily Basic Appliances")
        num_fans = st.number_input("Ceiling Fans", min_value=0, max_value=15, value=4, step=1)
        fan_hours = st.slider("Fans Usage (Hours/Day)", min_value=0, max_value=24, value=14)

        num_fridge = st.selectbox("Refrigerator", ["None", "1 Refrigerator (Standard)", "2 Refrigerators"], index=1)
        fridge_count = 0 if num_fridge == "None" else (1 if "1" in num_fridge else 2)

        num_tv = st.number_input("Television (TV)", min_value=0, max_value=5, value=1, step=1)
        tv_hours = st.slider("TV Usage (Hours/Day)", min_value=0, max_value=24, value=4 if num_tv > 0 else 0)

    with col_app3:
        st.markdown("##### 📅 Month & Lighting")
        selected_month = st.selectbox("Select Current Month", [
            "January (Winter)", "February", "March", "April", 
            "May (Peak Summer)", "June (Peak Summer)", "July (Monsoon)", 
            "August", "September", "October", "November", "December (Winter)"
        ], index=4)

        num_rooms = st.number_input("Number of Rooms (Lights & Other load)", min_value=1, max_value=10, value=3, step=1)
        washing_machine_weekly = st.slider("Washing Machine (Uses/Week)", min_value=0, max_value=14, value=4)
        
        has_pump = st.checkbox("Water Motor / Pump (1 HP)", value=True)
        pump_mins = st.slider("Water Motor Run Time (Minutes/Day)", min_value=0, max_value=180, value=45 if has_pump else 0, step=15)

    # Calculation Logic (Standard Indian Wattage Ratings)
    # AC: ~1.4 kWh per hour
    # Cooler: ~0.2 kWh per hour
    # Geyser: ~2.0 kWh per hour
    # Fan: ~0.075 kWh per hour
    # Fridge: ~1.6 kWh per day (24 hrs)
    # TV: ~0.10 kWh per hour
    # Water Pump (1 HP): ~0.75 kWh per hour
    # Lights & Misc per room: ~0.6 kWh per day
    # Washing machine: ~0.5 kWh per wash
    
    # Seasonal adjustments
    is_summer = any(m in selected_month for m in ["April", "May", "June", "July"])
    is_winter = any(m in selected_month for m in ["November", "December", "January"])
    
    daily_ac_kwh = num_ac * ac_hours * 1.4
    daily_cooler_kwh = num_cooler * cooler_hours * 0.2
    # In winter geysers run at full power, in summer usually turned off
    geyser_factor = 0.2 if is_summer else (1.2 if is_winter else 0.8)
    daily_geyser_kwh = num_geyser * geyser_hours * 2.0 * geyser_factor
    daily_fan_kwh = num_fans * fan_hours * 0.075
    daily_fridge_kwh = fridge_count * 1.6
    daily_tv_kwh = num_tv * tv_hours * 0.10
    daily_pump_kwh = (pump_mins / 60.0) * 0.75 if has_pump else 0.0
    daily_lights_misc = num_rooms * 0.65
    daily_washing_kwh = (washing_machine_weekly * 0.5) / 7.0

    total_daily_units = (daily_ac_kwh + daily_cooler_kwh + daily_geyser_kwh + 
                          daily_fan_kwh + daily_fridge_kwh + daily_tv_kwh + 
                          daily_pump_kwh + daily_lights_misc + daily_washing_kwh)
    
    total_monthly_units = round(total_daily_units * 30, 1)
    monthly_energy_charge = round(total_monthly_units * rate_per_unit, 2)
    total_appliance_bill = round(monthly_energy_charge + fixed_charges, 2)

    st.markdown("---")
    st.markdown("#### 📊 Bill Summary")

    res_c1, res_c2, res_c3 = st.columns(3)
    with res_c1:
        st.markdown(f"""
            <div class="result-card">
                <div class="result-title">Estimated Monthly Units</div>
                <div class="result-value">{total_monthly_units} kWh</div>
                <div class="result-sub">Approx. {round(total_daily_units, 1)} units/day</div>
            </div>
        """, unsafe_allow_html=True)
    with res_c2:
        st.markdown(f"""
            <div class="result-card">
                <div class="result-title">Energy Charge</div>
                <div class="result-value">₹{monthly_energy_charge:,.2f}</div>
                <div class="result-sub">@ ₹{rate_per_unit:.2f} per unit</div>
            </div>
        """, unsafe_allow_html=True)
    with res_c3:
        st.markdown(f"""
            <div class="result-card">
                <div class="result-title">Estimated Total Bill</div>
                <div class="result-value" style="color:#2563EB;">₹{total_appliance_bill:,.2f}</div>
                <div class="result-sub">Includes ₹{fixed_charges:.0f} fixed charges</div>
            </div>
        """, unsafe_allow_html=True)

    if simulate_savings:
        saved_units = round(total_monthly_units * 0.10, 1)
        new_units = round(total_monthly_units * 0.90, 1)
        savings_rs = round(saved_units * rate_per_unit, 2)
        new_bill = round((new_units * rate_per_unit) + fixed_charges, 2)
        st.success(f"💡 **10% Energy Savings Impact:** By cutting down 1-2 hours of AC or fan usage, consumption drops to **{new_units} kWh**, saving you **₹{savings_rs:,.2f}** per month (New Bill: **₹{new_bill:,.2f}**).")

    # Appliance Breakdown Graph
    st.markdown("##### 📌 Appliance Consumption Breakdown (kWh/Month)")
    breakdown_data = {
        'AC': daily_ac_kwh * 30,
        'Cooler': daily_cooler_kwh * 30,
        'Geyser': daily_geyser_kwh * 30,
        'Fans': daily_fan_kwh * 30,
        'Refrigerator': daily_fridge_kwh * 30,
        'Water Pump': daily_pump_kwh * 30,
        'TV': daily_tv_kwh * 30,
        'Lights & Misc': (daily_lights_misc + daily_washing_kwh) * 30
    }
    breakdown_filtered = {k: round(v, 1) for k, v in breakdown_data.items() if v > 0.5}

    if breakdown_filtered:
        fig_bar, ax_bar = plt.subplots(figsize=(9, 3.2))
        bars = ax_bar.bar(breakdown_filtered.keys(), breakdown_filtered.values(), color='#3B82F6', width=0.5)
        ax_bar.set_ylabel("Units Consumed (kWh)", fontsize=10)
        ax_bar.grid(axis='y', linestyle=':', alpha=0.7)
        for bar in bars:
            height = bar.get_height()
            ax_bar.annotate(f'{height}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig_bar)

    st.markdown("""
        <div class="note-box">
            <strong>Appliance Usage Insights:</strong><br>
            Calculations are based on standard wattage benchmarks of Indian household appliances. In summer, AC cooling accounts for the largest proportion of the bill, while in winter, water heating (geyser) dominates.
        </div>
    """, unsafe_allow_html=True)

    # ----------------- BILL REDUCTION RECOMMENDATIONS -----------------
    st.markdown("---")
    st.markdown("#### 💡 How to Reduce Your Monthly Electricity Bill")
    st.write("Actionable energy-saving habits and technology upgrades to cut down your monthly units:")

    tip_col1, tip_col2 = st.columns(2)

    with tip_col1:
        st.markdown("""
            * **❄️ Set AC Temperature to 24°C - 26°C:**
              According to BEE (Bureau of Energy Efficiency), increasing AC temperature from 18°C/20°C to 24°C saves **~6% electricity per degree** (up to **₹400 – ₹700 savings/month**).
            * **🌀 Switch to BLDC Ceiling Fans:**
              Traditional ceiling fans consume ~75 Watts, while 5-star BLDC fans consume only 28–32 Watts. Upgrading 3–4 fans can save **35–50 units per month**.
            * **🚰 Install Auto-Cut Switch for Water Motor:**
              Prevent water tank overflows and dry runs. Running a 1 HP pump for just 30 minutes instead of 60 minutes saves **~15 units/month**.
        """)

    with tip_col2:
        st.markdown("""
            * **♨️ Use Geyser with a Timer / Turn Off Promptly:**
              Heating water for 15–20 minutes before bathing rather than leaving the geyser on for hours prevents thermostat cycling losses (**saves 20–30 units/month**).
            * **🔌 Eliminate Phantom / Standby Power:**
              Appliances like TVs, set-top boxes, and microwave displays consume 5–10% idle power on standby. Switch them off directly at the main wall socket.
            * **💡 100% LED Lighting & Clean Filters:**
              Dusty AC and cooler air filters force motors to work 15% harder. Regular filter cleaning immediately lowers unit consumption.
        """)


# ==============================================================================
# TAB 2: HISTORICAL DATA FORECAST (TIME-SERIES ML MODEL)
# ==============================================================================
with tab2:
    st.subheader("Historical Time-Series Forecasting")
    st.write("Trains a Linear Regression model with Cyclical Month Encoding (Sine/Cosine) on historical monthly data.")

    c_source, c_blank = st.columns([2, 1])
    with c_source:
        data_source = st.radio(
            "Select Data Source:",
            ("Use Built-in Dataset (48 Consecutive Months)", "Upload Custom CSV"),
            horizontal=True
        )

    # Provide a simple CSV download template for users
    sample_template = "Year,Month,Units_Consumed\n2023,1,185\n2023,2,205\n2023,3,255\n2023,4,340\n2023,5,460\n2023,6,495\n2023,7,450\n2023,8,365\n2023,9,320\n2023,10,260\n2023,11,198\n2023,12,175\n2024,1,192\n2024,2,210"
    st.download_button(
        label="📥 Download CSV Template / Format",
        data=sample_template,
        file_name="electricity_template.csv",
        mime="text/csv",
        help="Download this template, open in Excel, add your own monthly data, and upload below."
    )

    df_ml = None
    if data_source == "Use Built-in Dataset (48 Consecutive Months)":
        try:
            df_ml = pd.read_csv("data/electricity_data.csv")
        except Exception as e:
            st.error(f"Error loading data: {e}")
    else:
        uploaded_file = st.file_uploader("Upload CSV (must contain Year, Month, Units_Consumed)", type=["csv"])
        if uploaded_file is not None:
            try:
                df_ml = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error reading file: {e}")

    if df_ml is not None:
        required_cols = {'Year', 'Month', 'Units_Consumed'}
        if not required_cols.issubset(set(df_ml.columns)):
            st.error("Uploaded CSV must have 'Year', 'Month', and 'Units_Consumed' columns.")
        elif len(df_ml) < 13:
            st.warning("⚠️ Insufficient historical data: Model requires at least 13 months to learn previous month (Lag 1) and same month last year (Lag 12) patterns.")
        else:
            # Cyclical and Lag feature engineering
            df_feat = df_ml.copy()
            df_feat['month_sin'] = np.sin(2 * np.pi * df_feat['Month'] / 12)
            df_feat['month_cos'] = np.cos(2 * np.pi * df_feat['Month'] / 12)
            df_feat['lag_1'] = df_feat['Units_Consumed'].shift(1)
            df_feat['lag_12'] = df_feat['Units_Consumed'].shift(12)
            
            clean_train = df_feat.dropna().reset_index(drop=True)
            feature_cols = ['month_sin', 'month_cos', 'lag_1', 'lag_12']
            X_all = clean_train[feature_cols]
            y_all = clean_train['Units_Consumed']

            # Chronological Evaluation Split (75% train, 25% test)
            split_idx = max(1, int(len(clean_train) * 0.75))
            X_train, X_test = X_all.iloc[:split_idx], X_all.iloc[split_idx:]
            y_train, y_test = y_all.iloc[:split_idx], y_all.iloc[split_idx:]

            from sklearn.metrics import mean_absolute_error, r2_score
            eval_model = LinearRegression()
            eval_model.fit(X_train, y_train)
            
            if len(X_test) > 0:
                y_pred_test = eval_model.predict(X_test)
                model_mae = mean_absolute_error(y_test, y_pred_test)
                model_r2 = r2_score(y_test, y_pred_test)
                baseline_pred = X_test['lag_12']
                baseline_mae = mean_absolute_error(y_test, baseline_pred)
            else:
                model_mae = 0.0
                model_r2 = 1.0
                baseline_mae = 0.0

            # Fit Final Model on all available data for future forecast
            lr_model = LinearRegression()
            lr_model.fit(X_all, y_all)

            # Predict Next Month
            last_record = df_ml.iloc[-1]
            last_year = int(last_record['Year'])
            last_month = int(last_record['Month'])

            if last_month == 12:
                next_month = 1
                next_year = last_year + 1
            else:
                next_month = last_month + 1
                next_year = last_year

            next_sin = np.sin(2 * np.pi * next_month / 12)
            next_cos = np.cos(2 * np.pi * next_month / 12)
            next_lag1 = float(last_record['Units_Consumed'])

            match_prev_year = df_ml[(df_ml['Year'] == next_year - 1) & (df_ml['Month'] == next_month)]
            if not match_prev_year.empty:
                next_lag12 = float(match_prev_year.iloc[0]['Units_Consumed'])
            else:
                next_lag12 = float(df_ml.iloc[-12]['Units_Consumed'])

            next_features = pd.DataFrame([{
                'month_sin': next_sin,
                'month_cos': next_cos,
                'lag_1': next_lag1,
                'lag_12': next_lag12
            }])

            predicted_ml_units = max(0.0, round(float(lr_model.predict(next_features)[0]), 1))
            ml_energy_charge = round(predicted_ml_units * rate_per_unit, 2)
            ml_total_bill = round(ml_energy_charge + fixed_charges, 2)

            month_names = ["January", "February", "March", "April", "May", "June", 
                           "July", "August", "September", "October", "November", "December"]
            target_name = month_names[next_month - 1]

            st.markdown(f"#### 🔮 Forecast for {target_name} {next_year}")
            
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">Forecasted Consumption</div>
                        <div class="result-value">{predicted_ml_units} kWh</div>
                        <div class="result-sub">Next Month Estimate</div>
                    </div>
                """, unsafe_allow_html=True)
            with mc2:
                st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">Energy Charge</div>
                        <div class="result-value">₹{ml_energy_charge:,.2f}</div>
                        <div class="result-sub">@ ₹{rate_per_unit:.2f}/unit</div>
                    </div>
                """, unsafe_allow_html=True)
            with mc3:
                st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">Estimated Total Bill</div>
                        <div class="result-value" style="color:#2563EB;">₹{ml_total_bill:,.2f}</div>
                        <div class="result-sub">Includes ₹{fixed_charges:.0f} Fixed Fee</div>
                    </div>
                """, unsafe_allow_html=True)

            # Evaluation Metrics Display
            st.markdown("##### 🎯 Model Accuracy & Evaluation Metrics")
            em1, em2, em3 = st.columns(3)
            with em1:
                st.metric("Model Error (MAE)", f"{model_mae:.2f} Units", help="Mean Absolute Error on test set. Lower is better.")
            with em2:
                st.metric("Baseline Error (Last Year MAE)", f"{baseline_mae:.2f} Units", help="Error if we simply used last year's same month units.")
            with em3:
                st.metric("R² Score (Goodness of Fit)", f"{model_r2:.4f}", help="Indicates how well the regression line fits the data (1.0 is ideal).")

            # Historical Chart
            st.markdown("##### 📈 Historical Trend & Next-Month Forecast")
            plot_history = df_ml.tail(24).copy().reset_index(drop=True)
            hist_labels = [f"{month_names[int(r['Month'])-1][:3]} '{str(int(r['Year']))[-2:]}" for _, r in plot_history.iterrows()]
            hist_values = list(plot_history['Units_Consumed'])
            
            forecast_label = f"{target_name[:3]} '{str(next_year)[-2:]} (Pred)"
            all_chart_labels = hist_labels + [forecast_label]

            fig_ts, ax_ts = plt.subplots(figsize=(10, 4.2))
            ax_ts.plot(range(len(hist_values)), hist_values, marker='o', color='#2563EB', linewidth=2, label="Actual Past Consumption")
            ax_ts.scatter([len(hist_values)], [predicted_ml_units], color='#DC2626', s=80, zorder=5, label=f"Predicted ({predicted_ml_units} kWh)")
            ax_ts.plot([len(hist_values)-1, len(hist_values)], [hist_values[-1], predicted_ml_units], color='#DC2626', linestyle='--', linewidth=2)

            ax_ts.set_xticks(range(len(all_chart_labels)))
            ax_ts.set_xticklabels(all_chart_labels, rotation=45, ha='right', fontsize=9)
            ax_ts.set_ylabel("Units Consumed (kWh)", fontsize=10)
            ax_ts.grid(True, linestyle=':', alpha=0.6)
            ax_ts.legend(loc="upper left")
            plt.tight_layout()
            st.pyplot(fig_ts)

            st.markdown("""
                <div class="note-box">
                    <strong>How the Forecast Model Works:</strong><br>
                    • <strong>Cyclical Encoding:</strong> Converts calendar months into Sine and Cosine coordinates so December and January are treated as adjacent seasons.<br>
                    • <strong>Lag Features:</strong> Analyzes previous month's usage (Lag 1) and same month last year (Lag 12) to capture annual seasonality patterns.<br>
                    • <strong>Algorithm:</strong> Linear Regression. Ensures high interpretability and transparent estimations based directly on historical data.
                </div>
            """, unsafe_allow_html=True)

            with st.expander("📄 View Last 12 Months Data"):
                st.dataframe(df_ml.tail(12).reset_index(drop=True), use_container_width=True)
