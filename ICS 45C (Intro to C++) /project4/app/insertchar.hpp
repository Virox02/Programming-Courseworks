#ifndef INSERTCHAR_HPP
#define INSERTCHAR_HPP

#include "Command.hpp"

class InsertCharacter: public Command
{
public:
    InsertCharacter(char text);
    virtual void execute(EditorModel& model);
    virtual void undo(EditorModel& model);

private:
    char text;
    
};



#endif 