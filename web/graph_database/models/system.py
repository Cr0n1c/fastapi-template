from neomodel import DateProperty, StringProperty, StructuredNode, UniqueIdProperty

class System(StructuredNode):  
    uid = UniqueIdProperty()
    hostname = StringProperty(unique_index=True, required=True)
    ip_address = StringProperty(name='ipAddress')
    last_updated = DateProperty(name='lastUpdated')