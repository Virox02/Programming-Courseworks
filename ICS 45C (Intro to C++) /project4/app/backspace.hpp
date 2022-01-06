#ifndef BACKSPACE_HPP
#define BACKSPACE_HPP

#include "Command.hpp"

class BackSpace: public Command
{
public:
    virtual void execute(EditorModel& model);
    virtual void undo(EditorModel& model);

private:
    int prevcol;
    char prevchar;
};



#endif 