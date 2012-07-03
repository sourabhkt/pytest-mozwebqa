#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

pytestmark = pytestmark = [pytest.mark.skip_selenium,
                           pytest.mark.nondestructive]


def testStartWebDriverClient(testdir):
    file_test = testdir.makepyfile("""
        import pytest
        @pytest.mark.nondestructive
        def test_selenium(mozwebqa):
            mozwebqa.selenium.get('http://localhost:8000/')
            header = mozwebqa.selenium.find_element_by_tag_name('h1')
            assert header.text == 'Success!'
    """)
    reprec = testdir.inline_run('--baseurl=http://localhost:8000',
                                '--api=webdriver',
                                '--driver=firefox',
                                file_test)
    passed, skipped, failed = reprec.listoutcomes()
    assert len(passed) == 1

def testSpecifyingFirefoxProfile(testdir):
    """Test that a specified profile is used when starting firefox.
        The profile changes the colors in the browser, which are then reflected when calling
        value_of_css_property.
    """
    path_to_profile_folder = _createProfileFolder()
    file_test = testdir.makepyfile("""
        import pytest, time
        @pytest.mark.nondestructive
        def test_selenium(mozwebqa):
            mozwebqa.selenium.get('http://localhost:8000/')
            header = mozwebqa.selenium.find_element_by_tag_name('h1')
            anchor = mozwebqa.selenium.find_element_by_tag_name('a')
            header_color = header.value_of_css_property('color')
            anchor_color = anchor.value_of_css_property('color')
            assert header_color == 'rgba(255,0,0,1)'
            assert anchor_color == 'rgba(255,105,180,1)'
    """)
    reprec = testdir.inline_run('--baseurl=http://localhost:8000',
        '--api=webdriver',
        '--driver=firefox',
        '--profilepath=' + path_to_profile_folder,
        file_test)
    passed, skipped, failed = reprec.listoutcomes()
    assert len(passed) == 1

def testSpecifyingFirefoxProfileAndOverridingPreferences(testdir):
    """Test that a specified profile is used when starting firefox.
        The profile changes the colors in the browser, which are then reflected when calling
        value_of_css_property. The test checks that the color of the h1 tag is overridden by
        the profile, while the color of the a tag is overridden by the preference.
    """
    path_to_profile_folder = _createProfileFolder()
    file_test = testdir.makepyfile("""
        import pytest, time
        @pytest.mark.nondestructive
        def test_selenium(mozwebqa):
            mozwebqa.selenium.get('http://localhost:8000/')
            header = mozwebqa.selenium.find_element_by_tag_name('h1')
            anchor = mozwebqa.selenium.find_element_by_tag_name('a')
            header_color = header.value_of_css_property('color')
            anchor_color = anchor.value_of_css_property('color')
            assert header_color == 'rgba(255,0,0,1)'
            assert anchor_color == 'rgba(255,0,0,1)'
    """)
    reprec = testdir.inline_run('--baseurl=http://localhost:8000',
        '--api=webdriver',
        '--driver=firefox',
        '--firefoxpref=''{"browser.anchor_color":"#FF0000"}''',
        '--profilepath=' + path_to_profile_folder,
        file_test)
    passed, skipped, failed = reprec.listoutcomes()
    assert len(passed) == 1

def _createProfileFolder():
    import os
    path_to_profile_folder = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'firefox_profile')
    if not os.path.exists(path_to_profile_folder):
        os.makedirs(path_to_profile_folder)
    prefs = [
        'user_pref("browser.anchor_color", "#FF69B4");',
        'user_pref("browser.display.background_color", "#FFFF66");',
        'user_pref("browser.display.foreground_color", "#FF0000");',
        'user_pref("browser.display.use_document_colors", false);',
        'user_pref("browser.visited_color", "#FF99FF");'
    ]
    with open(os.path.join(path_to_profile_folder, 'prefs.js'), 'w') as prefs_js:
        prefs_js.writelines(prefs)
    return path_to_profile_folder

