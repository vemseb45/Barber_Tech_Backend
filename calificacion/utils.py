# calificacion/utils.py

from datetime import datetime  
from rest_framework.exceptions import ValidationError  

def validar_cita_finalizada(cita):  
    if cita.fecha > datetime.now():  
        raise ValidationError("No puedes calificar una cita que no ha terminado")