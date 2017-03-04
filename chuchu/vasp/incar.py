import re
import logging

class Incar(object):

    """Incar class representation of a vasp incar file"""

    def __init__(self):
        self.logger = logging.getLogger("vasp:incar")
        self.props = dict()
    def get(self, key):
        """Get vale for a key in the incar settings

        :key: String with the incar key.
        :returns: Value

        """
        if not key in self.props.keys():
            return False
        else:
            return self.props[key]
    def set(self, key, value):
        """Set value for a given key

        :key: TODO
        :value: TODO
        :returns: TODO

        """
        self.props[key] = value
    def keys(self):
        """TODO: Docstring for getKeys.
        :returns: TODO

        """
        return self.props.keys()
    def load(self, obj):
        """Load an incar file

        :obj: TODO
        :returns: TODO

        """
        if type(obj) is file:
            f = obj
        elif type(obj) is str:
            f = open(obj, "r")
        self.logger.debug("Cleaning up comments")
        contents = re.sub(r"!.*\n", r"\n", f.read())
        contents = "\n".join(contents.split(";")).split("\n")
        is_variable = lambda line: re.match(r"\s*(\w+)\s*=(.*)[!]?$", line)
        for line in contents:
            m = is_variable(line)
            if m:
                key = m.group(1)
                val = m.group(2)
                self.logger.debug("Got %s = %s"%(key,val))
                self.set(key,val)
    def dump(self, fmt="vasp", fd=None):
        """TODO: Docstring for dump.

        :fmt: TODO
        :fd: TODO
        :returns: TODO

        """
        content = self.dumpVasp()
        if not fd:
            self.logger.debug("Returning output string")
            return content
        else:
            self.logger.debug("Writing output in %s"%fd)
            fd.write(content)
    def dumpVasp(self):
        """TODO: Docstring for dumpVasp.
        :returns: TODO

        """
        content = []
        for key in self.keys():
            content += ["%s = %s"%(key, self.get(key))]
        return "\n".join(content)

