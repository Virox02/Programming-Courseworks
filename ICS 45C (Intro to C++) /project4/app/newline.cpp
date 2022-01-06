#include "newline.hpp"

void NewLine::execute(EditorModel& model){
    model.newline();
}
void NewLine::undo(EditorModel& model){
    model.backspace();
}