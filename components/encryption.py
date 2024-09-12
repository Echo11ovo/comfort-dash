import base64
from urllib.parse import urlencode, parse_qs

def encode_base64_url_params(params):
    """Encode the URL parameters to a Base64 string."""
    encoded_str = urlencode(params)
    base64_bytes = base64.urlsafe_b64encode(encoded_str.encode('utf-8'))
    return base64_bytes.decode('utf-8')
