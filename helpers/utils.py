from django.conf import settings


def json_value_by_key(data, target_key):
    """
    Recursively search for a key in a nested dictionary.
    Returns the value if found, else None.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, dict):
                result = json_value_by_key(value, target_key)
                if result is not None:
                    return result
    return None


def xml_value_by_tag(element, target_tag):
    """
    Recursively search for a tag in an XML element.
    Returns the text of the first matching tag, else None.
    """
    if element.tag == target_tag:
        return element.text
    for child in element:
        result = xml_value_by_tag(child, target_tag)
        if result is not None:
            return result
    return None


def service_path(request):
    return f"{request.scheme}://{request.get_host()}/{settings.EXTERNAL_BASE_PREFIX}"