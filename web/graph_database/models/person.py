from neomodel import RelationshipTo, StringProperty, StructuredNode, UniqueIdProperty

from .system import System 

class Person(StructuredNode):
    uid = UniqueIdProperty()
    full_name = StringProperty(name='fullName')
    owner_of = RelationshipTo(System, 'OWNS')
