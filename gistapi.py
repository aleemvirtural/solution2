# coding=utf-8
"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""
import re
import requests
import urllib
import urllib2
from flask import Flask, jsonify, request


# *The* app object
app = Flask(__name__)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


# def getUrl():
#data = urllib.urlencode({'q' : 'user:justdionysus'})
#url = 'https://gist.github.com/search'
#full_url = url + '?' + data
#response = urllib2.urlopen(full_url)
#return url 
import urllib,re

data = urllib.urlencode({'q' : 'user:justdionysus'})
url = 'https://gist.github.com/search'
full_url = url + '?' + data

htmlFile = urllib.urlopen(full_url)
html = htmlFile.read()
regexp_link = r'''https://gist.github.com/justdionysus/6b2972aa971dd605f524'''
pattern = re.compile(regexp_link)
links = re.findall(pattern, html)
var1 = links

var2 = (", ".join(var1))    
#print var2




def gists_for_user(username):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = 'https://api.github.com/users/{username}/gists'.format(
            username=username)
    response = requests.get(gists_url)
    # BONUS: What failures could happen?
    # BONUS: Paging? How does this work for users with tons of gists?

    return response.json()


@app.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()
    # BONUS: Validate the arguments?

    username = post_data['username']
    pattern = post_data['pattern']

    result = {}
    gists = gists_for_user(username)
    # BONUS: Handle invalid users?


    for gist in gists:
        # REQUIRED: Fetch each gist and check for the pattern
        # BONUS: What about huge gists?
        # BONUS: Can we cache results in a datastore/db?
        #pass
	
	#if re.match(pattern, gists) == 'pattern':
 	#	return _compile(pattern, flags).match(string)


	#print gist
	#if re.search(gist, "justdionysus/6b2972aa971dd605f524") :
	pass

    
    result['status'] = 'success'
    result['username'] = username
    result['pattern'] = pattern
    result['matches'] = [var2]

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
