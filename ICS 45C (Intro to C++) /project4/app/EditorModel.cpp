// EditorModel.cpp
//
// ICS 45C Fall 2021
// Project #4: People Just Love to Play with Words
//
// Implementation of the EditorModel class

#include "EditorModel.hpp"
#include "EditorException.hpp"
#include <vector>
//#include "BooEditLog.hpp"


EditorModel::EditorModel()
    : curline{1}, curcol{1}, editorData{""}, errorMssg{""}
{
}


int EditorModel::cursorLine() const
{
    return curline;
}


int EditorModel::cursorColumn() const
{
    return curcol;
}


int EditorModel::lineCount() const
{
    return editorData.size();
}


const std::string& EditorModel::line(int lineNumber) const
{
    //static std::string removethis = "booedit!!";
    //return removethis;
    return editorData.at(lineNumber-1);
}


const std::string& EditorModel::currentErrorMessage() const
{
    return errorMssg;
}


void EditorModel::setErrorMessage(const std::string& errorMessage)
{
    errorMssg = errorMessage;
}


void EditorModel::clearErrorMessage()
{
    errorMssg = "";
}

void EditorModel::right()
{
    if (curcol <= (editorData.at(curline-1)).length())
    {
        curcol += 1;

    } else{
        if (curline < lineCount()){
            curcol = 1;
            curline += 1;
        } else{
            throw EditorException("THIS IS THE END OF THE FILE!");
        }
    }
}

void EditorModel::left()
{
    if (curcol > 1){
        curcol -= 1;
    } else {
        if (curline > 1){
            curline -= 1;
            curcol = editorData.at(curline-1).length()+1;
        } else {
            throw EditorException("THIS IS THE BEGINNING OF THE FILE!");
        }
    }
}

void EditorModel::up()
{
    if (curline > 1){
        curline -= 1;
        if (curcol > (editorData.at(curline-1)).length()+1){
            curcol = (editorData.at(curline-1)).length()+1;
        }
    } else{
        throw EditorException("YOU HAVE REACHED THE TOP OF THE FILE!");
    }
}

void EditorModel::down()
{
    if (curline < lineCount()){
        curline += 1;
        if (curcol > (editorData.at(curline-1)).length()+1){
            curcol = (editorData.at(curline-1)).length()+1;
        }
    }
    else{
        throw EditorException("YOU HAVE REACHED THE BOTTOM OF THE FILE!");
    }
}

void EditorModel::home()
{
    curcol = 1;
}

void EditorModel::end()
{
    curcol = (editorData.at(curline-1)).length()+1;
}

void EditorModel::newline()
{
    std::string next = editorData.at(curline-1).substr(curcol-1);
    editorData.at(curline-1) = editorData.at(curline-1).substr(0, curcol-1);
    editorData.insert(editorData.begin() + curline, next);
    curline += 1;
    curcol = 1;
}

void EditorModel::backspace()
{
    if (curline == 1 && curcol == 1){
        throw EditorException("THIS IS THE BEGINNING OF THE FILE!");
    } else if (curcol != 1){
        char_deleted = editorData.at(curline-1).at(curcol-2);
        editorData.at(curline-1) = editorData.at(curline-1).erase(curcol-2, 1);
        curcol -= 1;
    } else{
        int l = editorData.at(curline-1).length();
        editorData.at(curline-2) += editorData.at(curline-1);
        editorData.erase(editorData.begin() + (curline-1));
        curline -= 1;
        //booEditLog("got here");
        curcol = (editorData.at(curline-1).length() - l)+1;
        //booEditLog("got here also");
    }
}

void EditorModel::deleteline()
{
    line_deleted = editorData.at(curline-1);
    if (lineCount() != 1){
        editorData.erase(editorData.begin() + curline-1);
        if (curline>1){
            curline -= 1;
        } else{
            curline = 1;
        }
        if (curcol > (editorData.at(curline-1).length()+1)){
            curcol = editorData.at(curline-1).length()+1;
        }
    } else{
        editorData.push_back("");
        editorData.erase(editorData.begin() + curline-1);
        curline = 1, curcol = 1;
    }
}

void EditorModel::undoline(std::string l)
{
    editorData.insert(editorData.begin() + curline-1, l);
}

void EditorModel::insertcharacter(char text)
{
    editorData.at(curline-1) = editorData.at(curline-1).insert(curcol-1, 1, text);
    curcol += 1;
}

void EditorModel::setCursor(int ln, int clmn)
{
    curline = ln;
    curcol = clmn;
}

