from assignment_storage import get_assignment,save_explanation
from ai_processor import explain_assignment

def coordination(assignment_id):
    assignments = get_assignment()
    selected_assignment = None
    for assignment in assignments:
        if assignment['id'] == assignment_id:
            selected_assignment = assignment
            break
    if selected_assignment is not None:
        if selected_assignment['ai_explanation'] is not None:
            explanation = selected_assignment['ai_explanation']
            print("Test did not update")
            return explanation
        else:
            explanation = explain_assignment(selected_assignment)
            save_explanation(assignment_id=selected_assignment['id'],explanation=explanation)
            print("Test did update")
            return explanation
    else:
        return None

    


