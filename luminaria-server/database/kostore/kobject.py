class KObject:
    TYPE = 'KOBJECT'
    METADATA = '<!METADATA>'

    def __init__(self):
        self.data = {KObject.METADATA: None}

    def stringify(self):
        d = self.data
        if KObject.METADATA not in d:
            d[KObject.METADATA] = None
        return str(d)

    def metadata(self):
        return self.data[KObject.METADATA]
