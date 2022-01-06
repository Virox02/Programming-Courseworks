#include "cursorleft.hpp"

void CursorLeft::execute(EditorModel& model){
    model.left();
}
void CursorLeft::undo(EditorModel& model){
    model.right();
}