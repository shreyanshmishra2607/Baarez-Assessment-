# AI Agent Brain – FastAPI Backend (Baarez Assessment)

This project implements the "brain" of a simple AI agent as described in the Baarez Assessment. The system is a Python FastAPI backend that receives a user prompt, analyzes its intent, and routes the request to one of two internal tools: a Calculator or a Memory Store.

The goal of the project is to demonstrate:

* Clean FastAPI service design
* Database interaction (SQLite as allowed for POC)
* Rule-based agent reasoning and routing
* Safe logic execution

---

## 🎯 Objective (As Per Assessment)

Build a single FastAPI application that:

• Accepts a user prompt
• Determines intent using rule-based logic
• Routes the prompt to the correct internal tool
• Returns a unified JSON response

Tools required:

1. Memory Tool (Database CRUD)
2. Calculator Tool (Expression parsing & computation)

---

## 🚀 Core Technologies Used

* Python 3.12
* FastAPI – RESTful API framework
* SQLite – Database (explicitly allowed by assessment for quick POC)
* SQLAlchemy – ORM for DB operations
* Pydantic – Request/response validation
* Pytest – Automated testing

---

## 📁 Project Structure

APP/
├
├── agent/
│   ├── router.py
│   └── schemas.py
├── db/
│   └── database.py
├── tests/
│   └── test_agent.py
├── tools/
│   ├── calculator.py
│   └── memory.py
├── venv/
├── __init__.py
├── .gitignore
├── main.py
├── memory.db
├── memory.sql
├── README.md
└── requirements.txt

---

## 🧠 Tool 1: Memory Tool (Database CRUD)

### Database Design

A simple table named `memory` is used:

* id (primary key)
* key (unique)
* value

The schema is provided in `memory.sql` and the table is also auto-created on application startup using SQLAlchemy.

### Functions Implemented

• tool_save_memory(key: str, value: str)

* Saves a new key-value pair
* Updates the value if the key already exists

• tool_get_memory(key: str)

* Retrieves the stored value for a given key

---

## 🧮 Tool 2: Calculator Tool (Logic & Parsing)

### Function Implemented

• tool_calculate(expression: str)

### Approach

* Converts natural language math expressions into standard operators
* Uses Python AST parsing to safely evaluate expressions
* Avoids using eval() to prevent security risks
* Supports nested and complex expressions

Example:

"5 times (10 plus 2)" → 5 * (10 + 2)

---

## 🤖 Agent Brain – Intent Routing Logic

### Endpoint

POST /agent/query

### Request Format

{
"prompt": "What is 10 plus 5?"
}

---

### Rule-Based Intent Detection (As Required)

| Condition in Prompt    | Routed Tool      |
| ---------------------- | ---------------- |
| "what is", "calculate" | Calculator Tool  |
| "remember", "save"     | Memory Save Tool |
| "recall", "what is my" | Memory Read Tool |

---

### Entity Extraction Logic

The router parses user prompts to extract required values:

Examples:

• "What is 10 plus 5?" → "10 + 5"
• "Remember my cat's name is Fluffy" → key = "cat's name", value = "Fluffy"
• "What is my cat's name?" → key = "cat's name"

---

### Unified Response Format

{
"original_prompt": "...",
"chosen_tool": "...",
"tool_input": "...",
"response": {...}
}

---

## ❗ Error Handling

If the prompt does not match any tool:

{
"error": "I do not have a tool for that."
}

---

## ⚡ Smarter Enhancements (Beyond Basic Requirements)

To make the agent more robust while keeping it simple and rule-based, the following intelligent improvements were added:

### 1. Synonym Normalization

Allows flexible phrasing by mapping related terms:

Example:

* hometown → place, city

This ensures natural language variations still retrieve the correct memory.

---

### 2. Fuzzy Matching

Handles small typos in user input:

Example:

* "hometwon" → "hometown"

Improves usability without using AI models.

---

### 3. Safe Calculator Execution

* Uses AST parsing instead of eval
* Prevents execution of malicious code

---

### 4. Automated Stress & Edge Testing

Comprehensive pytest suite covering:

* Nested and large calculations
* Multiple memory saves
* Overwrites
* Synonym queries
* Typo handling
* Invalid inputs
* Unknown prompts

---

## ▶️ How to Run the Application

1. Install dependencies

pip install -r requirements.txt

2. Start the FastAPI server

uvicorn app.main:app --reload

3. Open API docs

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 How to Run Tests

python -m pytest -v


---

## ✅ Final Summary

This project fully implements all requirements of the Baarez Assessment:

✔ FastAPI backend service
✔ Memory CRUD tool with database
✔ Calculator tool with safe parsing
✔ Rule-based agent routing
✔ Entity extraction logic
✔ Unified response format
✔ Error handling
✔ SQL schema file included
✔ SQLite usage as allowed for POC

Additionally, smarter enhancements were included for robustness such as normalization, fuzzy matching, safe execution, and automated stress testing.

The solution remains simple, clean, and aligned with real backend engineering practices.
