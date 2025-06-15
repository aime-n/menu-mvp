# 🧠 Menu AI

Menu AI is an intelligent assistant that helps you eat better by transforming your nutrition plan or fridge contents into recipes, meal plans, grocery lists, and calorie/cost estimations.

This is the **MVP version**, focused on PDF parsing, recipe generation, and grocery planning — built using **LangGraph**, **FastAPI**, and **Streamlit**.

---

## 🚀 MVP Features

- 📄 Upload a nutritionist PDF and extract meals
- 🍲 Generate recipes from meals or ingredients
- 🗓 Select recipes for the week
- 🛒 Generate a grocery list
- 🔢 Estimate calories and price per recipe

---

## 🧰 Tech Stack

| Layer        | Tech               |
|--------------|--------------------|
| Backend API  | FastAPI            |
| AI Orchestration | LangGraph        |
| Frontend     | Streamlit (MVP)    |
| Language     | Python 3.10+       |

---

## 📦 Setup Instructions

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit app
cd src/app
streamlit run app.py

# 4. Run FastAPI backend (in a separate terminal)
cd src/api
uvicorn main:app --reload
```


⸻

📝 TODO (Initial Milestone)
	•	Create FastAPI and Streamlit boilerplate
	•	Integrate LangGraph with FastAPI
	•	Parse and normalize uploaded PDFs
	•	Generate recipes from meals
	•	Build weekly planner and grocery list

⸻

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

⸻

📄 License

This project is licensed under the MIT License.

---

Let me know if you want a Portuguese version too, or to include badges (build passing, license, etc).