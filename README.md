# I Despise iTunes (idi) - an iTunes Library command-line utility

I wish there were a better option than iTunes. I know there are technically lots of alternatives, but for those of us sufficiently invensted in Apple hardware (iPhone, Macs, etc.) it is sometimes most user-friendly to use the native apps and solutions, even if some of them make you a little angry.

So, the goal here is to have a script to police an iTunes library and the individual songs' metadata.  It can read and parse the XML file that iTunes "exports" (iTunes Library.xml) and also read the library files (their directory structure, filenames, and the metadata embedded within) and compare the information to ensure they're in sync.

The purpose is to also ensure that all MP3s use a single ID3v2.3 tag with only the frames used by iTunes and in the manner that iTunes uses them.  In other words, to ensure all embedded metadata is in the most iTunes compatible form possible.  So, this is used to report on and repair metadata tags that aren't iTunes compatible or where there are any information discrepencies, or at least allow you to try to brute-force update the bad data within the iTunes UI until everything is copacetic.

Lastly, if/when the iTunes library looks consistent (files' metadata matches iTunes Library.xml's details), then you can use this to run other reports on the library that are might be hard to do in the UI.  Examples include listing tracks that are missing values for specific metadata fields that you intend _all_ tracks to have, or to enforce consistent spelling of a composer's name, etc.

## Extra Credit

The last goal, running reports to help you maintain data consistency, may be helped by an extra credit feature.  Specifically, if you're like me then you want all artist and composer names (lyricists, etc.) to all have their names standardized to a specific form.  As such, this command also allows you to maintain a local file (JSON format) of your standardized artist and individuals' names.  This can use and update this when reporting on fields containing such information.

