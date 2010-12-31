!!! This is still under development !!!
!!! not all of these features have been implemented !!!

The Problem
===================

You want to automate the optimization of your JavaScript and CSS during both
development and production.

You obviously don't want to add any manual steps to optimize your static media.

You don't want to obfuscate your source code by optimizing it.

You don't want to worry about changing all of the URLS to your static media
between development and production.

You don't want to have to configure anything for your before/after optimized
files.

The Solution - Django Media Masher
===================

Django Media Masher uses Closure Compiler (http://code.google.com/closure/compiler/)
and YUI Compressor (http://developer.yahoo.com/yui/compressor/) to
optimize JavaScript and CSS media for Django applications.

Other Solutions: http://code.google.com/p/django-compress/

What happens...
===================

There are a lot of different places in a Django application that uses in
Forms, Widgets, Templates, and wherever else you might put them.  This is very
powerful and gives developers a lot of flexibility in how they design their
applications, but at the same time, it sucks... a lot (see Why Does it suck?).

What Media Masher does is it allows you to keep your JavaScript and CSS source
code logically separated into different directories, files, and written in a
readable manner.  At server startup time, all related files
(see What are Related Files?) are optimized into a single file and put in your
MASHER_OUTPUT_DIR. Media Masher also generates a unique name for each unique
combination of files and keeps track so it doesn't regenerate the same thing
more than once.

Why Does it suck?
===================

Django Media Masher doesn't suck (it's awesome, I wrote it), but the problem is solves does!

All JavaScript and CSS should be optimized so it downloads quickly, however nobody
wants to write optimized JavaScript or CSS because it is horribly unreadable and
hard to maintain.

I don't want to have to remember to run all of my JavaScript and CSS through an
optimizer every time I deploy, I don't want my CI environment to have those
additional steps either, and I also don't want to have to maintain a copy of source code
and optimized code, different file names or directories.

Finally, I don't want to have any server side processing for my static CSS and JavaScript
files, that shouldn't be necessary.

What are Related Files?
===================

Related files are a group of files that are used together, for either a form, or a widget
or even a page.

For example, say you've got a page that requires some fancy widgets
included in jQuery UI.  You'll need jQuery, jQueryUI and your own javascript
that uses them.  With Media Masher you can combine these all into a single optimized
file and cut down on HTTP requests. You can also optionally combine jQuery and jQueryUI
into a single file and your code into a separate one. In the latter case, anyplace on your
entire site that you want to use both jQuery and jQueryUI together they will all use the
same optimized file.

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