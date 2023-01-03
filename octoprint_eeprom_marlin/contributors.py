__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)

GITHUB_URL = "https://github.com/"


##############################################
# Adding users
# Name field can be either name, or username (with an @)
# if username is empty, then it will not be linked
##############################################


CONTRIBUTORS = [
    {"name": "Anderson Silva (Previous maintainer)", "username": "amsbr"},
    {"name": "Dan Pasanen", "username": "invisiblek"},
    {"name": "@Desterly", "username": "Desterly"},
    {"name": "@gddeen", "username": "gddeen"},
]


def export_contributors():
    return _export_urls(CONTRIBUTORS)


def _export_urls(data):
    """Adds github links"""
    exported = []
    for item in data:
        if item["username"]:
            url = GITHUB_URL + item["username"]
        else:
            url = ""

        exported.append({"name": item["name"], "url": url})
    return exported
