from database import SesseionLocal

def get_db():
    db=SesseionLocal()
    try:
        yield db
    finally:
        db.close()
