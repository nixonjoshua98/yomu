from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = True

        return super().dict(**kwargs)
