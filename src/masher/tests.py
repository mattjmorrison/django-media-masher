from hashlib import sha1
from mock import patch, Mock

from django import test
from django.conf import settings
from django.template import Template, Context

import masher
import os

class MashTemplateTagTests(test.TestCase):

    @patch('masher.MashMedia.mash')
    def test_returns_hashed_filename(self, mash):
        template = Template("""
        src="{% mash 'one.js' "two.js" three.js %}"
        """)
        result = template.render(Context())
        self.assertEqual(((['one.js', 'two.js', 'three.js'],), {}), mash.call_args)
        self.assertEqual('src="%s"' % mash.return_value, result.strip())

class MashMediaTests(test.TestCase):

    def setUp(self):
        self.files = ('one.js', 'two.js', 'three.js')
        self.mash = masher.MashMedia()

    def test_files_are_ordered(self):
        self.assertEqual(['one.js', 'three.js', 'two.js'], self.mash.sort_names(self.files))

    def test_files_are_combined_into_string(self):
        self.assertEqual('one.jstwo.jsthree.js', self.mash.join_names(self.files))

    def test_combined_file_names_are_hashed(self):
        file_names = "one.jstwo.jsthree.js"
        hashed_file_names = sha1(file_names).hexdigest()
        self.assertEqual(hashed_file_names, self.mash.hash_names(file_names))

    @patch('masher.MashMedia.sort_names')
    @patch('masher.MashMedia.join_names')
    @patch('masher.MashMedia.hash_names')
    def test_mash_sorts_joins_and_hashes_file_names(self, mock_hash, mock_join, mock_sort):
        mock_hash.return_value = "somehash"
        output_path = "%s.min.js" % mock_hash.return_value
        result = self.mash.create_output_filename(self.files)
        self.assertEqual(((self.files,), {}), mock_sort.call_args)
        self.assertEqual(((mock_sort.return_value, ), {}), mock_join.call_args)
        self.assertEqual(((mock_join.return_value, ), {}), mock_hash.call_args)
        self.assertEqual(output_path, result)

    @patch('masher.MashMedia.create_full_output_path')
    @patch('masher.call')
    def test_passes_each_file_to_closure_compiler(self, call_mock, create_full_path):
        self.mash.closure_compile(self.files, "x")
        compile_jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    'compressors', 'compiler.jar'))
        closure_command = ["java", "-jar", compile_jar_path]
        closure_command += ['--js_output_file', create_full_path.return_value]
        for js_file in self.files:
            closure_command += ["--js", js_file]

        self.assertEqual((('x',), {}), create_full_path.call_args)
        self.assertEqual(((closure_command, ), {}), call_mock.call_args)

    @patch('masher.MashMedia.create_output_filename')
    @patch('masher.MashMedia.closure_compile')
    def test_mashes_all_files(self, closure_compile, create_filename):
        settings.MEDIA_URL = '/media/'
        media_url = self.mash.mash(self.files)
        self.assertEqual(((self.files, create_filename.return_value,), {}),
                         closure_compile.call_args)
        self.assertEqual("%s%s" % (settings.MEDIA_URL, create_filename.return_value),
                         media_url)

    @patch('masher.MashMedia.closure_compile', Mock())
    def test_that_all_mashed_files_are_kept_track_of(self):
        self.mash.mash(self.files)
        other_files = ['asdf.js', 'xyz.js']
        self.mash.mash(other_files)
        self.assertEqual({self.mash.create_output_filename(self.files):self.files,
                          self.mash.create_output_filename(other_files):other_files},
                         self.mash._mashed_files)

    @patch('masher.MashMedia.closure_compile', Mock())
    def test_error_happens_when_same_files_are_in_different_order(self):
        self.mash.mash(self.files)
        self.assertRaises(ValueError, self.mash.mash, reversed(self.files))

    def test_output_dir_can_be_customized(self):
        original_setting = None
        if hasattr(settings, 'MASHER_OUTPUT_DIR'):
            original_setting = getattr(settings, 'MASHER_OUTPUT_DIR')

        settings.MASHER_OUTPUT_DIR = "/output/"
        filename = self.mash.create_full_output_path("file_name")

        self.assertEqual('/output/file_name', filename)

        if original_setting:
            settings.MASHER_OUTPUT_DIR = original_setting

#TODO - use yuicompressor for css
#    @patch('masher.MashMedia.create_output_filename')
#    @patch('masher.MashMedia.closure_compile')
#    @patch('masher.MashMedia.yui_compile')
#    def test_use_yuicompressor_when_configured(self, yui_compile, closure_compile, filename):
#        original_setting = None
#        if hasattr(settings, 'MASH_WITH_YUI'):
#            original_setting = getattr(settings, 'MASH_WITH_YUI')
#
#        settings.MASH_WITH_YUI = True
#        self.mash.mash(self.files)
#        self.assertFalse(closure_compile.called)
#        self.assertEqual(((self.files, filename.return_value), {}), yui_compile.call_args)
#
#        if original_setting:
#            settings.MASH_WITH_YUI = original_setting

#    @patch('masher.call')
#    def test_passes_each_file_to_yui_compressor_when_css_files(self, call_mock):
#        output_filename = 'outputfilename'
#        self.mash.yui_compile(self.files, output_filename)
#        jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                                    '..', 'yui_compressor-2.4.2.jar'))
#        closure_command = ["java", "-jar", jar_path]
#        closure_command += ['--js_output_file', output_filename]
#        for js_file in self.files:
#            closure_command += ["--js", js_file]
#
#        self.assertEqual(((closure_command, ), {}), call_mock.call_args)
