.. include:: headings.inc


.. _font overview:

=================================================
|phoenix_title|  **Font Overview**
=================================================


Introduction
------------

A font is an object which determines the appearance of text, primarily
when drawing text to a window or device context. A font is determined
by the following parameters (not all of them have to be specified, of
course):

======================== ==========================================
**Point size**	         This is the standard way of referring to text size.
**Family**	         Supported families are: ``wx.DEFAULT``, ``wx.DECORATIVE``, ``wx.ROMAN``, ``wx.SCRIPT``, ``wx.SWISS``, ``wx.MODERN``. ``wx.MODERN`` is a fixed pitch font; the others are either fixed or variable pitch.
**Style**	         The value can be ``wx.NORMAL``, ``wx.SLANT`` or ``wx.ITALIC``.
**Weight**	         The value can be ``wx.NORMAL``, ``wx.LIGHT`` or ``wx.BOLD``.
**Underlining**	         The value can be ``True`` or ``False``.
**Face name**	         An optional string specifying the actual typeface to be used. If ``None``, a default typeface will chosen based on the family.
**Encoding**	         The font encoding (see ``wx.FONTENCODING_XXX`` constants and the :ref:`Font Encodings <font encodings>` for more details)
======================== ==========================================

Specifying a family, rather than a specific typeface name, ensures a
degree of portability across platforms because a suitable font will be
chosen for the given font family, however it doesn't allow to choose a
font precisely as the parameters above don't suffice, in general, to
identify all the available fonts and this is where using the native
font descriptions may be helpful - see below.

Under Windows, the face name can be one of the installed fonts on the
user's system. Since the choice of fonts differs from system to
system, either choose standard Windows fonts, or if allowing the user
to specify a face name, store the family name with any file that might
be transported to a different Windows machine or other platform.

.. note:: There is currently a difference between the appearance of
   fonts on the two platforms, if the mapping mode is anything
   other than ``MM_TEXT``. Under X, font size is always specified in
   points. Under MS Windows, the unit for text is points but 
   the text is scaled according to the current mapping mode. However,
   user scaling on a device context will also scale fonts under both
   environments.
   
   
Native font information
-----------------------

An alternative way of choosing fonts is to use the native font
description. This is the only acceptable solution if the user is
allowed to choose the font using the :ref:`wx.FontDialog` because the
selected font cannot be described using only the family name and so,
if only family name is stored permanently, the user would almost
surely see a different font in the program later.

Instead, you should store the value returned by
:meth:`wx.Font.GetNativeFontInfoDesc` and pass it to
:meth:`wx.Font.SetNativeFontInfo` later to recreate exactly the same
font.

.. note:: Note that the contents of this string depends on the
   platform and shouldn't be used for any other purpose (in
   particular, it is not meant to be shown to the user). Also please
   note that although the native font information is currently
   implemented for Windows and Unix (GTK+ and Motif) ports only, all
   the methods are available for all the ports and should be used to
   make your program work correctly when they are implemented later.
   
