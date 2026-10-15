import sqlite3
import json


def initialize_database():
   lectra_database = sqlite3.connect('lectra.db')
   cursor = lectra_database.cursor()
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
   lectra_database.close()

def save_assignment(assignment):
        description = assignment.description
        requirements = json.dumps(assignment.requirements)
        min_word_count=assignment.min_word_count
        max_word_count = assignment.max_word_count
        deadline = assignment.deadline
        lectra_database = sqlite3.connect('lectra.db')
        cursor = lectra_database.cursor()
        with lectra_database:
            cursor.execute(
              "INSERT INTO assignments(description,requirements,min_word_count,max_word_count,deadline)VALUES(?,?,?,?,?)",(description,requirements,min_word_count,max_word_count,deadline)
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
     

initialize_database()


