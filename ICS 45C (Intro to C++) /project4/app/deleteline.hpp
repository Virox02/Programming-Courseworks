#ifndef DELETELINE_HPP
#define DELETELINE_HPP

#include "Command.hpp"

class DeleteLine: public Command
{
public:
    virtual void execute(EditorModel& model);
    virtual void undo(EditorModel& model);

private:
    int prevcol;
    int prevline;
    std::string line_deleted;
};



#endif 