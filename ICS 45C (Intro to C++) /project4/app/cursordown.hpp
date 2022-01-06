#ifndef CURSORDOWN_HPP
#define CURSORDOWN_HPP

#include "Command.hpp"

class CursorDown: public Command
{
public:
    virtual void execute(EditorModel& model);
    virtual void undo(EditorModel& model);
};



#endif 