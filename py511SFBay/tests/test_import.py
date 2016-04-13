from package.unittest import *

class TestImport(TestCase):
    def test_import(self):
        import py511SFBay

        self.assertTrue(True, 'py511SFBay module imported cleanly')

if __name__ == '__main__':
    main()
