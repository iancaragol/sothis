# Sothis

Sothis is an application that automatically places holds or checks out ebooks from any OverDrive library catalog using the user's *want-to-read* shelf on Goodreads.

### Example use case
A typical use case looks something like this:

1) A Goodreads user places *Harry Potter and the Deathly Hallows* on their *want-to-read* shelf.
2) Sothis scans the users shelf and checks the title's availability in all libraries that the user has an account at.
3) If the *Harry Potter and the Deathly Hallows* is available at any one of the user's libraries, Sothis checks it out using the OverDrive API.
4) If the book is not available, Sothis places a hold on it at all libraries. 
5) Once the book is checked out or moved from the *want-to-read* shelf, Sothis either cancels all holds or returns the book.

### Future Features
1) Popular ebooks may have waiting lists as long as 6 months. Sothis automatically manages holds so that, if the book is part of a series, as much of the series as possible will be available within the same time frame.
	
	For example, *Skyward by Brandon Sanderson* will be available in two weeks. *Starsight*, its sequel will not be available for another 5 weeks. Sothis automatically suspends the hold on *Skyward* until both *Startsight* and *Skyward* will be available in the same return period.

2) If the any one part of a series is placed on the users *want-to-read* shelf, Sothis will place holds on the entire series and suspend those holds until the user is ready to read.
