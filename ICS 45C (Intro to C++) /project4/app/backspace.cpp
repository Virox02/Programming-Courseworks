#include "backspace.hpp"

void BackSpace::execute(EditorModel& model){
    prevcol = model.cursorColumn();
    model.backspace();
    if (prevcol > 1){
        prevchar = model.char_deleted;
    }
}
void BackSpace::undo(EditorModel& model){
    if (prevcol == 1){
        model.newline();
    } else{
        model.insertcharacter(prevchar);
    }
}