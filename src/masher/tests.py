from hashlib import sha1
from mock import patch, Mock, MagicMock

from django import test
from django.conf import settings
from django.template import Template, Context

import masher
import os

class MashTemplateTagTests(test.TestCase):

    @patch('masher.MashMedia.mash')
    def test_returns_hashed_filename(self, mash):
        template = Template("""
        src="{% mash MEDIA_ROOT 'one.js' "two.js" three.js %}"
        """)
        result = template.render(Context({'MEDIA_ROOT':'/asdf'}))
        self.assertEqual(((['/asdf/one.js', '/asdf/two.js', '/asdf/three.js'],), {}),
                         mash.call_args)
        self.assertEqual('src="%s"' % mash.return_value, result.strip())

class MashCssMediaTests(test.TestCase):

    def setUp(self):
        self.files = ('one.css', 'two.css', 'three.css')
        self.mash = masher.MashMedia()

    @patch('masher.MashMedia.create_full_output_path')
    @patch('masher.call')
    @patch('masher.MashMedia.create_concat_file')
    def test_passes_each_file_to_yui_compressor(self, concat_files, call_mock, create_full_path):

        new_filename = 'x'
        self.mash.yui_compress(self.files, new_filename)
        self.assertEqual(((self.files, new_filename), {}), concat_files.call_args)

        compile_jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'compressors', 'yuicompressor-2.4.2.jar'))
        yui_command = ['java', '-jar', compile_jar_path, '--type',
                           'css', '-o', create_full_path.return_value, new_filename]
        self.assertEqual(((yui_command,), {}), call_mock.call_args)
        self.assertEqual(((new_filename,), {}), create_full_path.call_args)

    @patch('shutil.copyfileobj')
    @patch('__builtin__.open')
    def test_concats_files_together(self, open_mock, copy_file_object):
        filehandle = open_mock.return_value = MagicMock()
        new_filename = 'x'
        self.mash.create_concat_file(self.files, new_filename)

        self.assertTrue(filehandle.__enter__.called)
        self.assertTrue(filehandle.__exit__.called)

        self.assertEqual([((new_filename, 'w'), {}),
                          ((self.files[0], 'r'), {}),
                          ((self.files[1], 'r'), {}),
                          ((self.files[2], 'r'), {}),
                          ], open_mock.call_args_list)

        self.assertEqual([((open_mock.return_value, filehandle), {}),
                          ((open_mock.return_value, filehandle), {}),
                          ((open_mock.return_value, filehandle), {}),
                          ],
                         copy_file_object.call_args_list)

    @patch('masher.MashMedia.are_all_css', Mock(return_value=True))
    @patch('masher.MashMedia.combine_uncompressed')
    @patch('masher.MashMedia.closure_compile')
    @patch('masher.MashMedia.yui_compress')
    def test_yui_compress_is_called_instead_of_closure_compile_when_css(self, yui_compress, closure_compile, combine_uncompressed):
        original_setting = None
        if hasattr(settings, 'MASHER_COMPRESS'):
            original_setting = getattr(settings, 'MASHER_COMPRESS')

        settings.MASHER_COMPRESS = True

        new_filename = 'x'
        self.mash.cache_and_compile(self.files, new_filename)
        self.assertEqual(((self.files, new_filename), {}), yui_compress.call_args)
        self.assertFalse(closure_compile.called)
        self.assertFalse(combine_uncompressed.called)

        if original_setting:
            settings.STATIC_ROOT = original_setting

    def test_returns_false_when_no_files_are_css(self):
        self.assertFalse(self.mash.are_all_css(['first.js', 'second.js', 'third.js']))

    def test_returns_false_when_not_all_files_are_css(self):
        self.assertFalse(self.mash.are_all_css(['first.css', 'second.js', 'third.js']))

    def test_returns_true_when_all_files_are_css(self):
        self.assertTrue(self.mash.are_all_css(['first.css', 'second.css', 'third.css']))

class MashJavaScriptMediaTests(test.TestCase):

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
        if hasattr(settings, 'STATIC_ROOT'):
            original_setting = getattr(settings, 'STATIC_ROOT')

        settings.STATIC_ROOT = "/output/"
        filename = self.mash.create_full_output_path("file_name")

        self.assertEqual('/output/file_name', filename)

        if original_setting:
            settings.STATIC_ROOT = original_setting

    @patch('masher.MashMedia.closure_compile')
    @patch('masher.MashMedia.combine_uncompressed')
    def test_combines_but_does_not_compress_when_option_is_off(self, combine_uncompressed, closure_compile):
        original_setting = None
        if hasattr(settings, 'MASHER_COMPRESS'):
            original_setting = getattr(settings, 'MASHER_COMPRESS')

        settings.MASHER_COMPRESS = False

        filename = Mock()

        self.mash.cache_and_compile(self.files, filename)

        self.assertEqual(((self.files, filename), {}), combine_uncompressed.call_args)
        self.assertFalse(closure_compile.called)

        if original_setting:
            settings.MASHER_COMPRESS = original_setting
        else:
            del settings.MASHER_COMPRESS

    @patch('masher.MashMedia.create_full_output_path')
    @patch('__builtin__.open')
    def test_creates_file(self, open_mock, create_fill_path):
        filehandle = MagicMock()
        open_mock.return_value = filehandle
        filename = Mock()
        self.mash.combine_uncompressed(self.files, filename)

        self.assertEqual(((filename,), {}), create_fill_path.call_args)
        self.assertEqual([
                            ((create_fill_path.return_value, 'w'), {}),
                            ((self.files[0], 'r'), {}),
                            ((self.files[1], 'r'), {}),
                            ((self.files[2], 'r'), {}),
                         ], open_mock.call_args_list)
        self.assertTrue(filehandle.__enter__.called)
        self.assertTrue(filehandle.__exit__.called)

    @patch('__builtin__.open')
    def test_gets_file_contents(self, open_mock):
        filename = "filename"
        contents = self.mash.get_file_contents(filename)

        self.assertEqual(((filename, 'r'), {}), open_mock.call_args)
        self.assertEqual(open_mock.return_value.read.return_value, contents)

    @patch('masher.MashMedia.get_file_contents')
    @patch('__builtin__.open')
    def test_appends_files(self, open_mock, get_contents):
        filehandle = MagicMock()
        file_object = Mock()
        filehandle.__enter__.return_value = file_object
        open_mock.return_value = filehandle
        self.mash.combine_uncompressed([1], Mock())

        self.assertTrue(file_object.write.called)
        self.assertEqual(((get_contents.return_value,), {}), file_object.write.call_args)