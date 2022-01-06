#include "insertchar.hpp"

InsertCharacter::InsertCharacter(char text)
    : text{text}
{}

void InsertCharacter::execute(EditorModel& model){
    model.insertcharacter(text);
}
void InsertCharacter::undo(EditorModel& model){
    model.backspace();
}