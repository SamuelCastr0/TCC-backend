import jwt
import datetime, time
from django.conf import settings
from .models import User

def createToken(user): 
    payload = dict(
        id=user.id,
        exp=time.mktime((datetime.datetime.utcnow() + datetime.timedelta(hours=24)).timetuple()) * 1000,
        iat=datetime.datetime.utcnow(),
        isStaff=user.is_staff
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token

def getUserFromToken(token):
    tokenDecoded = jwt.decode(token, settings.JWT_SECRET,  algorithms="HS256")
    user = User.objects.filter(id=tokenDecoded['id']).first()

    if user:
        return user
    return None