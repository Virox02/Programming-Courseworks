#include "cursorhome.hpp"

void CursorHome::execute(EditorModel& model){
    prevcol = model.cursorColumn();
    model.home();
}
void CursorHome::undo(EditorModel& model){
    model.setCursor(model.cursorLine(), prevcol);
}