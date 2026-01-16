from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import sqlite3

app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")


# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "sindex.html",
        {"request": request}
    )


# ---------------- ADD FORM ----------------
@app.get("/add", response_class=HTMLResponse)
def add(request: Request):
    return templates.TemplateResponse(
        "sadd.html",
        {"request": request}
    )


# ---------------- SAVE DETAILS ----------------
@app.post("/savedetails", response_class=HTMLResponse)
def savedetails(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    number: str = Form(...),
    college_name: str = Form(...),
    city: str = Form(...),
    state: str = Form(...)
):
    msg = ""

    try:
        con = sqlite3.connect("senroll.db")
        cur = con.cursor()

      
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ens (
                name TEXT,
                email TEXT,
                address TEXT,
                number TEXT,
                college_name TEXT,
                city TEXT,
                state TEXT
            )
        """)

        cur.execute(
            "INSERT INTO ens VALUES (?,?,?,?,?,?,?)",
            (name, email, address, number, college_name, city, state)
        )

        con.commit()
        msg = "Your Details have been Successfully Submitted"

    except Exception:
        msg = "Sorry! Please fill all the details in the form"

    finally:
        con.close()

    return templates.TemplateResponse(
        "ssuccess.html",
        {"request": request, "msg": msg}
    )


# ---------------- VIEW ENROLLED ----------------
@app.get("/view", response_class=HTMLResponse)
def view(request: Request):
    con = sqlite3.connect("senroll.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM ens")
    rows = cur.fetchall()
    con.close()

    return templates.TemplateResponse(
        "sview.html",
        {"request": request, "rows": rows}
    )


# ---------------- JSON DATA ----------------
@app.get("/data")
def data_response():
    con = sqlite3.connect("senroll.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM ens")
    rows = cur.fetchall()
    con.close()

    students = []
    for r in rows:
        students.append({
            "name": r[0],
            "email": r[1],
            "address": r[2],
            "number": r[3],
            "college_name": r[4],
            "city": r[5],
            "state": r[6]
        })

    return JSONResponse(content={"students": students})

