from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()
DATA_FILE = "data.json"

class Announcement(BaseModel):
    id: int
    title: str
    content: str

def load_data() -> List[Announcement]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Announcement(**item) for item in data]

def save_data(data: List[Announcement]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([item.dict() for item in data], f, indent=2, ensure_ascii=False)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return RedirectResponse("/tablica")

@app.get("/announcements", response_model=List[Announcement])
def get_announcements():
    return load_data()

@app.post("/announcements", response_model=Announcement)
def add_announcement(announcement: Announcement):
    data = load_data()
    if any(a.id == announcement.id for a in data):
        raise HTTPException(status_code=400, detail="ID już istnieje")
    data.append(announcement)
    save_data(data)
    return announcement

@app.delete("/announcements/{announcement_id}")
def delete_announcement(announcement_id: int):
    data = load_data()
    data_new = [a for a in data if a.id != announcement_id]
    if len(data) == len(data_new):
        raise HTTPException(status_code=404, detail="Ogłoszenie nie znalezione")
    save_data(data_new)
    return {"message": "Usunięto ogłoszenie"}

@app.put("/announcements/{announcement_id}", response_model=Announcement)
def update_announcement(announcement_id: int, announcement: Announcement):
    data = load_data()
    for idx, a in enumerate(data):
        if a.id == announcement_id:
            data[idx] = announcement
            save_data(data)
            return announcement
    raise HTTPException(status_code=404, detail="Ogłoszenie nie znalezione")

@app.get("/tablica", response_class=HTMLResponse)
async def show_tablica():
    announcements = load_data()
    html_content = """
    <html>
        <head>
            <title>Tablica Ogłoszeń</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .announcement { border: 1px solid #ccc; padding: 10px; margin-bottom: 15px; border-radius: 5px; }
                .announcement h2 { margin: 0 0 5px 0; }
                form { margin-top: 10px; }
                label { display: block; margin-top: 8px; }
                input[type="text"], textarea { width: 100%; padding: 8px; box-sizing: border-box; }
                button { margin-top: 10px; padding: 8px 12px; color: white; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { opacity: 0.9; }
                .btn-add { background-color: #28a745; }
                .btn-edit { background-color: #007bff; }
                .btn-delete { background-color: #dc3545; margin-top: 5px; }
            </style>
        </head>
        <body>
            <h1>Tablica Ogłoszeń</h1>
    """
    for a in announcements:
        html_content += f"""
            <div class="announcement">
                <h2>{a.title} (ID: {a.id})</h2>
                <p>{a.content}</p>
                <form action="/edit" method="post">
                    <input type="hidden" name="id" value="{a.id}">
                    <label>Tytuł:<input type="text" name="title" value="{a.title}" required></label>
                    <label>Treść:<textarea name="content" rows="3" required>{a.content}</textarea></label>
                    <button type="submit" class="btn-edit">Edytuj</button>
                </form>
                <form action="/delete" method="post" onsubmit="return confirm('Na pewno chcesz usunąć to ogłoszenie?');">
                    <input type="hidden" name="id" value="{a.id}">
                    <button type="submit" class="btn-delete">Usuń</button>
                </form>
            </div>
        """
    html_content += """
            <h2>Dodaj nowe ogłoszenie</h2>
            <form action="/add" method="post">
                <label for="id">ID (unikalne, liczba):</label>
                <input type="number" id="id" name="id" required>
                <label for="title">Tytuł:</label>
                <input type="text" id="title" name="title" required>
                <label for="content">Treść:</label>
                <textarea id="content" name="content" rows="4" required></textarea>
                <button type="submit" class="btn-add">Dodaj</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/add")
async def add_announcement_form(id: int = Form(...), title: str = Form(...), content: str = Form(...)):
    data = load_data()
    if any(a.id == id for a in data):
        return HTMLResponse(f"<html><body><h3>Ogłoszenie z ID {id} już istnieje.</h3><a href='/tablica'>Wróć</a></body></html>")
    new_announcement = Announcement(id=id, title=title, content=content)
    data.append(new_announcement)
    save_data(data)
    return RedirectResponse(url="/tablica", status_code=303)

@app.post("/edit")
async def edit_announcement_form(id: int = Form(...), title: str = Form(...), content: str = Form(...)):
    data = load_data()
    for idx, a in enumerate(data):
        if a.id == id:
            data[idx] = Announcement(id=id, title=title, content=content)
            save_data(data)
            return RedirectResponse(url="/tablica", status_code=303)
    return HTMLResponse(f"<html><body><h3>Ogłoszenie z ID {id} nie znalezione.</h3><a href='/tablica'>Wróć</a></body></html>")

@app.post("/delete")
async def delete_announcement_form(id: int = Form(...)):
    data = load_data()
    new_data = [a for a in data if a.id != id]
    if len(new_data) == len(data):
        return HTMLResponse(f"<html><body><h3>Ogłoszenie z ID {id} nie znalezione.</h3><a href='/tablica'>Wróć</a></body></html>")
    save_data(new_data)
    return RedirectResponse(url="/tablica", status_code=303)
