import os
from hashlib import sha1
from subprocess import call
from django.conf import settings
from django.template.loader import add_to_builtins

add_to_builtins('masher.templatetags.masher_tags')

APP_PATH = os.path.abspath(os.path.dirname(__file__))
CLOSURE_JAR_PATH = os.path.join(APP_PATH, 'compressors', 'compiler.jar')
MASHER_OUTPUT_DIR = APP_PATH

CLOSURE_BASE_COMMAND = ["java", "-jar", CLOSURE_JAR_PATH]

class MashMedia(object):

    def __init__(self):
        self._mashed_files = {}

    def mash(self, files):
        new_filename = self.create_output_filename(files)

        if new_filename in self._mashed_files:
            self.check_for_invalid_remash(files, self._mashed_files[new_filename])
        else:
            self.cache_and_compile(files, new_filename)

        file_url = "%s%s" % (settings.MEDIA_URL, new_filename)

        return file_url


    def check_for_invalid_remash(self, new_files, existing_files):
        """
        if ['a.js', 'b.js', 'c.js'] is mashed and ['c.js', 'b.js', 'a.js'] is
        also mashed, there could be a javascript error if 'b.js' needs 'a.js'
        to be loaded first in the browser. since only unique combinations of files
        are mashed order is important to ensure that the files are combined in
        the way that they need to load in the browser.
        """
        if new_files != existing_files:
            raise ValueError("""
                These files have already been mashed, but in a different order.
                This could prove to result in undesirable results.
            """)

    def cache_and_compile(self, files, new_filename):
        self._mashed_files[new_filename] = files
        if getattr(settings, 'MASHER_COMPRESS', True):
            self.closure_compile(files, new_filename)
        else:
            self.combine_uncompressed(files, new_filename)

    def closure_compile(self, files, new_filename):
        args = ['--js_output_file', self.create_full_output_path(new_filename)]

        for js_file in files:
            args += ["--js", js_file]

        call(CLOSURE_BASE_COMMAND + args)

    def get_file_contents(self, file):
        return open(file, 'r').read()

    def combine_uncompressed(self, files, filename):
        with open(self.create_full_output_path(filename), 'w') as combined_file:
            for file in files:
                contents = self.get_file_contents(file)
                combined_file.write(contents)

    def create_full_output_path(self, filename):
        return os.path.join(self.get_output_dir(), filename)

    def create_output_filename(self, files):
        sorted_file_names = self.sort_names(files)
        file_name_string = self.join_names(sorted_file_names)
        filename_hash = self.hash_names(file_name_string)
        return "%s.min.js" % filename_hash

    def get_output_dir(self):
        return getattr(settings, 'MASHER_OUTPUT_DIR', MASHER_OUTPUT_DIR)

    def sort_names(self, files):
        return sorted(files)

    def join_names(self, sorted_file_names):
        return ''.join(sorted_file_names)

    def hash_names(self, combined_file_names):
        return sha1(combined_file_names).hexdigest()


site = MashMedia()