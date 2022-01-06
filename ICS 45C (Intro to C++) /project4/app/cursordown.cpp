#include "cursordown.hpp"

void CursorDown::execute(EditorModel& model){
    model.down();
}
void CursorDown::undo(EditorModel& model){
    model.up();
}