
class SCPPYEXCEPTION(Exception):
    """Base class for exceptions"""


class INVALIDSCPNUMBER(SCPPYEXCEPTION):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"You gave an invalid SCP number: {self.value}"


class NOTSCPWIKILINK(SCPPYEXCEPTION):
    def __init__(self, link):
        self.link = link

    def __str__(self):
        return f"You gave an invalid link, make sure any link is from the scp wiki site. Erroneous value: {self.link}"


class CONTENTNOTFOUND(SCPPYEXCEPTION):
    def __str__(self):
        return f"The page content wasn't found. This shouldn't happen"


class PAGENOTCREATED(SCPPYEXCEPTION):
    def __str__(self):
        return f"That page hasn't been created yet."


class NOTMAINLISTSCP(SCPPYEXCEPTION):
    def __init__(self, link):
        self.link = link

    def __str__(self):
        return f"That link is not a mainlist scp article. Erroneous value: {self.link}"


class SCP001ERROR(SCPPYEXCEPTION):
    def __str__(self):
        return "SCP-001 is a weird one, and I have't added handling for it yet, sorry"


class FAILEDTOLOADCONTENT(SCPPYEXCEPTION):
    def __init__(self, content: str, error):
        self.content = str
        self.e = error

    def __str__(self):
        return f"Failed to load: {self.content}.\n{self.e}"