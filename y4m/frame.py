
__all__ = ['Frame']


from collections import namedtuple


class Frame(namedtuple('Frame', ['buffer', 'headers', 'count'])):
    def __repr__(self):
        return '<frame %d: %dx%d>' % (self.count, self.headers['H'], self.headers['W'])
