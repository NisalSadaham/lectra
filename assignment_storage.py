import sqlite3
import json
from datetime import datetime, timezone

def initialize_database():
   lectra_database = sqlite3.connect('lectra.db')
   cursor = lectra_database.cursor()
   with lectra_database:
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS assignments(" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "description TEXT NOT NULL," \
    "requirements TEXT NOT NULL," \
    "min_word_count INTEGER," \
    "max_word_count INTEGER," \
    "deadline TEXT," \
    "ai_explanation TEXT)"
      
   )
   cursor.execute(
    "CREATE TABLE IF NOT EXISTS transcript_imports(" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "transcript_hash TEXT NOT NULL," \
    "created_at TEXT NOT NULL)"   
   )
   cursor.execute("PRAGMA table_info(assignments)")
   rows = cursor.fetchall()
   column_names = [row[1] for row in rows]
   if 'import_id' not in column_names:
    cursor.execute(
        "ALTER TABLE assignments ADD COLUMN import_id INTEGER"
    )

   lectra_database.close()

def save_assignment(assignment,import_id = None):
        description = assignment.description
        requirements = json.dumps(assignment.requirements)
        min_word_count=assignment.min_word_count
        max_word_count = assignment.max_word_count
        deadline = assignment.deadline
        lectra_database = sqlite3.connect('lectra.db')
        cursor = lectra_database.cursor()
        with lectra_database:
            cursor.execute(
              "INSERT INTO assignments(description,requirements,min_word_count,max_word_count,deadline,import_id)VALUES(?,?,?,?,?,?)",(description,requirements,min_word_count,max_word_count,deadline,import_id)
            )
        lectra_database.close()
        
def get_assignment():
    lectra_database = sqlite3.connect('lectra.db')
    cursor = lectra_database.cursor()
    cursor.execute(
         "SELECT * FROM assignments"
    )
    rows = cursor.fetchall()
    assignments = [{"id":row[0],"description":row[1],"requirements":json.loads(row[2]),"min_word_count":row[3],"max_word_count":row[4],"deadline":row[5],"ai_explanation":json.loads(row[6]) if row[6] is not None else None} for row in rows]
    lectra_database.close()
    return assignments
def get_assignments_by_import_id(import_id):
    lectra_database = sqlite3.connect('lectra.db')
    cursor = lectra_database.cursor()
    cursor.execute(
        "SELECT * FROM assignments WHERE import_id = ?",(import_id,)
    )
    rows = cursor.fetchall()
    assignments = [{"id":row[0],"description":row[1],"requirements":json.loads(row[2]),"min_word_count":row[3],"max_word_count":row[4],"deadline":row[5],"ai_explanation":json.loads(row[6]) if row[6] is not None else None} for row in rows]
    lectra_database.close()
    return assignments




def save_explanation(assignment_id,explanation):
    lectra_database = sqlite3.connect('lectra.db')
    explanation_data = explanation.model_dump()
    explanation_json = json.dumps(explanation_data)
    cursor = lectra_database.cursor()
    with lectra_database:
        cursor.execute(
            "UPDATE assignments " \
            "SET ai_explanation = ? " \
            "WHERE id = ?",(explanation_json,assignment_id)  
    )
    lectra_database.close()
     
def assigment_exists(description):
    assignments = get_assignment()
    new_description = description.strip().lower()
    for assignment in assignments:
        cleaned_description = assignment['description'].strip().lower()
        if cleaned_description == new_description:
            return True
    return False

def find_transcript_import(transcript_hash):
    lectra_database = sqlite3.connect('lectra.db')
    cursor = lectra_database.cursor()
    cursor.execute(
        "SELECT id,transcript_hash FROM transcript_imports WHERE transcript_hash = ? ORDER BY id DESC",(transcript_hash,)
    )
    row = cursor.fetchone()
    lectra_database.close()
    if(row):
        return row
    return None
def save_transcript_import(transcript_hash):
    time_stamp = datetime.now(timezone.utc).isoformat()
    lectra_database = sqlite3.connect('lectra.db')
    cursor = lectra_database.cursor()
    with lectra_database:
        cursor.execute(
        "INSERT INTO transcript_imports(transcript_hash,created_at)VALUES(?,?)",(transcript_hash,time_stamp)
    )
    import_id = cursor.lastrowid
    lectra_database.close()
    return import_id
def find_completed_transcript_import(transcript_hash):
    lectra_database = sqlite3.connect('lectra.db')
    cursor = lectra_database.cursor()
    cursor.execute(
        "SELECT DISTINCT t.id, t.transcript_hash FROM transcript_imports t JOIN assignments a ON t.id = a.import_id WHERE t.transcript_hash = ? ORDER BY t.id DESC",(transcript_hash,))
    row = cursor.fetchone()
    lectra_database.close()
    if(row):
        return row
    return None


    

    



initialize_database()


