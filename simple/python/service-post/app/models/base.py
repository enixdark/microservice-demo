class CRUDMixin(object):
    meta = {
        'abstract': True,
    }

    @classmethod
    def all(cls):
        return cls.objects

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get(cls, id):
        try:
            return cls.objects(id=id).first()
        except Exception as error:
            return None

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() or self

    def remove(self):
        return self.delete()
