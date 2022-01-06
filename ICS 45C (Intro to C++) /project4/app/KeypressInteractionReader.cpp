// KeypressInteractionReader.cpp
//
// ICS 45C Fall 2021
// Project #4: People Just Want to Play with Words
//
// Implementation of the KeypressInteractionReader
//
// YOU WILL NEED TO IMPLEMENT SOME THINGS HERE

#include "KeypressInteractionReader.hpp"
#include "Command.hpp"
#include "Interaction.hpp"
#include "cursorright.hpp"
#include "cursorleft.hpp"
#include "cursorup.hpp"
#include "cursordown.hpp"
#include "cursorhome.hpp"
#include "cursorend.hpp"
#include "insertchar.hpp"
#include "backspace.hpp"
#include "newline.hpp"
#include "deleteline.hpp"

// You will need to update this member function to watch for the right
// keypresses and build the right kinds of Interactions as a result.
//
// The reason you'll need to implement things here is that you'll need
// to create Command objects, which you'll be declaring and defining
// yourself; they haven't been provided already.
//
// I've added handling for "quit" here, but you'll need to add the others.

Interaction KeypressInteractionReader::nextInteraction()
{
    while (true)
    {
        Keypress keypress = keypressReader.nextKeypress();

        if (keypress.ctrl())
        {
            // The user pressed a Ctrl key (e.g., Ctrl+X); react accordingly

            switch (keypress.code())
            {
                case 'O':
                    return Interaction::command(new CursorRight());
                
                case 'U':
                    return Interaction::command(new CursorLeft());

                case 'I':
                    return Interaction::command(new CursorUp());

                case 'K':
                    return Interaction::command(new CursorDown());

                case 'Y':
                    return Interaction::command(new CursorHome());

                case 'P':
                    return Interaction::command(new CursorEnd());

                case 'J':
                    return Interaction::command(new NewLine());

                case 'M':
                    return Interaction::command(new NewLine());

                case 'H':
                    return Interaction::command(new BackSpace());

                case 'D':
                    return Interaction::command(new DeleteLine());

                case 'Z':
                    return Interaction::undo();

                case 'A':
                    return Interaction::redo();

                case 'X':
                    return Interaction::quit();
            }
        }
        else
        {
            return Interaction::command(new InsertCharacter(keypress.code()));
            // The user pressed a normal key (e.g., 'h') without holding
            // down Ctrl; react accordingly
        }
    }
}

