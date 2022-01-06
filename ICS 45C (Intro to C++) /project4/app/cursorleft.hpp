#ifndef CURSORLEFT_HPP
#define CURSORLEFT_HPP

#include "Command.hpp"

class CursorLeft: public Command
{
public:
    virtual void execute(EditorModel& model);
    virtual void undo(EditorModel& model);
};



#endif 