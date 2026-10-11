# 🎓 Electricity Bill Smart — College Viva Preparation Guide (Hinglish)

College viva aur presentation ke liye ye sabse common questions aur simple answers hain:

---

### Q1: Aapka project kis baare me hai? (Project Overview)
**Answer:**
> *"Sir, project ka naam **Electricity Bill Smart** hai. Ye ek machine learning model hai jo household electricity consumption ke historical monthly data ko analyze karke agle mahine ka electricity consumption (kWh / units) predict karta hai, aur user ke tariff rate ke basis par estimated bijli ka bill calculate karta hai."*

---

### Q2: Kaunsa Machine Learning algorithm use kiya hai aur kyu?
**Answer:**
> *"Sir, humne **Linear Regression** use kiya hai. Electricity consumption ek continuous numeric value hai, isliye ye ek **Regression problem** hai. Linear Regression lightweight, simple aur easily interpretable hota hai jisse model ke coefficients aur predictions ko clearly explain kiya ja sakta hai."*

---

### Q3: Seasonality (Mausam ke badlaav) ko model ne kaise handle kiya?
**Answer (Very Important):**
> *"Sir, electricity usage mausam par bohot depend karta hai—jaise garmiyo me AC ki wajah se consumption peak pe hota hai. Is seasonal pattern ko capture karne ke liye humne 2 main techniques use ki hain:*
> 1. **Cyclical Encoding (Sine aur Cosine):** Normal numbers (1 to 12) me computer ko lagta hai December (12) aur January (1) bohot door hain. Humne `sin(2*pi*month/12)` aur `cos(2*pi*month/12)` use kiya jisse calendar ek circle ban jata hai aur Dec & Jan padosi mahine ban jate hain.
> 2. **Lag-12 Feature:** Agle mahine ke prediction ke liye pichhle saal ke usi same mahine ka consumption (same month last year) bhi feature ke roop me diya hai."*

---

### Q4: Train-Test Split kaise kiya? Random shuffle kyu nahi kiya?
**Answer:**
> *"Sir, ye **Time Series (chronological) data** hai. Agar hum random train-test split karte toh data leakage ho jata (future ka data model pehle dekh leta). Isliye humne **chronological split** kiya—shuru ke 75% months training ke liye aur aakhiri ke 25% months testing ke liye use kiye bina shuffle kiye."*

---

### Q5: Model ki evaluation metric kya hai? Accuracy score kyu nahi nikala?
**Answer:**
> *"Sir, classification problems me Accuracy percentage hoti hai, lekin Regression me hum errors measure karte hain. Humne **MAE (Mean Absolute Error)** use kiya hai. Model ka test set par MAE sirf ~1.43 units aaya hai, jabki baseline model (last year same month directly lena) ka error ~11.33 units tha. Iska matlab Linear Regression seasonal trend ko effectively capture kar raha hai."*

---

### Q6: Energy Charges aur Bill kaise calculate hota hai?
**Answer:**
> *"Sir:*
> - **Energy Charge** = Predicted Units × Rate per Unit (₹)
> - **Estimated Bill** = Energy Charge + Fixed Charges
> Humne app me disclaimer bhi diya hai ki ye estimated bill hai, koi official discom bill nahi."*

---

### Q7: 10% Savings feature kya karta hai?
**Answer:**
> *"Sir, ye ek simple simulation feature hai. User ko aware karne ke liye ki agar wo apne usage me 10% reduction kare, toh unke bill me kitne rupaye bachenge."*
