from __future__ import absolute_import

import cgi
import email.utils
import getpass
import json
import logging
import mimetypes
import os
import platform
import re
import shutil
import sys

from pip._vendor import requests, six, urllib3
from pip._vendor.cachecontrol import CacheControlAdapter
from pip._vendor.cachecontrol.caches import FileCache
from pip._vendor.lockfile import LockError
from pip._vendor.requests.adapters import BaseAdapter, HTTPAdapter
from pip._vendor.requests.auth import AuthBase, HTTPBasicAuth
from pip._vendor.requests.models import CONTENT_CHUNK_SIZE, Response
from pip._vendor.requests.structures import CaseInsensitiveDict
from pip._vendor.requests.utils import get_netrc_auth
# NOTE: XMLRPC Client is not annotated in typeshed as on 2017-07-17, which is
#       why we ignore the type on this import
from pip._vendor.six.moves import xmlrpc_client  # type: ignore
from pip._vendor.six.moves.urllib import parse as urllib_parse
from pip._vendor.six.moves.urllib import request as urllib_request
from pip._vendor.six.moves.urllib.parse import unquote as urllib_unquote
from pip._vendor.urllib3.util import IS_PYOPENSSL

import pip
from pip._internal.exceptions import HashMismatch, InstallationError
from pip._internal.locations import write_delete_marker_file
from pip._internal.models.index import PyPI
from pip._internal.utils.encoding import auto_decode
from pip._internal.utils.filesystem import check_path_owner
from pip._internal.utils.glibc import libc_ver
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import (
    ARCHIVE_EXTENSIONS, ask_path_exists, backup_dir, call_subprocess, consume,
    display_path, format_size, get_installed_version, rmtree, splitext,
    unpack_file,
)
from pip._internal.utils.setuptools_build import SETUPTOOLS_SHIM
from pip._internal.utils.temp_dir import TempDirectory
from pip._internal.utils.ui import DownloadProgressProvider
from pip._internal.vcs import vcs

try:
    import ssl  # noqa
except ImportError:
    ssl = None

HAS_TLS = (ssl is not None) or IS_PYOPENSSL

__all__ = ['get_file_content',
           'is_url', 'url_to_path', 'path_to_url',
           'is_archive_file', 'unpack_vcs_link',
           'unpack_file_url', 'is_vcs_url', 'is_file_url',
           'unpack_http_url', 'unpack_url']


logger = logging.getLogger(__name__)


class TUFInTotoError(Exception):

    def __init__(self, target_relpath):
        self.target_relpath = target_relpath

    def __str__(self):
        return "Unexpected tuf-in-toto error for {}!"\
               .format(self.target_relpath)


class NoInTotoLinkMetadataFound(TUFInTotoError):

    def __str__(self):
        return "in-toto link metadata expected, "\
               "but not found for {}!".format(self.target_relpath)


class NoInTotoRootLayoutPublicKeysFound(TUFInTotoError):

    def __str__(self):
        return "in-toto root layout public keys expected, "\
               "but not found for {}!".format(self.target_relpath)


class TUFDownloader:

    def __init__(self, path_to_tuf_config_file):
        '''
        This object must be given a TUF configuration file, an example of which
        follows, and explanations of which are given in the rest of this
        function:

        {
          "download_in_toto_metadata": false,
          "enable_logging": false,
          "repositories_dir": "repositories",
          "repository_dir": "repository-name",
          "target_path_patterns": ["^.*/(wheels/.*\\.whl)$"],
          "repository_mirrors": {
            "mirror-name": {
              "url_prefix": "https://example.com",
              "metadata_path": "metadata",
              "targets_path": "targets",
              "confined_target_dirs": [""]
            }
          }
        }
        '''

        with open(path_to_tuf_config_file) as tuf_config_file:
            tuf_config = json.load(tuf_config_file)

        # NOTE: The directory where TUF metadata for *all* repositories are
        # kept.
        # If it is an absolute directory, then we will use that directly.
        if os.path.isabs(tuf_config['repositories_dir']):
            tuf.settings.repositories_directory = \
                                                tuf_config['repositories_dir']
        # Otherwise, if it is a relative directory, then we will assume that
        # it is stored *UNDER* the directory containing the TUF configuration
        # file itself.
        else:
            tuf.settings.repositories_directory = os.path.join(
                os.path.dirname(path_to_tuf_config_file),
                tuf_config['repositories_dir']
            )

        # NOTE: By default, we turn off TUF logging, and use the pip log
        # instead. You may turn toggle this behaviour using this flag in the
        # TUF configuration file. Alternatively, you may also toggle this
        # behaviour using an environment variable (TUF_ENABLE_LOGGING).
        enable_logging = tuf_config.get('enable_logging', False) or \
                         os.environ.get('TUF_ENABLE_LOGGING', False)

        if enable_logging:
            # NOTE: Also set TUF output to DEBUG and above.
            logging.getLogger("tuf").setLevel(logging.DEBUG)

            # Also set verbose, non-quiet in-toto logging.
            # https://github.com/in-toto/in-toto/blob/8eb8eab8c94f47e67a24b5e7d56f4519092dd9d2/in_toto/in_toto_verify.py#L205
            logging.getLogger("in_toto").setLevelVerboseOrQuiet(True, False)

        # NOTE: The directory where the targets for *this* repository is
        # cached. We hard-code this keep this to a subdirectory dedicated to
        # this repository.
        self.__targets_dir = os.path.join(tuf.settings.repositories_directory,
                                          tuf_config['repository_dir'],
                                          'targets')

        # NOTE: A list of TUF target path patterns to match using Python
        # regular expressions. *ONLY* these matching targets will be downloaded
        # using TUF from this repository. Each pattern MUST have exactly one
        # group used to match and download the target.
        # E.g.: ["^.*/(wheels/.*\\.whl)$"]
        self.__target_path_patterns = tuf_config['target_path_patterns']

        # NOTE: Build a TUF updater which stores metadata in (1) the given
        # directory, and (2) uses the following mirror configuration,
        # respectively.
        # https://github.com/theupdateframework/tuf/blob/aa2ab218f22d8682e03c992ea98f88efd155cffd/tuf/client/updater.py#L628-L683
        # NOTE: This updater will store files under:
        # os.path.join(tuf.settings.repositories_directory,
        #              tuf_config['repository_dir'])
        self.__updater = Updater(tuf_config['repository_dir'],
                                 tuf_config['repository_mirrors'])

        # NOTE: A flag, False by default, to signal whether we should download
        # and verify in-toto metadata. You may turn toggle this behaviour using
        # this flag in the TUF configuration file. Alternatively, you may also
        # toggle this behaviour using an environment variable
        # (TUF_DOWNLOAD_IN_TOTO_METADATA).
        self.__DOWNLOAD_IN_TOTO_METADATA = \
                        tuf_config.get('download_in_toto_metadata', False) or \
                        os.environ.get('TUF_DOWNLOAD_IN_TOTO_METADATA', False)


        # NOTE: A module with a function that substitutes parameters for
        # in-toto inspections. The function is expected to be called
        # "substitute", and takes one parameter, target_relpath, that specifies
        # the relative target path of the given Python package. The function is
        # expected to return a dictionary which maps parameter names to
        # parameter values, so that in-toto can substitute these parameters in
        # order to perform a successful inspection.
        if self.__DOWNLOAD_IN_TOTO_METADATA:
            # The module is expected to live here.
            from pip._internal.parameters import substitute
            self.__substitute_parameters = substitute

        # NOTE: Update to the latest top-level role metadata only ONCE, so that
        # we use the same consistent snapshot to download targets.
        self.__updater.refresh()

    def __download_in_toto_metadata(self, target):
        # A list to collect where in-toto metadata targets live.
        target_relpaths = []

        fileinfo = target.get('fileinfo')

        if fileinfo:
            custom = fileinfo.get('custom')

            if custom:
                in_toto_metadata = custom.get('in-toto')

                # A long but safe way of checking whether there is any in-toto
                # metadata embeddeed in an expected, hard-coded location.
                if in_toto_metadata:

                    for target_relpath in in_toto_metadata:
                        # Download the in-toto layout / link metadata file
                        # using TUF, which, among other things, prevents
                        # mix-and-match attacks by MitM attackers, and rollback
                        # attacks even by attackers who control the repository:
                        # https://www.usenix.org/conference/atc17/technical-sessions/presentation/kuppusamy
                        self._get_target(target_relpath,
                                         # NOTE: Avoid recursively downloading
                                         # in-toto metadata for in-toto
                                         # metadata themselves, and so on ad
                                         # infinitum.
                                         download_in_toto_metadata=False)

                        # Add this file to the growing collection of where
                        # in-toto metadata live.
                        target_relpaths.append(target_relpath)

        # Return list of where in-toto metadata files live.
        return target_relpaths

    # NOTE: We assume that all the public keys needed to verify any in-toto
    # root layout, or sublayout, metadata file has been directly signed by the
    # top-level TUF targets role using *OFFLINE* keys. This is a reasonable
    # assumption, as TUF does not offer meaningful security guarantees if _ALL_
    # targets were signed using _online_ keys.
    def __update_in_toto_layout_pubkeys(self):
        target_relpaths = []
        targets = self.__updater.targets_of_role('targets')

        for target in targets:
            target_relpath = target['filepath']

            # Download this target only if it _looks_ like a public key.
            if target_relpath.endswith('.pub'):
                self._get_target(target_relpath,
                                 download_in_toto_metadata=False)
                target_relpaths.append(target_relpath)

        return target_relpaths

    # TODO: Consider borrowing techniques used in containers to restrict CPU,
    # RAM, disk space, and so on for the inspection.
    def __verify_in_toto_metadata(self, target_relpath,
                                  in_toto_metadata_relpaths, pubkey_relpaths):
        # Make a temporary directory.
        tempdir = tempfile.mkdtemp()
        prev_cwd = os.getcwd()

        try:
            # Copy files over into temp dir.
            rel_paths = [target_relpath] + in_toto_metadata_relpaths + \
                    pubkey_relpaths
            for rel_path in rel_paths:
                # Don't confuse Python with any leading path separator.
                rel_path = rel_path.strip('/')
                abs_path = os.path.join(self.__targets_dir, rel_path)
                shutil.copy(abs_path, tempdir)

            # Switch to the temp dir.
            # FIXME: Consider using chroot.
            os.chdir(tempdir)
            # Get a list of all the layouts.
            layout_relpaths = glob.glob('*.layout')

            # Iterate over layouts.
            for layout_relpath in layout_relpaths:
                # Load the layout and public keys.
                layout = Metablock.load(layout_relpath)
                pubkeys = glob.glob('*.pub')
                layout_key_dict = \
                             import_public_keys_from_files_as_dict(pubkeys)
                # Verify and inspect.
                params = self.__substitute_parameters(target_relpath)
                verifylib.in_toto_verify(layout, layout_key_dict,
                                         substitution_parameters=params)
                logger.info('in-toto verified {}'.format(target_relpath))
        except:
            logger.exception('in-toto failed to verify {}'\
                             .format(target_relpath))
            raise
        else:
            os.chdir(prev_cwd)
            # Delete temp dir.
            shutil.rmtree(tempdir)
        finally:
            os.chdir(prev_cwd)

    def __download_and_verify_in_toto_metadata(self, target, target_relpath):
	in_toto_metadata_relpaths = self.__download_in_toto_metadata(target)

        if not len(in_toto_metadata_relpaths):
            raise NoInTotoLinkMetadataFound(target_relpath)

        else:
            pubkey_relpaths = self.__update_in_toto_layout_pubkeys()

            if not len(pubkey_relpaths):
                raise NoInTotoRootLayoutPublicKeysFound(target_relpath)

            else:
                self.__verify_in_toto_metadata(target_relpath,
                                               in_toto_metadata_relpaths,
                                               pubkey_relpaths)

    def _get_target(self, target_relpath, download_in_toto_metadata=True):
        target = self.__updater.get_one_valid_targetinfo(target_relpath)
        updated_targets = self.__updater.updated_targets((target,),
                                                         self.__targets_dir)

        # Either the target has not been updated...
        if not len(updated_targets):
            logger.debug('{} has not been updated'.format(target_relpath))
        # or, it has been updated, in which case...
        else:
            # First, we use TUF to download and verify the target.
            assert len(updated_targets) == 1
            updated_target = updated_targets[0]
	    assert updated_target == target
            self.__updater.download_target(updated_target, self.__targets_dir)

        logger.info('TUF verified {}'.format(target_relpath))

	# Next, we use in-toto to verify the supply chain of the target.
	# NOTE: We use a flag to avoid recursively downloading in-toto
	# metadata for in-toto metadata themselves, and so on ad infinitum.
	# NOTE: We use a global flag (self.__DOWNLOAD_IN_TOTO_METADATA) for
	# coarse-grained control, and a local flag
	# (download_in_toto_metadata) for fine-grained control (e.g.,
	# override global flag, even when switched on, for HTML files).
	# TODO: When it comes to HTML files, we should just verify.
	# All other files, presumably packages, should also be
	# inspected.
	# TODO: Ideally, shouldn't we check that the simple index and
	# any corresponding wheel were actually built in the same
	# pipeline run?
	if self.__DOWNLOAD_IN_TOTO_METADATA and \
	   download_in_toto_metadata and \
	   not target_relpath.endswith('.html'):
	    self.__download_and_verify_in_toto_metadata(target, target_relpath)
	else:
	    logger.warning('Switched off in-toto verification for {}'\
			   .format(target_relpath))

        target_path = os.path.join(self.__targets_dir, target_relpath)
        return target_path

    def match(self, url):
        for pattern in self.__target_path_patterns:
            match = re.match(pattern, url)
            if match:
                logger.debug('{} matched {}'.format(url, pattern))
                return match.group(1)
            else:
                logger.debug('{} mismatched {}'.format(url, pattern))
        return None

    def download(self, target_relpath, dest_dir, dest_filename):
        target_path = self._get_target(target_relpath)
        from_path = os.path.join(dest_dir, dest_filename)
        shutil.copyfile(target_path, from_path)
        content_type = mimetypes.guess_type(target_relpath)
        return from_path, content_type


if 'TUF_CONFIG_FILE' in os.environ:
    import glob
    import tempfile

    # We always turn off TUF logging.
    import tuf.settings
    tuf.settings.ENABLE_FILE_LOGGING = False
    # By default, set the TUF console logging level to >= CRITICAL.
    import tuf.log
    logging.getLogger("tuf").setLevel(logging.CRITICAL)

    # Import what we need from TUF.
    from tuf.client.updater import Updater

    # Also set non-verbose, quiet in-toto logging.
    import in_toto.log
    logging.getLogger("in_toto").setLevelVerboseOrQuiet(False, True)

    # Import what we need from in-toto.
    from in_toto import verifylib
    from in_toto.models.metadata import Metablock
    from in_toto.util import import_public_keys_from_files_as_dict

    tuf_downloader = TUFDownloader(os.environ['TUF_CONFIG_FILE'])
else:
    tuf_downloader = None


def user_agent():
    """
    Return a string representing the user agent.
    """
    data = {
        "installer": {"name": "pip", "version": pip.__version__},
        "python": platform.python_version(),
        "implementation": {
            "name": platform.python_implementation(),
        },
    }

    if data["implementation"]["name"] == 'CPython':
        data["implementation"]["version"] = platform.python_version()
    elif data["implementation"]["name"] == 'PyPy':
        if sys.pypy_version_info.releaselevel == 'final':
            pypy_version_info = sys.pypy_version_info[:3]
        else:
            pypy_version_info = sys.pypy_version_info
        data["implementation"]["version"] = ".".join(
            [str(x) for x in pypy_version_info]
        )
    elif data["implementation"]["name"] == 'Jython':
        # Complete Guess
        data["implementation"]["version"] = platform.python_version()
    elif data["implementation"]["name"] == 'IronPython':
        # Complete Guess
        data["implementation"]["version"] = platform.python_version()

    if sys.platform.startswith("linux"):
        from pip._vendor import distro
        distro_infos = dict(filter(
            lambda x: x[1],
            zip(["name", "version", "id"], distro.linux_distribution()),
        ))
        libc = dict(filter(
            lambda x: x[1],
            zip(["lib", "version"], libc_ver()),
        ))
        if libc:
            distro_infos["libc"] = libc
        if distro_infos:
            data["distro"] = distro_infos

    if sys.platform.startswith("darwin") and platform.mac_ver()[0]:
        data["distro"] = {"name": "macOS", "version": platform.mac_ver()[0]}

    if platform.system():
        data.setdefault("system", {})["name"] = platform.system()

    if platform.release():
        data.setdefault("system", {})["release"] = platform.release()

    if platform.machine():
        data["cpu"] = platform.machine()

    if HAS_TLS:
        data["openssl_version"] = ssl.OPENSSL_VERSION

    setuptools_version = get_installed_version("setuptools")
    if setuptools_version is not None:
        data["setuptools_version"] = setuptools_version

    return "{data[installer][name]}/{data[installer][version]} {json}".format(
        data=data,
        json=json.dumps(data, separators=(",", ":"), sort_keys=True),
    )


class MultiDomainBasicAuth(AuthBase):

    def __init__(self, prompting=True):
        self.prompting = prompting
        self.passwords = {}

    def __call__(self, req):
        parsed = urllib_parse.urlparse(req.url)

        # Get the netloc without any embedded credentials
        netloc = parsed.netloc.rsplit("@", 1)[-1]

        # Set the url of the request to the url without any credentials
        req.url = urllib_parse.urlunparse(parsed[:1] + (netloc,) + parsed[2:])

        # Use any stored credentials that we have for this netloc
        username, password = self.passwords.get(netloc, (None, None))

        # Extract credentials embedded in the url if we have none stored
        if username is None:
            username, password = self.parse_credentials(parsed.netloc)

        # Get creds from netrc if we still don't have them
        if username is None and password is None:
            netrc_auth = get_netrc_auth(req.url)
            username, password = netrc_auth if netrc_auth else (None, None)

        if username or password:
            # Store the username and password
            self.passwords[netloc] = (username, password)

            # Send the basic auth with this request
            req = HTTPBasicAuth(username or "", password or "")(req)

        # Attach a hook to handle 401 responses
        req.register_hook("response", self.handle_401)

        return req

    def handle_401(self, resp, **kwargs):
        # We only care about 401 responses, anything else we want to just
        #   pass through the actual response
        if resp.status_code != 401:
            return resp

        # We are not able to prompt the user so simply return the response
        if not self.prompting:
            return resp

        parsed = urllib_parse.urlparse(resp.url)

        # Prompt the user for a new username and password
        username = six.moves.input("User for %s: " % parsed.netloc)
        password = getpass.getpass("Password: ")

        # Store the new username and password to use for future requests
        if username or password:
            self.passwords[parsed.netloc] = (username, password)

        # Consume content and release the original connection to allow our new
        #   request to reuse the same one.
        resp.content
        resp.raw.release_conn()

        # Add our new username and password to the request
        req = HTTPBasicAuth(username or "", password or "")(resp.request)

        # Send our new request
        new_resp = resp.connection.send(req, **kwargs)
        new_resp.history.append(resp)

        return new_resp

    def parse_credentials(self, netloc):
        if "@" in netloc:
            userinfo = netloc.rsplit("@", 1)[0]
            if ":" in userinfo:
                user, pwd = userinfo.split(":", 1)
                return (urllib_unquote(user), urllib_unquote(pwd))
            return urllib_unquote(userinfo), None
        return None, None


class LocalFSAdapter(BaseAdapter):

    def send(self, request, stream=None, timeout=None, verify=None, cert=None,
             proxies=None):
        pathname = url_to_path(request.url)

        resp = Response()
        resp.status_code = 200
        resp.url = request.url

        try:
            stats = os.stat(pathname)
        except OSError as exc:
            resp.status_code = 404
            resp.raw = exc
        else:
            modified = email.utils.formatdate(stats.st_mtime, usegmt=True)
            content_type = mimetypes.guess_type(pathname)[0] or "text/plain"
            resp.headers = CaseInsensitiveDict({
                "Content-Type": content_type,
                "Content-Length": stats.st_size,
                "Last-Modified": modified,
            })

            resp.raw = open(pathname, "rb")
            resp.close = resp.raw.close

        return resp

    def close(self):
        pass


class SafeFileCache(FileCache):
    """
    A file based cache which is safe to use even when the target directory may
    not be accessible or writable.
    """

    def __init__(self, *args, **kwargs):
        super(SafeFileCache, self).__init__(*args, **kwargs)

        # Check to ensure that the directory containing our cache directory
        # is owned by the user current executing pip. If it does not exist
        # we will check the parent directory until we find one that does exist.
        # If it is not owned by the user executing pip then we will disable
        # the cache and log a warning.
        if not check_path_owner(self.directory):
            logger.warning(
                "The directory '%s' or its parent directory is not owned by "
                "the current user and the cache has been disabled. Please "
                "check the permissions and owner of that directory. If "
                "executing pip with sudo, you may want sudo's -H flag.",
                self.directory,
            )

            # Set our directory to None to disable the Cache
            self.directory = None

    def get(self, *args, **kwargs):
        # If we don't have a directory, then the cache should be a no-op.
        if self.directory is None:
            return

        try:
            return super(SafeFileCache, self).get(*args, **kwargs)
        except (LockError, OSError, IOError):
            # We intentionally silence this error, if we can't access the cache
            # then we can just skip caching and process the request as if
            # caching wasn't enabled.
            pass

    def set(self, *args, **kwargs):
        # If we don't have a directory, then the cache should be a no-op.
        if self.directory is None:
            return

        try:
            return super(SafeFileCache, self).set(*args, **kwargs)
        except (LockError, OSError, IOError):
            # We intentionally silence this error, if we can't access the cache
            # then we can just skip caching and process the request as if
            # caching wasn't enabled.
            pass

    def delete(self, *args, **kwargs):
        # If we don't have a directory, then the cache should be a no-op.
        if self.directory is None:
            return

        try:
            return super(SafeFileCache, self).delete(*args, **kwargs)
        except (LockError, OSError, IOError):
            # We intentionally silence this error, if we can't access the cache
            # then we can just skip caching and process the request as if
            # caching wasn't enabled.
            pass


class InsecureHTTPAdapter(HTTPAdapter):

    def cert_verify(self, conn, url, verify, cert):
        conn.cert_reqs = 'CERT_NONE'
        conn.ca_certs = None


class PipSession(requests.Session):

    timeout = None

    def __init__(self, *args, **kwargs):
        retries = kwargs.pop("retries", 0)
        cache = kwargs.pop("cache", None)
        insecure_hosts = kwargs.pop("insecure_hosts", [])

        super(PipSession, self).__init__(*args, **kwargs)

        # Attach our User Agent to the request
        self.headers["User-Agent"] = user_agent()

        # Attach our Authentication handler to the session
        self.auth = MultiDomainBasicAuth()

        # Create our urllib3.Retry instance which will allow us to customize
        # how we handle retries.
        retries = urllib3.Retry(
            # Set the total number of retries that a particular request can
            # have.
            total=retries,

            # A 503 error from PyPI typically means that the Fastly -> Origin
            # connection got interrupted in some way. A 503 error in general
            # is typically considered a transient error so we'll go ahead and
            # retry it.
            # A 500 may indicate transient error in Amazon S3
            # A 520 or 527 - may indicate transient error in CloudFlare
            status_forcelist=[500, 503, 520, 527],

            # Add a small amount of back off between failed requests in
            # order to prevent hammering the service.
            backoff_factor=0.25,
        )

        # We want to _only_ cache responses on securely fetched origins. We do
        # this because we can't validate the response of an insecurely fetched
        # origin, and we don't want someone to be able to poison the cache and
        # require manual eviction from the cache to fix it.
        if cache:
            secure_adapter = CacheControlAdapter(
                cache=SafeFileCache(cache, use_dir_lock=True),
                max_retries=retries,
            )
        else:
            secure_adapter = HTTPAdapter(max_retries=retries)

        # Our Insecure HTTPAdapter disables HTTPS validation. It does not
        # support caching (see above) so we'll use it for all http:// URLs as
        # well as any https:// host that we've marked as ignoring TLS errors
        # for.
        insecure_adapter = InsecureHTTPAdapter(max_retries=retries)

        self.mount("https://", secure_adapter)
        self.mount("http://", insecure_adapter)

        # Enable file:// urls
        self.mount("file://", LocalFSAdapter())

        # We want to use a non-validating adapter for any requests which are
        # deemed insecure.
        for host in insecure_hosts:
            self.mount("https://{}/".format(host), insecure_adapter)

    def request(self, method, url, *args, **kwargs):
        # Allow setting a default timeout on a session
        kwargs.setdefault("timeout", self.timeout)

        # Dispatch the actual request
        return super(PipSession, self).request(method, url, *args, **kwargs)


def get_file_content(url, comes_from=None, session=None):
    """Gets the content of a file; it may be a filename, file: URL, or
    http: URL.  Returns (location, content).  Content is unicode.

    :param url:         File path or url.
    :param comes_from:  Origin description of requirements.
    :param session:     Instance of pip.download.PipSession.
    """
    if session is None:
        raise TypeError(
            "get_file_content() missing 1 required keyword argument: 'session'"
        )

    match = _scheme_re.search(url)
    if match:
        scheme = match.group(1).lower()
        if (scheme == 'file' and comes_from and
                comes_from.startswith('http')):
            raise InstallationError(
                'Requirements file %s references URL %s, which is local'
                % (comes_from, url))
        if scheme == 'file':
            path = url.split(':', 1)[1]
            path = path.replace('\\', '/')
            match = _url_slash_drive_re.match(path)
            if match:
                path = match.group(1) + ':' + path.split('|', 1)[1]
            path = urllib_parse.unquote(path)
            if path.startswith('/'):
                path = '/' + path.lstrip('/')
            url = path
        else:
            # FIXME: catch some errors
            resp = session.get(url)
            resp.raise_for_status()
            return resp.url, resp.text
    try:
        with open(url, 'rb') as f:
            content = auto_decode(f.read())
    except IOError as exc:
        raise InstallationError(
            'Could not open requirements file: %s' % str(exc)
        )
    return url, content


_scheme_re = re.compile(r'^(http|https|file):', re.I)
_url_slash_drive_re = re.compile(r'/*([a-z])\|', re.I)


def is_url(name):
    """Returns true if the name looks like a URL"""
    if ':' not in name:
        return False
    scheme = name.split(':', 1)[0].lower()
    return scheme in ['http', 'https', 'file', 'ftp'] + vcs.all_schemes


def url_to_path(url):
    """
    Convert a file: URL to a path.
    """
    assert url.startswith('file:'), (
        "You can only turn file: urls into filenames (not %r)" % url)

    _, netloc, path, _, _ = urllib_parse.urlsplit(url)

    # if we have a UNC path, prepend UNC share notation
    if netloc:
        netloc = '\\\\' + netloc

    path = urllib_request.url2pathname(netloc + path)
    return path


def path_to_url(path):
    """
    Convert a path to a file: URL.  The path will be made absolute and have
    quoted path parts.
    """
    path = os.path.normpath(os.path.abspath(path))
    url = urllib_parse.urljoin('file:', urllib_request.pathname2url(path))
    return url


def is_archive_file(name):
    """Return True if `name` is a considered as an archive file."""
    ext = splitext(name)[1].lower()
    if ext in ARCHIVE_EXTENSIONS:
        return True
    return False


def unpack_vcs_link(link, location):
    vcs_backend = _get_used_vcs_backend(link)
    vcs_backend.unpack(location)


def _get_used_vcs_backend(link):
    for backend in vcs.backends:
        if link.scheme in backend.schemes:
            vcs_backend = backend(link.url)
            return vcs_backend


def is_vcs_url(link):
    return bool(_get_used_vcs_backend(link))


def is_file_url(link):
    return link.url.lower().startswith('file:')


def is_dir_url(link):
    """Return whether a file:// Link points to a directory.

    ``link`` must not have any other scheme but file://. Call is_file_url()
    first.

    """
    link_path = url_to_path(link.url_without_fragment)
    return os.path.isdir(link_path)


def _progress_indicator(iterable, *args, **kwargs):
    return iterable


def _download_url(resp, link, content_file, hashes, progress_bar):
    try:
        total_length = int(resp.headers['content-length'])
    except (ValueError, KeyError, TypeError):
        total_length = 0

    cached_resp = getattr(resp, "from_cache", False)
    if logger.getEffectiveLevel() > logging.INFO:
        show_progress = False
    elif cached_resp:
        show_progress = False
    elif total_length > (40 * 1000):
        show_progress = True
    elif not total_length:
        show_progress = True
    else:
        show_progress = False

    show_url = link.show_url

    def resp_read(chunk_size):
        try:
            # Special case for urllib3.
            for chunk in resp.raw.stream(
                    chunk_size,
                    # We use decode_content=False here because we don't
                    # want urllib3 to mess with the raw bytes we get
                    # from the server. If we decompress inside of
                    # urllib3 then we cannot verify the checksum
                    # because the checksum will be of the compressed
                    # file. This breakage will only occur if the
                    # server adds a Content-Encoding header, which
                    # depends on how the server was configured:
                    # - Some servers will notice that the file isn't a
                    #   compressible file and will leave the file alone
                    #   and with an empty Content-Encoding
                    # - Some servers will notice that the file is
                    #   already compressed and will leave the file
                    #   alone and will add a Content-Encoding: gzip
                    #   header
                    # - Some servers won't notice anything at all and
                    #   will take a file that's already been compressed
                    #   and compress it again and set the
                    #   Content-Encoding: gzip header
                    #
                    # By setting this not to decode automatically we
                    # hope to eliminate problems with the second case.
                    decode_content=False):
                yield chunk
        except AttributeError:
            # Standard file-like object.
            while True:
                chunk = resp.raw.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def written_chunks(chunks):
        for chunk in chunks:
            content_file.write(chunk)
            yield chunk

    progress_indicator = _progress_indicator

    if link.netloc == PyPI.netloc:
        url = show_url
    else:
        url = link.url_without_fragment

    if show_progress:  # We don't show progress on cached responses
        progress_indicator = DownloadProgressProvider(progress_bar,
                                                      max=total_length)
        if total_length:
            logger.info("Downloading %s (%s)", url, format_size(total_length))
        else:
            logger.info("Downloading %s", url)
    elif cached_resp:
        logger.info("Using cached %s", url)
    else:
        logger.info("Downloading %s", url)

    logger.debug('Downloading from URL %s', link)

    downloaded_chunks = written_chunks(
        progress_indicator(
            resp_read(CONTENT_CHUNK_SIZE),
            CONTENT_CHUNK_SIZE
        )
    )
    if hashes:
        hashes.check_against_chunks(downloaded_chunks)
    else:
        consume(downloaded_chunks)


def _copy_file(filename, location, link):
    copy = True
    download_location = os.path.join(location, link.filename)
    if os.path.exists(download_location):
        response = ask_path_exists(
            'The file %s exists. (i)gnore, (w)ipe, (b)ackup, (a)abort' %
            display_path(download_location), ('i', 'w', 'b', 'a'))
        if response == 'i':
            copy = False
        elif response == 'w':
            logger.warning('Deleting %s', display_path(download_location))
            os.remove(download_location)
        elif response == 'b':
            dest_file = backup_dir(download_location)
            logger.warning(
                'Backing up %s to %s',
                display_path(download_location),
                display_path(dest_file),
            )
            shutil.move(download_location, dest_file)
        elif response == 'a':
            sys.exit(-1)
    if copy:
        shutil.copy(filename, download_location)
        logger.info('Saved %s', display_path(download_location))


def unpack_http_url(link, location, download_dir=None,
                    session=None, hashes=None, progress_bar="on"):
    if session is None:
        raise TypeError(
            "unpack_http_url() missing 1 required keyword argument: 'session'"
        )

    with TempDirectory(kind="unpack") as temp_dir:
        # If a download dir is specified, is the file already downloaded there?
        already_downloaded_path = None
        if download_dir:
            already_downloaded_path = _check_download_dir(link,
                                                          download_dir,
                                                          hashes)

        if already_downloaded_path:
            from_path = already_downloaded_path
            content_type = mimetypes.guess_type(from_path)[0]
        else:
            target_relpath = tuf_downloader and tuf_downloader.match(link.url)

            if target_relpath:
                from_path, content_type = \
                                       tuf_downloader.download(target_relpath,
                                                               temp_dir.path,
                                                               link.filename)
            else:
                # let's download to a tmp dir
                from_path, content_type = _download_http_url(link,
                                                             session,
                                                             temp_dir.path,
                                                             hashes,
                                                             progress_bar)

        # unpack the archive to the build dir location. even when only
        # downloading archives, they have to be unpacked to parse dependencies
        unpack_file(from_path, location, content_type, link)

        # a download dir is specified; let's copy the archive there
        if download_dir and not already_downloaded_path:
            _copy_file(from_path, download_dir, link)

        if not already_downloaded_path:
            os.unlink(from_path)


def unpack_file_url(link, location, download_dir=None, hashes=None):
    """Unpack link into location.

    If download_dir is provided and link points to a file, make a copy
    of the link file inside download_dir.
    """
    link_path = url_to_path(link.url_without_fragment)

    # If it's a url to a local directory
    if is_dir_url(link):
        if os.path.isdir(location):
            rmtree(location)
        shutil.copytree(link_path, location, symlinks=True)
        if download_dir:
            logger.info('Link is a directory, ignoring download_dir')
        return

    # If --require-hashes is off, `hashes` is either empty, the
    # link's embedded hash, or MissingHashes; it is required to
    # match. If --require-hashes is on, we are satisfied by any
    # hash in `hashes` matching: a URL-based or an option-based
    # one; no internet-sourced hash will be in `hashes`.
    if hashes:
        hashes.check_against_path(link_path)

    # If a download dir is specified, is the file already there and valid?
    already_downloaded_path = None
    if download_dir:
        already_downloaded_path = _check_download_dir(link,
                                                      download_dir,
                                                      hashes)

    if already_downloaded_path:
        from_path = already_downloaded_path
    else:
        from_path = link_path

    content_type = mimetypes.guess_type(from_path)[0]

    # unpack the archive to the build dir location. even when only downloading
    # archives, they have to be unpacked to parse dependencies
    unpack_file(from_path, location, content_type, link)

    # a download dir is specified and not already downloaded
    if download_dir and not already_downloaded_path:
        _copy_file(from_path, download_dir, link)


def _copy_dist_from_dir(link_path, location):
    """Copy distribution files in `link_path` to `location`.

    Invoked when user requests to install a local directory. E.g.:

        pip install .
        pip install ~/dev/git-repos/python-prompt-toolkit

    """

    # Note: This is currently VERY SLOW if you have a lot of data in the
    # directory, because it copies everything with `shutil.copytree`.
    # What it should really do is build an sdist and install that.
    # See https://github.com/pypa/pip/issues/2195

    if os.path.isdir(location):
        rmtree(location)

    # build an sdist
    setup_py = 'setup.py'
    sdist_args = [sys.executable]
    sdist_args.append('-c')
    sdist_args.append(SETUPTOOLS_SHIM % setup_py)
    sdist_args.append('sdist')
    sdist_args += ['--dist-dir', location]
    logger.info('Running setup.py sdist for %s', link_path)

    with indent_log():
        call_subprocess(sdist_args, cwd=link_path, show_stdout=False)

    # unpack sdist into `location`
    sdist = os.path.join(location, os.listdir(location)[0])
    logger.info('Unpacking sdist %s into %s', sdist, location)
    unpack_file(sdist, location, content_type=None, link=None)


class PipXmlrpcTransport(xmlrpc_client.Transport):
    """Provide a `xmlrpclib.Transport` implementation via a `PipSession`
    object.
    """

    def __init__(self, index_url, session, use_datetime=False):
        xmlrpc_client.Transport.__init__(self, use_datetime)
        index_parts = urllib_parse.urlparse(index_url)
        self._scheme = index_parts.scheme
        self._session = session

    def request(self, host, handler, request_body, verbose=False):
        parts = (self._scheme, host, handler, None, None, None)
        url = urllib_parse.urlunparse(parts)
        try:
            headers = {'Content-Type': 'text/xml'}
            response = self._session.post(url, data=request_body,
                                          headers=headers, stream=True)
            response.raise_for_status()
            self.verbose = verbose
            return self.parse_response(response.raw)
        except requests.HTTPError as exc:
            logger.critical(
                "HTTP error %s while getting %s",
                exc.response.status_code, url,
            )
            raise


def unpack_url(link, location, download_dir=None,
               only_download=False, session=None, hashes=None,
               progress_bar="on"):
    """Unpack link.
       If link is a VCS link:
         if only_download, export into download_dir and ignore location
          else unpack into location
       for other types of link:
         - unpack into location
         - if download_dir, copy the file into download_dir
         - if only_download, mark location for deletion

    :param hashes: A Hashes object, one of whose embedded hashes must match,
        or HashMismatch will be raised. If the Hashes is empty, no matches are
        required, and unhashable types of requirements (like VCS ones, which
        would ordinarily raise HashUnsupported) are allowed.
    """
    # non-editable vcs urls
    if is_vcs_url(link):
        unpack_vcs_link(link, location)

    # file urls
    elif is_file_url(link):
        unpack_file_url(link, location, download_dir, hashes=hashes)

    # http urls
    else:
        if session is None:
            session = PipSession()

        unpack_http_url(
            link,
            location,
            download_dir,
            session,
            hashes=hashes,
            progress_bar=progress_bar
        )
    if only_download:
        write_delete_marker_file(location)


def _download_http_url(link, session, temp_dir, hashes, progress_bar):
    """Download link url into temp_dir using provided session"""
    target_url = link.url.split('#', 1)[0]
    try:
        resp = session.get(
            target_url,
            # We use Accept-Encoding: identity here because requests
            # defaults to accepting compressed responses. This breaks in
            # a variety of ways depending on how the server is configured.
            # - Some servers will notice that the file isn't a compressible
            #   file and will leave the file alone and with an empty
            #   Content-Encoding
            # - Some servers will notice that the file is already
            #   compressed and will leave the file alone and will add a
            #   Content-Encoding: gzip header
            # - Some servers won't notice anything at all and will take
            #   a file that's already been compressed and compress it again
            #   and set the Content-Encoding: gzip header
            # By setting this to request only the identity encoding We're
            # hoping to eliminate the third case. Hopefully there does not
            # exist a server which when given a file will notice it is
            # already compressed and that you're not asking for a
            # compressed file and will then decompress it before sending
            # because if that's the case I don't think it'll ever be
            # possible to make this work.
            headers={"Accept-Encoding": "identity"},
            stream=True,
        )
        resp.raise_for_status()
    except requests.HTTPError as exc:
        logger.critical(
            "HTTP error %s while getting %s", exc.response.status_code, link,
        )
        raise

    content_type = resp.headers.get('content-type', '')
    filename = link.filename  # fallback
    # Have a look at the Content-Disposition header for a better guess
    content_disposition = resp.headers.get('content-disposition')
    if content_disposition:
        type, params = cgi.parse_header(content_disposition)
        # We use ``or`` here because we don't want to use an "empty" value
        # from the filename param.
        filename = params.get('filename') or filename
    ext = splitext(filename)[1]
    if not ext:
        ext = mimetypes.guess_extension(content_type)
        if ext:
            filename += ext
    if not ext and link.url != resp.url:
        ext = os.path.splitext(resp.url)[1]
        if ext:
            filename += ext
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'wb') as content_file:
        _download_url(resp, link, content_file, hashes, progress_bar)
    return file_path, content_type


def _check_download_dir(link, download_dir, hashes):
    """ Check download_dir for previously downloaded file with correct hash
        If a correct file is found return its path else None
    """
    download_path = os.path.join(download_dir, link.filename)
    if os.path.exists(download_path):
        # If already downloaded, does its hash match?
        logger.info('File was already downloaded %s', download_path)
        if hashes:
            try:
                hashes.check_against_path(download_path)
            except HashMismatch:
                logger.warning(
                    'Previously-downloaded file %s has bad hash. '
                    'Re-downloading.',
                    download_path
                )
                os.unlink(download_path)
                return None
        return download_path
    return None
