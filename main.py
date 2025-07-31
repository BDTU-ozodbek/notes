from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Note
from schemas import NoteCreate, NoteOut
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Flutter uchun CORS ruxsat beramiz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/notes", response_model=list[NoteOut])
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()

@app.post("/notes", response_model=NoteOut)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    existing_note = db.query(Note).filter(Note.id == note_id).first()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    existing_note.title = note.title
    existing_note.content = note.content
    db.commit()
    db.refresh(existing_note)
    return existing_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
