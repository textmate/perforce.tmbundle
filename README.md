Welcome to Perforce
===================

This bundle is meant to help Subversion users transition to Perforce.  Its commands are mapped to Command-4.  (It was forked from an older plugin, which used the slightly-more-awkward Command-Shift-F.  Unported commands still live at that mapping.)

Unlike Subversion, Perforce requires you to mark which files you intend to edit before you commit them.  This is quite tedious.  Thankfully, this bundle extends the Save command to mark the file as edited on your behalf as soon as you save.  Unfortunately, the command isn't run until after the Save happens, which means TextMate will ask you if it's OK to overwrite the file.  (Perforce marks files as read-only until you `edit`.)

Don't worry!  Ignore the flashing blue warning and click Overwrite.  As soon as you do, the bundle will mark the file with `edit`.

TODO:
-----

 - Fix the `Submit Changelist…` command.
 - Implement `shelve`/`unshelve`.

Licensing:
----------

 - This bundle is licensed under the GPLv2.  It includes the p4python library, supplied by Perforce under the terms of the Apache license.  It also includes portions of an earlier Perforce bundle by Adam Vandenberg and Daniel Stockman, used with permission.