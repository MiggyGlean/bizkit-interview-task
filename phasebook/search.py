from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database based on various optional parameters.
    
    Parameters:
        args: a dictionary containing the following search parameters:
            id: string (unique)
            name: string (partial match, case insensitive)
            age: string (match within a range of age-1 to age+1)
            occupation: string (partial match, case insensitive)

    Returns:
        a list of users that match ANY of the search parameters provided
    """
    matched_users = set()

    # Check if ID is in arguments and find the user
    if 'id' in args:
        user = next((user for user in USERS if user['id'] == args['id']), None)
        if user:
            matched_users.add(tuple(user.items()))

    # Continue to check other parameters even if ID is found
    for user in USERS:
        if ('name' in args and args['name'].lower() in user['name'].lower()) or \
           ('occupation' in args and args['occupation'].lower() in user['occupation'].lower()) or \
           ('age' in args and int(user['age']) in range(int(args['age']) - 1, int(args['age']) + 2)):
            matched_users.add(tuple(user.items()))

    # Convert set of tuples back to list of dicts
    return [dict(t) for t in matched_users]

