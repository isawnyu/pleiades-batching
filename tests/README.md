# README for tests

There's config for the tests, using the "testconfig" package. This means you
need to run "nosetests" with some config parameters. Here are the options:

To perform tests/functions that need HTTP, use: 

> nosetests --tc-file tests/test_config.ini 

To skip HTTP use (i.e., if you're offline):

> nosetests --tc-file tests/test_config.ini --tc=error_handling.skip_http_tests:yes

