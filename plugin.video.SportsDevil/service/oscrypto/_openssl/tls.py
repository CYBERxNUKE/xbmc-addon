# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import re
import socket as socket_
import select
import numbers

from asn1crypto import x509

from ._libssl import libssl, LibsslConst
from ._libcrypto import libcrypto, libcrypto_version_info, handle_openssl_error, peek_openssl_error
from .. import _backend_config
from .._errors import pretty_message
from .._ffi import null, bytes_from_buffer, buffer_from_bytes, is_null, buffer_pointer
from .._types import type_name, str_cls, byte_cls, int_types
from ..errors import TLSError
from .._tls import (
    detect_client_auth_request,
    extract_chain,
    get_dh_params_length,
    parse_session_info,
    raise_client_auth,
    raise_dh_params,
    raise_disconnection,
    raise_expired_not_yet_valid,
    raise_handshake,
    raise_hostname,
    raise_no_issuer,
    raise_protocol_error,
    raise_self_signed,
    raise_verification,
    raise_weak_signature,
)
from .asymmetric import load_certificate, Certificate
from ..keys import parse_certificate
from ..trust_list import get_path

if sys.version_info < (3,):
    range = xrange  # noqa


__all__ = [
    'TLSSession',
    'TLSSocket',
]


_trust_list_path = _backend_config().get('trust_list_path')
_line_regex = re.compile(b'(\r\n|\r|\n)')
_PROTOCOL_MAP = {
    'SSLv2': LibsslConst.SSL_OP_NO_SSLv2,
    'SSLv3': LibsslConst.SSL_OP_NO_SSLv3,
    'TLSv1': LibsslConst.SSL_OP_NO_TLSv1,
    'TLSv1.1': LibsslConst.SSL_OP_NO_TLSv1_1,
    'TLSv1.2': LibsslConst.SSL_OP_NO_TLSv1_2,
}


class TLSSession(object):
    """
    A TLS session object that multiple TLSSocket objects can share for the
    sake of session reuse
    """

    _protocols = None
    _ciphers = None
    _manual_validation = None
    _extra_trust_roots = None
    _ssl_ctx = None
    _ssl_session = None

    def __init__(self, protocol=None, manual_validation=False, extra_trust_roots=None):
        """
        :param protocol:
            A unicode string or set of unicode strings representing allowable
            protocols to negotiate with the server:

             - "TLSv1.2"
             - "TLSv1.1"
             - "TLSv1"
             - "SSLv3"

            Default is: {"TLSv1", "TLSv1.1", "TLSv1.2"}

        :param manual_validation:
            If certificate and certificate path validation should be skipped
            and left to the developer to implement

        :param extra_trust_roots:
            A list containing one or more certificates to be treated as trust
            roots, in one of the following formats:
             - A byte string of the DER encoded certificate
             - A unicode string of the certificate filename
             - An asn1crypto.x509.Certificate object
             - An oscrypto.asymmetric.Certificate object

        :raises:
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library
        """

        if not isinstance(manual_validation, bool):
            raise TypeError(pretty_message(
                '''
                manual_validation must be a boolean, not %s
                ''',
                type_name(manual_validation)
            ))

        self._manual_validation = manual_validation

        if protocol is None:
            protocol = set(['TLSv1', 'TLSv1.1', 'TLSv1.2'])

        if isinstance(protocol, str_cls):
            protocol = set([protocol])
        elif not isinstance(protocol, set):
            raise TypeError(pretty_message(
                '''
                protocol must be a unicode string or set of unicode strings,
                not %s
                ''',
                type_name(protocol)
            ))

        valid_protocols = set(['SSLv3', 'TLSv1', 'TLSv1.1', 'TLSv1.2'])
        unsupported_protocols = protocol - valid_protocols
        if unsupported_protocols:
            raise ValueError(pretty_message(
                '''
                protocol must contain only the unicode strings "SSLv3", "TLSv1",
                "TLSv1.1", "TLSv1.2", not %s
                ''',
                repr(unsupported_protocols)
            ))

        self._protocols = protocol

        self._extra_trust_roots = []
        if extra_trust_roots:
            for extra_trust_root in extra_trust_roots:
                if isinstance(extra_trust_root, Certificate):
                    extra_trust_root = extra_trust_root.asn1
                elif isinstance(extra_trust_root, byte_cls):
                    extra_trust_root = parse_certificate(extra_trust_root)
                elif isinstance(extra_trust_root, str_cls):
                    with open(extra_trust_root, 'rb') as f:
                        extra_trust_root = parse_certificate(f.read())
                elif not isinstance(extra_trust_root, x509.Certificate):
                    raise TypeError(pretty_message(
                        '''
                        extra_trust_roots must be a list of byte strings, unicode
                        strings, asn1crypto.x509.Certificate objects or
                        oscrypto.asymmetric.Certificate objects, not %s
                        ''',
                        type_name(extra_trust_root)
                    ))
                self._extra_trust_roots.append(extra_trust_root)

        ssl_ctx = None
        try:
            if libcrypto_version_info < (1, 1):
                method = libssl.SSLv23_method()
            else:
                method = libssl.TLS_method()
            ssl_ctx = libssl.SSL_CTX_new(method)
            if is_null(ssl_ctx):
                handle_openssl_error(0)
            self._ssl_ctx = ssl_ctx

            libssl.SSL_CTX_set_timeout(ssl_ctx, 600)

            # Allow caching SSL sessions
            libssl.SSL_CTX_ctrl(
                ssl_ctx,
                LibsslConst.SSL_CTRL_SET_SESS_CACHE_MODE,
                LibsslConst.SSL_SESS_CACHE_CLIENT,
                null()
            )

            if sys.platform in set(['win32', 'darwin']):
                trust_list_path = _trust_list_path
                if trust_list_path is None:
                    trust_list_path = get_path()

                if sys.platform == 'win32':
                    path_encoding = 'mbcs'
                else:
                    path_encoding = 'utf-8'
                result = libssl.SSL_CTX_load_verify_locations(
                    ssl_ctx,
                    trust_list_path.encode(path_encoding),
                    null()
                )

            else:
                result = libssl.SSL_CTX_set_default_verify_paths(ssl_ctx)
            handle_openssl_error(result)

            verify_mode = LibsslConst.SSL_VERIFY_NONE if manual_validation else LibsslConst.SSL_VERIFY_PEER
            libssl.SSL_CTX_set_verify(ssl_ctx, verify_mode, null())

            # Modern cipher suite list from https://wiki.mozilla.org/Security/Server_Side_TLS late August 2015
            result = libssl.SSL_CTX_set_cipher_list(
                ssl_ctx,
                (
                    b'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:'
                    b'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:'
                    b'DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:'
                    b'kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:'
                    b'ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:'
                    b'ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:'
                    b'DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:'
                    b'DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:'
                    b'AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:'
                    b'AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:'
                    b'!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:'
                    b'!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA'
                )
            )
            handle_openssl_error(result)

            disabled_protocols = set(['SSLv2'])
            disabled_protocols |= (valid_protocols - self._protocols)
            for disabled_protocol in disabled_protocols:
                libssl.SSL_CTX_ctrl(
                    ssl_ctx,
                    LibsslConst.SSL_CTRL_OPTIONS,
                    _PROTOCOL_MAP[disabled_protocol],
                    null()
                )

            if self._extra_trust_roots:
                x509_store = libssl.SSL_CTX_get_cert_store(ssl_ctx)
                for cert in self._extra_trust_roots:
                    oscrypto_cert = load_certificate(cert)
                    result = libssl.X509_STORE_add_cert(
                        x509_store,
                        oscrypto_cert.x509
                    )
                    handle_openssl_error(result)

        except (Exception):
            if ssl_ctx:
                libssl.SSL_CTX_free(ssl_ctx)
            self._ssl_ctx = None
            raise

    def __del__(self):
        if self._ssl_ctx:
            libssl.SSL_CTX_free(self._ssl_ctx)
            self._ssl_ctx = None

        if self._ssl_session:
            libssl.SSL_SESSION_free(self._ssl_session)
            self._ssl_session = None


class TLSSocket(object):
    """
    A wrapper around a socket.socket that adds TLS
    """

    _socket = None
    _session = None

    _ssl = None
    _rbio = None
    _wbio = None
    _bio_write_buffer = None
    _read_buffer = None

    _decrypted_bytes = None

    _hostname = None

    _certificate = None
    _intermediates = None

    _protocol = None
    _cipher_suite = None
    _compression = None
    _session_id = None
    _session_ticket = None

    _local_closed = False

    @classmethod
    def wrap(cls, socket, hostname, session=None):
        """
        Takes an existing socket and adds TLS

        :param socket:
            A socket.socket object to wrap with TLS

        :param hostname:
            A unicode string of the hostname or IP the socket is connected to

        :param session:
            An existing TLSSession object to allow for session reuse, specific
            protocol or manual certificate validation

        :raises:
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library
        """

        if not isinstance(socket, socket_.socket):
            raise TypeError(pretty_message(
                '''
                socket must be an instance of socket.socket, not %s
                ''',
                type_name(socket)
            ))

        if not isinstance(hostname, str_cls):
            raise TypeError(pretty_message(
                '''
                hostname must be a unicode string, not %s
                ''',
                type_name(hostname)
            ))

        if session is not None and not isinstance(session, TLSSession):
            raise TypeError(pretty_message(
                '''
                session must be an instance of oscrypto.tls.TLSSession, not %s
                ''',
                type_name(session)
            ))

        new_socket = cls(None, None, session=session)
        new_socket._socket = socket
        new_socket._hostname = hostname
        new_socket._handshake()

        return new_socket

    def __init__(self, address, port, timeout=10, session=None):
        """
        :param address:
            A unicode string of the domain name or IP address to conenct to

        :param port:
            An integer of the port number to connect to

        :param timeout:
            An integer timeout to use for the socket

        :param session:
            An oscrypto.tls.TLSSession object to allow for session reuse and
            controlling the protocols and validation performed
        """

        self._decrypted_bytes = b''

        if address is None and port is None:
            self._socket = None

        else:
            if not isinstance(address, str_cls):
                raise TypeError(pretty_message(
                    '''
                    address must be a unicode string, not %s
                    ''',
                    type_name(address)
                ))

            if not isinstance(port, int_types):
                raise TypeError(pretty_message(
                    '''
                    port must be an integer, not %s
                    ''',
                    type_name(port)
                ))

            if timeout is not None and not isinstance(timeout, numbers.Number):
                raise TypeError(pretty_message(
                    '''
                    timeout must be a number, not %s
                    ''',
                    type_name(timeout)
                ))

            self._socket = socket_.create_connection((address, port), timeout)
            self._socket.settimeout(timeout)

        if session is None:
            session = TLSSession()

        elif not isinstance(session, TLSSession):
            raise TypeError(pretty_message(
                '''
                session must be an instance of oscrypto.tls.TLSSession, not %s
                ''',
                type_name(session)
            ))

        self._session = session

        if self._socket:
            self._hostname = address
            self._handshake()

    def _handshake(self):
        """
        Perform an initial TLS handshake
        """

        ssl = None
        rbio = None
        wbio = None

        try:
            ssl = libssl.SSL_new(self._session._ssl_ctx)
            if is_null(ssl):
                handle_openssl_error(0)

            mem_bio = libssl.BIO_s_mem()

            rbio = libssl.BIO_new(mem_bio)
            if is_null(rbio):
                handle_openssl_error(0)

            wbio = libssl.BIO_new(mem_bio)
            if is_null(wbio):
                handle_openssl_error(0)

            libssl.SSL_set_bio(ssl, rbio, wbio)

            utf8_domain = self._hostname.encode('utf-8')
            libssl.SSL_ctrl(
                ssl,
                LibsslConst.SSL_CTRL_SET_TLSEXT_HOSTNAME,
                LibsslConst.TLSEXT_NAMETYPE_host_name,
                utf8_domain
            )

            libssl.SSL_set_connect_state(ssl)

            if self._session._ssl_session:
                libssl.SSL_set_session(ssl, self._session._ssl_session)

            self._bio_write_buffer = buffer_from_bytes(8192)
            self._read_buffer = buffer_from_bytes(8192)

            handshake_server_bytes = b''
            handshake_client_bytes = b''

            self._ssl = ssl
            self._rbio = rbio
            self._wbio = wbio

            while True:
                result = libssl.SSL_do_handshake(self._ssl)
                handshake_client_bytes += self._raw_write(self._wbio)

                if result == 1:
                    break

                error = libssl.SSL_get_error(ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    chunk = self._raw_read(self._rbio)
                    if chunk == b'':
                        if handshake_server_bytes == b'':
                            raise_disconnection()
                        if detect_client_auth_request(handshake_server_bytes):
                            raise_client_auth()
                        raise_protocol_error(handshake_server_bytes)
                    handshake_server_bytes += chunk

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    handshake_client_bytes += self._raw_write(self._wbio)

                else:
                    info = peek_openssl_error()

                    if libcrypto_version_info < (1, 1):
                        dh_key_info = (
                            20,
                            LibsslConst.SSL_F_SSL3_CHECK_CERT_AND_ALGORITHM,
                            LibsslConst.SSL_R_DH_KEY_TOO_SMALL
                        )
                    else:
                        dh_key_info = (
                            20,
                            LibsslConst.SSL_F_TLS_PROCESS_SKE_DHE,
                            LibsslConst.SSL_R_DH_KEY_TOO_SMALL
                        )
                    if info == dh_key_info:
                        raise_dh_params()

                    if libcrypto_version_info < (1, 1):
                        unknown_protocol_info = (
                            20,
                            LibsslConst.SSL_F_SSL23_GET_SERVER_HELLO,
                            LibsslConst.SSL_R_UNKNOWN_PROTOCOL
                        )
                    else:
                        unknown_protocol_info = (
                            20,
                            LibsslConst.SSL_F_SSL3_GET_RECORD,
                            LibsslConst.SSL_R_WRONG_VERSION_NUMBER
                        )
                    if info == unknown_protocol_info:
                        raise_protocol_error(handshake_server_bytes)

                    handshake_error_info = (
                        20,
                        LibsslConst.SSL_F_SSL23_GET_SERVER_HELLO,
                        LibsslConst.SSL_R_SSLV3_ALERT_HANDSHAKE_FAILURE
                    )
                    if info == handshake_error_info:
                        raise_handshake()

                    handshake_failure_info = (
                        20,
                        LibsslConst.SSL_F_SSL3_READ_BYTES,
                        LibsslConst.SSL_R_SSLV3_ALERT_HANDSHAKE_FAILURE
                    )
                    if info == handshake_failure_info:
                        raise_client_auth()

                    if libcrypto_version_info < (1, 1):
                        cert_verify_failed_info = (
                            20,
                            LibsslConst.SSL_F_SSL3_GET_SERVER_CERTIFICATE,
                            LibsslConst.SSL_R_CERTIFICATE_VERIFY_FAILED
                        )
                    else:
                        cert_verify_failed_info = (
                            20,
                            LibsslConst.SSL_F_TLS_PROCESS_SERVER_CERTIFICATE,
                            LibsslConst.SSL_R_CERTIFICATE_VERIFY_FAILED
                        )

                    if info == cert_verify_failed_info:
                        verify_result = libssl.SSL_get_verify_result(ssl)
                        chain = extract_chain(handshake_server_bytes)

                        self_signed = False
                        time_invalid = False
                        no_issuer = False
                        cert = None
                        oscrypto_cert = None

                        if chain:
                            cert = chain[0]
                            oscrypto_cert = load_certificate(cert)
                            self_signed = oscrypto_cert.self_signed

                            issuer_error_codes = set([
                                LibsslConst.X509_V_ERR_DEPTH_ZERO_SELF_SIGNED_CERT,
                                LibsslConst.X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN,
                                LibsslConst.X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY
                            ])
                            if verify_result in issuer_error_codes:
                                no_issuer = not self_signed

                            time_error_codes = set([
                                LibsslConst.X509_V_ERR_CERT_HAS_EXPIRED,
                                LibsslConst.X509_V_ERR_CERT_NOT_YET_VALID
                            ])
                            time_invalid = verify_result in time_error_codes

                        if time_invalid:
                            raise_expired_not_yet_valid(cert)
                        if no_issuer:
                            raise_no_issuer(cert)
                        if self_signed:
                            raise_self_signed(cert)
                        if oscrypto_cert and oscrypto_cert.asn1.hash_algo in set(['md5', 'md2']):
                            raise_weak_signature(oscrypto_cert)
                        raise_verification(cert)

                    handle_openssl_error(0, TLSError)

            session_info = parse_session_info(
                handshake_server_bytes,
                handshake_client_bytes
            )
            self._protocol = session_info['protocol']
            self._cipher_suite = session_info['cipher_suite']
            self._compression = session_info['compression']
            self._session_id = session_info['session_id']
            self._session_ticket = session_info['session_ticket']

            if self._cipher_suite.find('_DHE_') != -1:
                dh_params_length = get_dh_params_length(handshake_server_bytes)
                if dh_params_length < 1024:
                    self.close()
                    ssl = None
                    rbio = None
                    wbio = None
                    raise_dh_params()

            # When saving the session for future requests, we use
            # SSL_get1_session() variant to increase the reference count. This
            # prevents the session from being freed when one connection closes
            # before another is opened. However, since we increase the ref
            # count, we also have to explicitly free any previous session.
            if self._session_id == 'new' or self._session_ticket == 'new':
                if self._session._ssl_session:
                    libssl.SSL_SESSION_free(self._session._ssl_session)
                self._session._ssl_session = libssl.SSL_get1_session(ssl)

            if not self._session._manual_validation:
                if self.certificate.hash_algo in set(['md5', 'md2']):
                    raise_weak_signature(self.certificate)

                # OpenSSL does not do hostname or IP address checking in the end
                # entity certificate, so we must perform that check
                if not self.certificate.is_valid_domain_ip(self._hostname):
                    raise_hostname(self.certificate, self._hostname)

        except (OSError, socket_.error):
            if ssl:
                libssl.SSL_free(ssl)
            # The BIOs are freed by SSL_free(), so we only need to free
            # them if for some reason SSL_free() was not called
            else:
                if rbio:
                    libssl.BIO_free(rbio)
                if wbio:
                    libssl.BIO_free(wbio)

            self._ssl = None
            self._rbio = None
            self._wbio = None
            self.close()

            raise

    def _raw_read(self, rbio):
        try:
            to_write = self._socket.recv(8192)
        except (socket_.error):
            to_write = b''
        output = to_write
        while to_write != b'':
            written = libssl.BIO_write(rbio, to_write, len(to_write))
            to_write = to_write[written:]
        return output

    def _raw_write(self, wbio):
        data_available = libssl.BIO_ctrl_pending(wbio)
        if data_available == 0:
            return b''
        to_read = min(8192, data_available)
        read = libssl.BIO_read(wbio, self._bio_write_buffer, to_read)
        to_write = bytes_from_buffer(self._bio_write_buffer, read)
        output = to_write
        while len(to_write):
            sent = self._socket.send(to_write)
            to_write = to_write[sent:]
            if len(to_write):
                self.select_write()
        return output

    def read(self, max_length):
        """
        Reads data from the TLS-wrapped socket

        :param max_length:
            The number of bytes to read - output may be less than this

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library

        :return:
            A byte string of the data read
        """

        if not isinstance(max_length, int_types):
            raise TypeError(pretty_message(
                '''
                max_length must be an integer, not %s
                ''',
                type_name(max_length)
            ))

        if self._ssl is None:
            # Even if the session is closed, we can use
            # buffered data to respond to read requests
            if self._decrypted_bytes != b'':
                output = self._decrypted_bytes
                self._decrypted_bytes = b''
                return output

            self._raise_closed()

        buffered_length = len(self._decrypted_bytes)

        # If we already have enough buffered data, just use that
        if buffered_length >= max_length:
            output = self._decrypted_bytes[0:max_length]
            self._decrypted_bytes = self._decrypted_bytes[max_length:]
            return output

        # Don't block if we have buffered data available, since it is ok to
        # return less than the max_length
        if buffered_length > 0 and not self.select_read(0):
            output = self._decrypted_bytes
            self._decrypted_bytes = b''
            return output

        # Only read enough to get the requested amount when
        # combined with buffered data
        to_read = max_length - len(self._decrypted_bytes)

        output = self._decrypted_bytes

        # The SSL_read() loop handles renegotiations, so we need to handle
        # requests for both reads and writes
        again = True
        while again:
            again = False
            result = libssl.SSL_read(self._ssl, self._read_buffer, to_read)
            self._raw_write(self._wbio)
            if result <= 0:

                error = libssl.SSL_get_error(self._ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    self._raw_read(self._rbio)
                    again = True
                    continue

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    self._raw_write(self._wbio)
                    again = True
                    continue

                elif error == LibsslConst.SSL_ERROR_ZERO_RETURN:
                    self.shutdown()
                    return b''

                else:
                    handle_openssl_error(0, TLSError)

            output += bytes_from_buffer(self._read_buffer, result)

        self._decrypted_bytes = output[max_length:]
        return output[0:max_length]

    def select_read(self, timeout=None):
        """
        Blocks until the socket is ready to be read from, or the timeout is hit

        :param timeout:
            A float - the period of time to wait for data to be read. None for
            no time limit.

        :return:
            A boolean - if data is ready to be read. Will only be False if
            timeout is not None.
        """

        # If we have buffered data, we consider a read possible
        if len(self._decrypted_bytes) > 0:
            return True

        read_ready, _, _ = select.select([self._socket], [], [], timeout)
        return len(read_ready) > 0

    def read_until(self, marker):
        """
        Reads data from the socket until a marker is found. Data read includes
        the marker.

        :param marker:
            A byte string or regex object from re.compile(). Used to determine
            when to stop reading.

        :return:
            A byte string of the data read, including the marker
        """

        if not isinstance(marker, byte_cls) and not isinstance(marker, re._pattern_type):
            raise TypeError(pretty_message(
                '''
                marker must be a byte string or compiled regex object, not %s
                ''',
                type_name(marker)
            ))

        output = b''

        is_regex = isinstance(marker, re._pattern_type)

        while True:
            if len(self._decrypted_bytes) > 0:
                chunk = self._decrypted_bytes
                self._decrypted_bytes = b''
            else:
                to_read = libssl.SSL_pending(self._ssl) or 8192
                chunk = self.read(to_read)

            output += chunk

            if is_regex:
                match = marker.search(chunk)
                if match is not None:
                    offset = len(output) - len(chunk)
                    end = offset + match.end()
                    break
            else:
                match = chunk.find(marker)
                if match != -1:
                    offset = len(output) - len(chunk)
                    end = offset + match + len(marker)
                    break

        self._decrypted_bytes = output[end:] + self._decrypted_bytes
        return output[0:end]

    def read_line(self):
        r"""
        Reads a line from the socket, including the line ending of "\r\n", "\r",
        or "\n"

        :return:
            A byte string of the next line from the socket
        """

        return self.read_until(_line_regex)

    def read_exactly(self, num_bytes):
        """
        Reads exactly the specified number of bytes from the socket

        :param num_bytes:
            An integer - the exact number of bytes to read

        :return:
            A byte string of the data that was read
        """

        output = b''
        remaining = num_bytes
        while remaining > 0:
            output += self.read(remaining)
            remaining = num_bytes - len(output)

        return output

    def write(self, data):
        """
        Writes data to the TLS-wrapped socket

        :param data:
            A byte string to write to the socket

        :raises:
            socket.socket - when a non-TLS socket error occurs
            oscrypto.errors.TLSError - when a TLS-related error occurs
            ValueError - when any of the parameters contain an invalid value
            TypeError - when any of the parameters are of the wrong type
            OSError - when an error is returned by the OS crypto library
        """

        if self._ssl is None:
            self._raise_closed()

        data_len = len(data)
        while data_len:
            result = libssl.SSL_write(self._ssl, data, data_len)
            self._raw_write(self._wbio)
            if result <= 0:

                error = libssl.SSL_get_error(self._ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    self._raw_read(self._rbio)
                    continue

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    self._raw_write(self._wbio)
                    continue

                elif error == LibsslConst.SSL_ERROR_ZERO_RETURN:
                    self.shutdown()
                    return

                else:
                    handle_openssl_error(0, TLSError)

            data = data[result:]
            data_len = len(data)

    def select_write(self, timeout=None):
        """
        Blocks until the socket is ready to be written to, or the timeout is hit

        :param timeout:
            A float - the period of time to wait for the socket to be ready to
            written to. None for no time limit.

        :return:
            A boolean - if the socket is ready for writing. Will only be False
            if timeout is not None.
        """

        _, write_ready, _ = select.select([], [self._socket], [], timeout)
        return len(write_ready) > 0

    def shutdown(self):
        """
        Shuts down the TLS session and then shuts down the underlying socket
        """

        if self._ssl is None:
            return

        while True:
            result = libssl.SSL_shutdown(self._ssl)
            self._raw_write(self._wbio)

            if result >= 0:
                break
            if result < 0:
                error = libssl.SSL_get_error(self._ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    self._raw_read(self._rbio)
                    continue

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    self._raw_write(self._wbio)
                    continue

                else:
                    handle_openssl_error(0, TLSError)

        self._local_closed = True

        libssl.SSL_free(self._ssl)
        self._ssl = None
        # BIOs are freed by SSL_free()
        self._rbio = None
        self._wbio = None

        try:
            self._socket.shutdown(socket_.SHUT_RDWR)
        except (socket_.error):
            pass

    def close(self):
        """
        Shuts down the TLS session and socket and forcibly closes it
        """

        try:
            self.shutdown()

        finally:
            if self._socket:
                try:
                    self._socket.close()
                except (socket_.error):
                    pass
                self._socket = None

    def _read_certificates(self):
        """
        Reads end-entity and intermediate certificate information from the
        TLS session
        """

        stack_pointer = libssl.SSL_get_peer_cert_chain(self._ssl)
        if is_null(stack_pointer):
            handle_openssl_error(0, TLSError)

        if libcrypto_version_info < (1, 1):
            number_certs = libssl.sk_num(stack_pointer)
        else:
            number_certs = libssl.OPENSSL_sk_num(stack_pointer)

        self._intermediates = []

        for index in range(0, number_certs):
            if libcrypto_version_info < (1, 1):
                x509_ = libssl.sk_value(stack_pointer, index)
            else:
                x509_ = libssl.OPENSSL_sk_value(stack_pointer, index)
            buffer_size = libcrypto.i2d_X509(x509_, null())
            cert_buffer = buffer_from_bytes(buffer_size)
            cert_pointer = buffer_pointer(cert_buffer)
            cert_length = libcrypto.i2d_X509(x509_, cert_pointer)
            handle_openssl_error(cert_length)
            cert_data = bytes_from_buffer(cert_buffer, cert_length)

            cert = x509.Certificate.load(cert_data)

            if index == 0:
                self._certificate = cert
            else:
                self._intermediates.append(cert)

    def _raise_closed(self):
        """
        Raises an exception describing if the local or remote end closed the
        connection
        """

        if self._local_closed:
            message = 'The connection was already closed'
        else:
            message = 'The remote end closed the connection'
        raise TLSError(message)

    @property
    def certificate(self):
        """
        An asn1crypto.x509.Certificate object of the end-entity certificate
        presented by the server
        """

        if self._ssl is None:
            self._raise_closed()

        if self._certificate is None:
            self._read_certificates()

        return self._certificate

    @property
    def intermediates(self):
        """
        A list of asn1crypto.x509.Certificate objects that were presented as
        intermediates by the server
        """

        if self._ssl is None:
            self._raise_closed()

        if self._certificate is None:
            self._read_certificates()

        return self._intermediates

    @property
    def cipher_suite(self):
        """
        A unicode string of the IANA cipher suite name of the negotiated
        cipher suite
        """

        return self._cipher_suite

    @property
    def protocol(self):
        """
        A unicode string of: "TLSv1.2", "TLSv1.1", "TLSv1", "SSLv3"
        """

        return self._protocol

    @property
    def compression(self):
        """
        A boolean if compression is enabled
        """

        return self._compression

    @property
    def session_id(self):
        """
        A unicode string of "new" or "reused" or None for no ticket
        """

        return self._session_id

    @property
    def session_ticket(self):
        """
        A unicode string of "new" or "reused" or None for no ticket
        """

        return self._session_ticket

    @property
    def session(self):
        """
        The oscrypto.tls.TLSSession object used for this connection
        """

        return self._session

    @property
    def hostname(self):
        """
        A unicode string of the TLS server domain name or IP address
        """

        return self._hostname

    @property
    def socket(self):
        """
        The underlying socket.socket connection
        """

        if self._ssl is None:
            self._raise_closed()

        return self._socket

    def __del__(self):
        self.close()
