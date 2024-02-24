
__all__ = ['Writer']

from .frame import Frame


class Writer(object):
    def __init__(self, fd, verbose=False):
        self._fd = fd
        self._stream_headers = None
        self._count = 0
        self._verbose = verbose

    def _print(self, *args):
        if self._verbose:
            print('Y4M Writer:', ' '.join([str(e) for e in args]))

    def encode(self, frame):
        assert isinstance(frame, Frame), 'only Frame object are supported'
        if self._stream_headers is None:
            assert 'W' in frame.headers, 'No width header'
            assert 'H' in frame.headers, 'No height header'
            assert 'F' in frame.headers, 'No frame-rate header'
            self._stream_headers = frame.headers.copy()
            if 'C' not in self._stream_headers:
                self._stream_headers['C'] = '420jpeg'  # man yuv4mpeg
            data = self._encode_headers(self._stream_headers.copy())
            self._fd.write(b'YUV4MPEG2 ' + data + b' Xpython-y4m\n')
            self._print('generating stream with headers:', self._stream_headers)
        else:
            self._encode_frame(frame)

    def _frame_size(self):
        if self._stream_headers['C'].startswith('420'):
            return self._stream_headers['W'] * self._stream_headers['H'] * 3 // 2
        elif self._stream_headers['C'].startswith('422'):
            return self._stream_headers['W'] * self._stream_headers['H'] * 2
        elif self._stream_headers['C'].startswith('444'):
            return self._stream_headers['W'] * self._stream_headers['H'] * 3
        raise f"only support I420, I422, I444 fourcc (not {self._stream_headers['C']})"

    def _encode_headers(self, headers):
        for k in headers.keys():
            if isinstance(headers[k], int):
                headers[k] = str(headers[k])
            elif isinstance(headers[k], list):
                headers[k] = ':'.join([str(i) for i in headers[k]])
        data = b' '.join([k.encode('ascii') + v.encode('ascii') for k, v in headers.items()])
        return data

    def _encode_frame(self, frame):
        assert len(frame.buffer) == self._frame_size()
        data = self._encode_headers(frame.headers)
        self._fd.write(b'FRAME')
        if len(data) > 0:
            self._fd.write(b' ' + data)
        self._fd.write(b'\n')
        self._fd.write(frame.buffer)
