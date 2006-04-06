# $Id$

from pyscript.groups import Group, VAlign, HAlign
from pyscript.objects import Text

class PyScriptTest(Group):
    def __init__(self, **options):
        Group.__init__(self, **options)
        self.text = "undecorated"
        self.objects = VAlign()

    def test(self, object, text="undecorated"):
        """
        Test the given object, using the text to indicate what is being
        tested
        """
        if object is None:
            raise ValueError, "I need an object!!"

        if text is not None:
            self.text = text

        self.objects.append( HAlign( object, Text(self.text) ) )
        print "Appending %s" % object.__class__

        return

