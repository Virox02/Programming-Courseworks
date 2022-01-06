#include "cursorup.hpp"

void CursorUp::execute(EditorModel& model){
    model.up();
}
void CursorUp::undo(EditorModel& model){
    model.down();
}