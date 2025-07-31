from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
from models import Note
from schemas import NoteCreate, NoteOut

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/notes", response_model=list[NoteOut])
def read_notes():
    db = SessionLocal()
    notes = db.query(Note).all()
    db.close()
    return notes

@app.post("/notes", response_model=NoteOut)
def create_note(note: NoteCreate):
    db = SessionLocal()
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    db.close()
    return db_note

@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note: NoteCreate):
    db = SessionLocal()
    db_note = db.query(Note).get(note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    db.close()
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    db = SessionLocal()
    db_note = db.query(Note).get(note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(db_note)
    db.commit()
    db.close()
    return {"detail": "Deleted"}
