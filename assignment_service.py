from assignment_storage import get_assignment,save_explanation
from ai_processor import explain_assignment

def coordination():
    assignments = get_assignment()
    selected_assignment = assignments[1]

    if selected_assignment['ai_explanation'] is not None:
        explanation = selected_assignment['ai_explanation']
        print("Test did not update")
    else:
        explanation = explain_assignment(selected_assignment)
        save_explanation(assignment_id=selected_assignment['id'],explanation=explanation)
        print("Test did update")
coordination() 
    


