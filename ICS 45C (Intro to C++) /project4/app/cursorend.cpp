#include "cursorend.hpp"

void CursorEnd::execute(EditorModel& model){
    prevcol = model.cursorColumn();
    model.end();
}
void CursorEnd::undo(EditorModel& model){
    model.setCursor(model.cursorLine(), prevcol);
}