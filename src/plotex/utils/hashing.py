import hashlib
import base64


def hash_url(url):
    """
    generate a hash for the url

    :param url: the url string
    :return: the generated hash
    """
    # Take the hash of the URL
    url_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()
    # Encode the hash in base64
    file_name = base64.b64encode(url_hash.encode('utf-8')).decode('utf-8')
    # Remove any characters that are not safe for use in a file name
    file_name = file_name.replace('/', '_').replace('+', '-')
    # Truncate the file name to a maximum length
    file_name = file_name[:10]
    return file_name