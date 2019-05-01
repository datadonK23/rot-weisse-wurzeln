#!/usr/bin/python
""" locate_control

Add Locate control to folium Map.
Based on leaflet plugin: https://github.com/domoritz/leaflet-locatecontrol

Taken from Folium PR#1116 and slightly modified.

Utility methods 'parse_options' and 'camelize' taken from Folium master branch.

Author: dbf [@fullonic](https://github.com/fullonic), Folium contributors
"""

from branca.element import CssLink, Figure, JavascriptLink, MacroElement # type: ignore

from jinja2 import Template
#from folium.utilities import parse_options


class LocateControl(MacroElement):
    """Control plugin to geolocate the user.
    This plugins adds a button to the map, and when it's clicked shows the current
    user device location.
    To work properly in production, the connection needs to be encrypted, otherwise browser will not
    allow users to share their location.
    WARNING: This plugin when used with Draw plugin, it must be added to your map before Draw. See
    example below.
    Parameters
    ----------
    **kwargs
        For possible options, see https://github.com/domoritz/leaflet-locatecontrol
    Examples
    --------
    >>> m = folium.Map()
    # With default settings
    >>> LocateControl().add_to(m)
    # With custom options and alongside with Draw
    >>> LocateControl(
    ...     position="bottomright",
    ...     strings={"title": "See you current location",
    ...              "popup": "Your position"}).add_to(m))
    >>> Draw(export=True).add_to(m)
    For more info check:
    https://github.com/domoritz/leaflet-locatecontrol
    """

    _template = Template("""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.control.locate(
                {{this.options | tojson}}
            ).addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)

    def __init__(self, **kwargs):
        super(LocateControl, self).__init__()
        self._name = 'LocateControl'
        self.options = parse_options(**kwargs)

    def render(self, **kwargs):
        super(LocateControl, self).render(**kwargs)
        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            CssLink(
                "https://cdnjs.cloudflare.com/ajax/libs/leaflet-locatecontrol/0.66.2/L.Control.Locate.min.css"))  # noqa
        figure.header.add_child(JavascriptLink(
            "https://cdnjs.cloudflare.com/ajax/libs/leaflet-locatecontrol/0.66.2/L.Control.Locate.min.js"))  # noqa


def parse_options(**kwargs):
    """Return a dict with lower-camelcase keys and non-None values.."""
    return {camelize(key): value
            for key, value in kwargs.items()
            if value is not None}

def camelize(key):
    """Convert a python_style_variable_name to lowerCamelCase.
    Examples
    --------
    >>> camelize('variable_name')
    'variableName'
    >>> camelize('variableName')
    'variableName'
    """
    return ''.join(x.capitalize() if i > 0 else x
                   for i, x in enumerate(key.split('_')))
