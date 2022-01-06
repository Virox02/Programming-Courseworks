#include "cursorright.hpp"

void CursorRight::execute(EditorModel& model){
    model.right();
}
void CursorRight::undo(EditorModel& model){
    model.left();
}