Caja Wipe
===============

An extension for Caja to securely delete files , using the `secure-delete`
programme.

Description
==============

Caja Wipe is a small Python 3 extension for the Caja file manager (the default
file manager in MATE) that adds options to the right-click menu to securely
delete files.
`srm` is called when deleting files. The deletion algorithm is this:
```
*      1 pass with 0xff

*      5 random passes. /dev/urandom is used for a secure RNG if available.

*      27 passes with special values defined by Peter Gutmann.

*      5 random passes. /dev/urandom is used for a secure RNG if available.

*      Rename the file to a random value

*      Truncate the file

As an additional measure of security, the file is opened in O_SYNC mode and
after each pass an fsync() call is done.  srm writes 32k blocks for the
purpose of speed, filling buffers of disk caches to force them to flush and
overwriting old data which belonged to the file.
```

Examples
==============
You want to completely remove a document with your bank account number from
your computer.  

You need to delete your private GPG key from your secret folder.  

You just really, *really*, don't want anyone to see that embarassing photo from
grade school...

Building and Installing
=======================
Debian (and Debian-based distros)  
a) Download source code  
```
git clone https://github.com/Fred-Barclay/Caja-Wipe.git
cd Caja-Wipe
dpkg-buildpackage
cd .. && sudo dpkg -i install caja-wipe_0.8.9_all.deb
```


Limitations
==============
(Adapted from the man page of `srm`):
 - NFS:    Beware of NFS. You can't ensure you really completely wiped your data
from the remote disks, especially because of caching.

 - Raid:   Raid Systems use stripped disks and have got large caches. It's hard
wipe them.

 - Swap: For secure deletion of the swap space, use `sswap`. Due to the great
difficulty in setting up a generic implementation to `sswap`, and the potential
for system damage this command might cause, Caja Wipe does not have a option
to this so you will have to use the command line.

 - Some of your data might have a temporary (deleted) copy somewhere on the
disk.

	If this is a concern, the secure-delete suite, which should be installed as
a dependency to Caja Wipe on Debian-based distros (Debian, Linux Mint, etc),
comes with the `sfill` command which can be used to delete *all* free space on
your hard drive. Beware that this may take a very long time. If you abort the
process before it ends, you may end up with extra files in various locations
that may take up a great deal of space.

Credits
==============
Portions of this README were copied and modified from the man page to `srm`;
copyright van Hauser / THC <vh@thc.org>.

License
==============
Caja Wipe is dual-licensed under the GPLv2, or, at your option, any later
version; and custom, highly-permissive licensing terms.

The text for both can be found in the COPYING file. A list of authors is in the
AUTHORS file.

Copyright (C) 2016 Caja Wipe authors.
