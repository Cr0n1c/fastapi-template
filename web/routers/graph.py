from fastapi import APIRouter, Depends, HTTPException

import web.graph_database as models

graph = APIRouter()

@graph.get('/')
def home():
    return {'message': 'graph online'}

@graph.get('/systems')
def get_all_systems():
    systems = {}

    for system in models.System.nodes.all():
        systems[system.hostname] = {
            'ipAddress': system.ip_address,
            'uid': system.uid,
            'lastUpdated': system.last_updated,
            'hostname': system.hostname
        }

    return systems

@graph.get('/systems/{system_uid}')
def get_system_by_uid(system_uid: str):
    system = models.System.nodes.first_or_none(uid=system_uid)

    if not system:
        return {}
    
    return {
        'ipAddress': system.ip_address,
        'uid': system.uid,
        'lastUpdated': system.last_updated,
        'hostname': system.hostname
    }


