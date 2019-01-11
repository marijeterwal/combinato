"""
formatter for decoupage
"""

import mimetypes
import os
from cropresize import crop_resize
from decoupage.formatters import FormatterBase

# PIL
try:
    import Image
except:
    from PIL import Image

class Images(FormatterBase):
    """display images with thumbnails"""

    defaults = { 'size': 'x',
                 'columns': None,
                 'thumb_dir': 'thumbs',
                 'thumb_prefix': 'thumb_'}

    def __init__(self, arg):
        FormatterBase.__init__(self, arg)

        # get image size for display
        width, height = [ i.strip() for i in self.size.split('x', 1) ]
        self.width = width and int(width) or None
        self.height = height and int(height) or None

    def __call__(self, request, data):

        # add width + height data
        data['width'] = self.width
        data['height'] = self.height

        # filter out non-images
        _files = []
        for f in data['files']:
            mimetype = mimetypes.guess_type(f['name'])[0]
            if mimetype and mimetype.split('/')[0] == 'image':
                _files.append(f)
                f['link'] = f['path']
        data['files'] = _files
        
        # columns for grid display
        if self.columns is None:
            data['columns'] = len(data['files'])
        else:
            data['columns'] = int(self.columns)

        # thumbnails 
        if 'thumbnails' not in self.args:
            return
        thumb_dir = self.thumb_dir
        if not os.path.isabs(thumb_dir):
            thumb_dir = os.path.join(data['directory'], self.thumb_dir)
        else:
            raise NotImplementedError
        if not os.path.exists(thumb_dir):
            os.mkdir(thumb_dir)
        for f in data['files']:
            filepath = os.path.join(data['directory'], f['name'])
            thumbnail = '%s%s' % (self.thumb_prefix, f['name'])
            thumbnail_file = os.path.join(data['directory'], thumb_dir, thumbnail)
            create_thumbnail = False
            if os.path.exists(thumbnail_file):

                try:
                    # ensure the size is smaller than the specified size
                    thumb = Image.open(thumbnail_file)
                    if self.width and thumb.size[0] > self.width:
                        create_thumbnail = True
                    if self.height and thumb.size[1] > self.height:
                        create_thumbnail = True

                except:
                    pass

                # ensure the original file has not been modified
                if os.path.getmtime(thumbnail_file) < os.path.getmtime(filepath):
                    create_thumbnail = True

            else:
                # create a new thumbnail
                create_thumbnail = True
            
            if create_thumbnail: # do thumbnail creation

                flag = False
                try:
                    image = Image.open(filepath)
                    thumbnail_image = crop_resize(image, (self.width, self.height))
                    fd = file(thumbnail_file, 'w')
                    flag = True
                    thumbnail_image.save(fd)
                    fd.close()

                except Exception, e: # failure to create thumbnail
                    # cleanup file
                    if flag:
                        fd.close()
                        os.remove(thumbnail_file)
    
            # fix the path to point to the thumbnail
            if os.path.exists(thumbnail_file):
                f['path'] = '%s/%s/%s' % (f['path'].rsplit('/', 1)[0],
                                          self.thumb_dir,
                                          thumbnail)
    
