montage
=======

Photogallery extension to `decoupage <http://k0s.org/hg/decopage>`_.
If you want to present a directory of images with decoupage, montage
is the way to do it.

montage provides an additional decopage formatter, ``/images``, that
is used to help format an image gallery (i.e. a directory full of
images) for display.

Templates
---------

montage provides additional templates to display a gallery of images
in various formats.

 * strip.html : present images in a filmstrip like environment
 * grid.html: present images in a table
 * sequence.html: present images like a web comic, in sequence
 * background.html: present images with in the body backround

Templates are invoked via the /template keyword in decoupage
configuration. The webmaster may override templates on a site or
directory basis,

Example:
/template = strip.html
