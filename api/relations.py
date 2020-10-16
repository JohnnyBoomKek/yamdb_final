from django.utils.functional import SimpleLazyObject
from rest_framework.relations import ManyRelatedField as BaseManyRelatedField, MANY_RELATION_KWARGS, SlugRelatedField as BaseSlugRelatedField


class ManyRelatedField(BaseManyRelatedField):
    def to_representation(self, iterable):
        return [
            self.child_relation.to_representation(value)
            for value in iterable if self.read_only or value in self.child_relation.queryset
        ]


class SlugRelatedField(BaseSlugRelatedField):
    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {'child_relation': cls(*args, **kwargs)}
        for key in kwargs.keys():
            if key in MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return ManyRelatedField(**list_kwargs)
