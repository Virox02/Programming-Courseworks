#ifndef CURSORUP_HPP
#define CURSORUP_HPP

#include "Command.hpp"

class CursorUp: public Command
{
public:
    virtual void execute(EditorModel& model);
    virtual void undo(EditorModel& model);
};



#endif 