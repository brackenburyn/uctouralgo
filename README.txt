Tour Algorithm ReadMe file
Noah Brackenbury (noahbrackenbury@gmail.com) wrote a python program (UCtours18.py) to assign BMRD visitors to tours in a way that maximizes the possibility that each person gets at least one tour for which they have indicated a preference.
The program is based on data derived from the web-based registration interface.  As set up for 2018, there were 10 tours with different capacities (number of participants that can be accommodated).  Tours were conducted during two “sessions”, with nine of the tours being repeated and one tour given only once, during the second session.  During “pre-registration” online, each registrant sees a list of the tours, with a brief description and then chooses three tours that interest them the most.  
The program is designed to first fill those tours that have limited capacity and are most frequently selected. For this purpose, each tour is first given a ranking to the tune of the number of times it is selected, divided by the capacity of the tour.  The program fills the tours in decreasing order of “difficulty to fill”. 
For input, the program needs to access two comma-delimited files (.csv).  
The first file, called tours.csv, which contains a row for each tour (this year, there were 10 tours, so ten rows) and four columns, with fields as follows:
Column A:  name of tour exactly as given in output file from the web registration.
Column B: the “difficulty” ranking (which must be manually computed and entered)
Column C: the capacity for session the tour during session 1
Column D:  the capacity for session the tour during session 2
(Generally, the capacity will be the same for both sessions, but for any tour that is offered only once, a capacity of 0 must be entered for the non-used session).
The second file, called people.csv, contains a row for each person who registered (this year, there were 101 registrants, so 101 rows) and four columns, with fields as follows:
Column A:  The name of the registrant (FirstName LastName) as given in the output file from the web registration.
Column B: the name of the first tour selected by the registrant exactly as given in the output file from the web registration
Column C: the name of the second tour selected by the registrant exactly as given in the output file from the web registration
Column D:  the name of third first tour selected by the registrant exactly as given in the output file from the web registration
Program’s Output File is called 2018output.csv, which gives the output in three sections, formatted like this:
The first section shows the tours assigned to each registrant.  This section contains a row for each registrant (for 2018, there were 101 registrants, so 101 rows), with fields in three columns:
Column A:  The name of the registrant (FirstName LastName) as given in the output file from the web registration.
Column B: the name of the first tour assigned to the registrant, exactly as given in the output file from the web registration
Column C: the name of the second tour assigned to the registrant, exactly as given in the output file from the web registration
Then there are two empty spacer rows, followed by the second section, which lists the registrants assigned to each tour during the first session.  For this section, therefore, the number of rows will equal the number of tours (for 2018, there were 10 tours, so 10 lines.  Because tour #10 was not offered during the first session, this tour is listed, but has no assigned registrants). The format for each row is:
Column A: the name of the tour, exactly as given in the output file from the web registration
Column B through Column X  (the number of columns will be equal to the number of registrants assigned to that tour, but cannot exceed the maximum capacity of the tour):  Each column will contain the name of a registrant (FirstName LastName) assigned to this tour during the first session.
Then there is one empty spacer row, followed by the third section, which lists the registrants assigned to each tour during the second session.  The formatting is exactly the same as for the second session: 
Column A: the name of the tour, exactly as given in the output file from the web registration
Column B through Column X  (the number of columns will be equal to the number of registrants assigned to that tour, but cannot exceed the maximum capacity of the tour):  Each column will contain the name of a registrant (FirstName LastName) assigned to this tour during the second session.

In order to run the python program, Python must be installed on your device (ideally Python 3).  You can run it by running "python3 uctours18.py" in your command line or terminal while in the sme directory as the requisite script and input files.  The output file will be generated automatically.
Nuances:
This program should be able to run if a participant selects less than three tours in their preferences, but not more.  
If the total number of registrants is greater than the total capacity of the tours, then some registrants simply will not be placed in two tours.  They will be placed in either 1 or no tours if there is no other possibility.
This program is not currently able to sort registrants based on tours that are mutually exclusive (if two tours focus on the same topic).   
