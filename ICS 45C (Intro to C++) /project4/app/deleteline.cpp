#include "deleteline.hpp"

void DeleteLine::execute(EditorModel& model){
    prevcol = model.cursorColumn();
    prevline = model.cursorLine();
    model.deleteline();
    line_deleted = model.line_deleted;
}
void DeleteLine::undo(EditorModel& model){
    model.setCursor(prevline, prevcol);
    model.undoline(line_deleted);
}