from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
import json
from .models import Sport, Badge
from .settings import *


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return redirect(url_for('views.event_search'))
    #return redirect("/events", code=200)
    #return render_template("home.html", user=current_user)

@views.route('create_equipment/', methods=['POST','GET'])
def create_equipment():
    
    """
    This prepares the front-end side of the equipment addition functionality.
    It can be used as a POST; when it is used as a POST, the provided fields for an equipment is posted.
    The intended response is created.
    """
    
    if request.method == 'POST':
        equipment = {
            "name" : request.form.get("name")
        }

        req = BASE_URL+"/api/v1.0/equipments/"
        headers = {'Content-type': 'application/json'}
        response = requests.post(req, data=json.dumps(equipment), headers=headers)

        if response.status_code == 201:
            flash('Equipment Created', category='success')
            return redirect(url_for('views.home'))
        elif response.status_code == 400 :
            flash('Check Information Entered', category='error')
        elif response.status_code == 409 :
            flash('Equipment Already Exists!', category='error')
        else:
            flash('Error Occured, Try Again Later', category='error')
    
    return render_template("equipments.html", user=current_user)
    

@views.route('badge/', methods=['POST','GET'])
def badge():
    """
    This prepares the front-end side of the badge addition functionality.
    It can be used as a POST and GET. When it is used as a GET, badge addition page is shown to provide related fields for it.
    When it is used as a POST, the provided fields for a badge is posted and badge post endpoint is requested.
    """
    if request.method == "POST":
        badge = {
            "name" : request.form.get("name"),
            "symbol": request.form.get("symbol")
        }

        req = BASE_URL+"/api/v1.0/badges"
        headers = {'Content-type': 'application/json'}
        response = requests.post(req, data=json.dumps(badge), headers=headers)

        if response.status_code == 201:
            flash('Badge Added', category='success')
        else:
            flash('Error Occured, Try Again Later', category='error')

        return redirect(url_for('views.home'))
    
    return render_template("badge.html", user= current_user)

  
  
@views.route('show_badge/', methods=['POST','GET'])
def show_badge():
    """ This function takes a json from the show_badge API. That json contains
    a boolean variable control, cat photos and other informations of badges from the
    database. API also returns a status code and if the status code is not 200, it means
    there is a problem.
    """
    if request.method == "POST":

        req = BASE_URL+"/api/v1.0/badges/show_badge/"
        headers = {'Content-type': 'application/json'}
        response = requests.get(req, headers=headers)
        json_response = response.json()
        
        if response.status_code != 200:
            flash('Error Occured, Try Again Later', category='error')

        badges = []
        for badge in json_response['badges']:
            badges.append(Badge(badgeID=badge['badgeID'], name=badge['name'], point=badge['point']))
            
        return render_template("show_badges.html", badges=list(zip(badges,json_response['dog_photos'])), control=json_response['control'], user= current_user)
    
    return render_template("show_badges.html", user= current_user)



@views.route('point_badge/', methods=['POST','GET'])
def point_badge():
    """
    This prepares the front-end side of the badge point retrieval.
    It can be used as a POST and GET. When it is used as a GET, badge point retrieval page is shown.
    When it is used as a POST, badge point for a given badge name is shown.
    """
    if request.method == "POST":

        badge_name = request.form.get('name')
        req = f'{BASE_URL}/api/v1.0/badges/point?name={badge_name}'
        headers = {'Content-type': 'application/json'}
        response = requests.get(req, headers=headers)

        if response.status_code != 200:
            flash(response.text, category='error')
            return redirect(url_for('views.home'))
            
        return render_template("show_badge_point.html", user=current_user, badge=response.json())
    
    return render_template("point_badge.html", user=current_user)


"""
    Get sport id-name pairs.
    return:
        Dictionary with id key, sport name value
"""

def get_sport_names():
    result = Sport.query.all()

    sports={}

    for sport in result:
        sports[sport.id] = sport.sport
    return sports

"""
    List all sport id-name pairs with a name filter
"""
@views.route('sports/', methods=['POST','GET'])
def sports_page():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        # Call sports API to get filtered sports.
        req = BASE_URL+"/api/v1.0/sports?keyword=" + keyword
        headers = {'Content-type': 'application/json'}
        response = requests.get(req, headers=headers)
        items = response.json()['sports']

        # No error occured, list sports
        if response.status_code == 200:
            return render_template("sports.html", user= current_user, items=items)
        # Error occured, error message
        else:
            flash('Some Error Occured', category='error')
    
    return render_template("sports.html", user= current_user, items=[])

"""
    Front-end to create event.
    
"""

@views.route('create_event/', methods=['POST','GET'])
@login_required
def create_event():
    # Get id - sport name pairs
    sports = get_sport_names()
    if request.method == 'POST':
        # Get form information
        event = {
            "name" : request.form.get('name'),
            "date" : request.form.get('date'),
            "location" : request.form.get('location'),
            "sport" : request.form.get('sport'),
            "creator_user" : current_user.id
        }

        # Make request to back-end API
        req = BASE_URL+"/api/v1.0/events"
        headers = {'Content-type': 'application/json'}
        response = requests.post(req, data=json.dumps(event), headers=headers)
        event = response.json()

        # No error, show event information
        if response.status_code == 201:
            flash('Event Created', category='success')
            return render_template("create_event.html", user= current_user, sports=sports, created = True, event = event)
        # Incorrect information
        elif response.status_code == 400 :
            flash('Check Information Entered', category='error')
        # Some other error
        else:
            flash('Error Occured, Try Again Later', category='error')
    
    return render_template("create_event.html", user= current_user, sports=sports, created = False, event = {})

# helper method for url handling
def url_handler_events(base, name, sport, date_from, date_to):
    url = base
    params = []

    # collect parameters
    if name:
        params.append("name="+name)
    if sport:
        params.append("sport="+str(sport))
    if date_from:
        params.append("date_from="+date_from)
    if date_to:
        params.append("date_to="+date_to)
    
    # handle collected parameters. change url accordingly
    if params:
        url += "?"
        for par in params:
            url += (par+"&")
        url = url[:-1]
    
    return url

@views.route('events/', methods=['POST', 'GET'])
@login_required
def event_search():
    # gets sport names and ids
    sports = get_sport_names()

    # initialize request url
    req = BASE_URL+"/api/v1.0/events"

    # handle post request from frontend. in form input format
    if request.method == 'POST':
        
        print(request.form.get('date_from'))
        # change url according to posted parameters
        req = url_handler_events(req, request.form.get('name'), request.form.get('sport'), request.form.get('date_from'), request.form.get('date_to'))
        print(req)

    # call api from event.py file
    headers = {'Content-type': 'application/json'}
    response = requests.get(req, headers = headers)

    # return rendered page
    if response.status_code == 200:
        #flash('Events are fetched successfully', category='success')
        # TODO: When event page implemented, redirect to it.
        return render_template("event_search.html", user= current_user, sports=sports, events=response.json())
    elif response.status_code == 400 :
        return "<h1>Check Information Entered</h1>"
    else:
        return "<h1>Error Occured, Try Again Later</h1>"

  
@views.route('events/<event_id>/', methods=['GET'])
def view_event(event_id):
    """
    This is the front-end side of the show event by id functionality.
    Shows the event information for the event with event_id and also
    the corresponding weather icon, according to the weather description in
    the event location.
    """
    if request.method == 'GET':
        
        uri = f"{BASE_URL}/api/v1.0/events/{event_id}/"        
        res = requests.get(uri)      
        event = res.json() 
        # Incorrect information
        if res.status_code == 400:
            return "<h1>ERROR : The ID is invalid</h1>"
        # There exists no such event with the corresponding ID
        elif res.status_code == 404 :         
            return "<h1>ERROR : There is no such event</h1>"
        else:      
            icon = event["weather_icon"]
            weather_icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            url = f"/events/{event_id}/discussions"
            return render_template("event_page_by_id.html", user = current_user, event = event, weather_icon_url = weather_icon_url, url=url)


# Shows the discussion page for the event with id event_id. 
# It also shows the description of the sport type of the event 
# using an external API 
@views.route('/events/<event_id>/discussions', methods=["GET"])
@login_required
def discussionPage(event_id):
    
    BASE = 'http://127.0.0.1:5000/'  #  should be changed
    response = requests.get(BASE + 'api/v1.0/events/' + event_id + '/discussions')

    if response.status_code == 201:
        description = response.json()["description"]
        text = response.json()["text"]
        return render_template("discussionPage.html", user= current_user, event_id=event_id, definition = description, text = text.split('#')) 
    else:

        return f"<h1>Error<h1>"
      
      
@views.route('/events/<event_id>/discussionPost', methods=["GET", "POST"])
@login_required
def discussionPost(event_id):
    
    if request.method == 'GET':
        return render_template("discussionPost.html", event_id=event_id, user=current_user)
    else:
        message = {"text" : request.form.get('comment')}

        BASE = 'http://127.0.0.1:5000/'  #  should be changed
        
        headers = {'Content-type': 'application/json'}
        response = requests.post(BASE + '/api/v1.0/events/' + event_id + '/discussions', data=json.dumps(message), headers=headers)
       
        if response.status_code == 201:
            flash('Comment Posted', category='success')
            return redirect(url_for('views.discussionPage', event_id=event_id, user=current_user))
        
        else:
            flash('Error Occured, Try Again Later', category='error')

        return redirect(url_for('views.discussionPost', event_id=event_id, user=current_user))
