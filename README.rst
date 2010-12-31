!!! This is still under development !!!

Django Media Masher
===================

Django Media Masher uses Closure Compiler (http://code.google.com/closure/compiler/)
and YUI Compressor (http://developer.yahoo.com/yui/compressor/) to
optimize JavaScript and CSS media for Django applications.

What happens...
===================

There are a lot of different places in a Django application that uses in
Forms, Widgets and in Templates.  This is very powerful and gives
developers a lot of flexibility in how they design their applications, but at
the same time, it sucks... a lot (see Why Does it suck?).

What Media Masher does is it allows you to keep your JavaScript and CSS source
code logically separated into different directories, files, and written in a
readable manner.  At server startup time, all related files are optimized
into a single file and put in your MASHER_OUTPUT_DIR. Media Masher also generates
a unique name for each unique combination of files and keeps track so it doesn't
regenerate the same thing more than once.  

Why Does it suck?
===================

All JavaScript and CSS should be optimized so it downloads quickly, however nobody
wants to write optimized JavaScript or CSS because it is horribly unreadable and
hard to maintain.

I don't want to have to remember to run all of my JavaScript and CSS through an
optimizer every time I deploy, I don't want my CI environment to have those
additional steps either, and I also don't want to have to maintain a copy of source code
and optimized code, different file names or directories.

Finally, I don't want to have any server side processing for my static CSS and JavaScript
files, that shouldn't be necessary.

How to use it...
===================

Forms::
    from masher import site

    class MyForm(forms.Form):
        # ... fields ...
        class Media:
            js = (site.mash(['path/to/media/file.js'],)
            css = {
                'all': (site.mash(['path/to/media/file.css'],)
            }

Widgets::
    from masher import site
    class CalendarWidget(forms.TextInput):
        class Media:
            js = (site.mash(['path/to/media/file.js'],)
            css = {
                'all': (site.mash(['path/to/media/file.css'],)
            }

Templates::
    {% mash 'path/to/media/file1.css' 'path/to/media/file2.css' %}
    {% mash 'path/to/media/file1.js' 'path/to/media/file2.js' %}