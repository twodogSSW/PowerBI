print("RUNNING FILE:", __file__)
print("PASSWORD SENT TO ODBC:", "@McbNx8w@!9*")


from fastapi import FastAPI
import pyodbc

app = FastAPI()

#MultipleActiveResultSets=False;
#Persist Security Info=False;

# Azure SQL connection
password = "@McbNx8w@!9*"
print("PASSWORD SENT TO ODBC:", password)

conn = pyodbc.connect(
	password = "McbNx8w@!9*"
	"Driver={ODBC Driver 18 for SQL Server};"
	"Server=tcp.steven-edit-sql.database.windows.net,1433;""
	"Database=EditableTextDB;"
	"Uid=apiuser;"
	f"Pwd={Password};"
	"Encrypt=yes";
	"TrustServerCertification=yes";
	"Connection Timeout=30;"
)

print("FULL CONNECTION STRING:", full_conn)

conn = pyodbc.connect(full_conn)

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/editabletext/{category}")
def get_text(category: str):
    cursor = conn.cursor()
    cursor.execute("SELECT DisplayText FROM EditableText WHERE Category = ?", (category,))
    row = cursor.fetchone()
    return {"category": category, "text": row.DisplayText if row else None}

@app.post("/editabletext/{category}")
def update_text(category: str, new_text: str):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE EditableText SET DisplayText = ? WHERE Category = ?",
        (new_text, category)
    )
    conn.commit()
    return {"status": "updated", "category": category, "new_text": new_text}
