# file: utils/encoders/encode_device_meta.py
import numpy as np

def encode_device_meta(user_data):
    """
    Encodes device_type and OS_version.
    - device_type is one-hot: [iOS, Android, Other]
    - OS_version is parsed into a float: major.minor/20
    """

    device = user_data.get("device_type", "").lower()
    device_encoded = {
        "ios": [1.0, 0.0, 0.0],
        "android": [0.0, 1.0, 0.0]
    }.get(device, [0.0, 0.0, 1.0])  # default → Other

    os_version_str = user_data.get("os_version", "0.0")
    try:
        major, minor = os_version_str.split(".")[:2]
        os_version = (int(major) + int(minor)/10.0) / 20.0  # normalize to ~[0, 1]
    except:
        os_version = 0.5  # fallback

    return np.array(device_encoded + [os_version])
