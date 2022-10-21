from dataclasses import dataclass, field
from json import load as jsonload
from pathlib import Path
from tkinter.ttk import Treeview, Scrollbar, Label
from tkinter import VERTICAL, Tk
from pipe import where, select, sort, reverse, groupby, traverse
from typing import NewType, Final
from typing import Any as AnyType
from collections.abc import Sequence


@dataclass
class Cooker:
    id: str = ""
    difficulty: int = -1

    def __repr__(self) -> str:
        diff:str = "" if self.difficulty == -1 else f" adds {self.difficulty} difficulty"
        return f"{self.id}{diff}"


@dataclass
class Container:
    id: str = ""
    difficulty: int = -1

    def __repr__(self) -> str:
        diff:str = "" if self.difficulty == -1 else f" adds {self.difficulty} difficulty"
        return f"{self.id}{diff}"


@dataclass
class Ingredient:
    id: str
    cstate: str = ""
    pstate: str = ""
    material: str = ""
    realtemplate: str = ""
    difficulty: int = -1
    loss: int = -1
    ratio: int = -1
    amount: int = -1
    creature: str = ""

    def __repr__(self) -> str:
        if self.cstate == "":
            c = ""
        elif self.cstate == "none":
            c = ", no cook"
        else:
            c = ", {}".format(self.cstate)
        
        if self.pstate == "":
            p = ""
        elif self.pstate == "none":
            p = ", no prep"
        else:
            p = ", {}".format(self.pstate)

        return "{id}{c}{p}{mat}{real}{diff}{loss}{ratio}{amt}{creature}".format(id=self.id, c=c, p=p,
                    mat="" if self.material == "" else ", {}".format(self.material),
                    real="" if self.realtemplate == "" else ", real {}".format(self.realtemplate),
                    diff="" if self.difficulty == -1 else ", adds {} difficulty".format(self.difficulty),
                    loss="" if self.loss == -1 else ", loss {}%".format(self.loss),
                    ratio="" if self.ratio == -1 else ", ratio {}%".format(self.ratio),
                    amt="" if self.amount == -1 else ", amount {}".format(self.amount),
                    creature="" if self.creature == -1 else ", {}".format(self.creature)
        )
EMPTY_INGREDIENT: Final[Ingredient] = Ingredient(id="")


@dataclass
class Mandatory:
    ingredients:list[Ingredient] = field(default_factory=list)
    
    def __init__(self, mandatory:list[dict[str,AnyType]]=[]):
        self.ingredients = list(mandatory | select(lambda x: Ingredient(**x)))
    
    def __iter__(self):
        self.n = -1
        return self

    def __next__(self) -> Ingredient:
        self.n += 1
        if self.n >= len(self.ingredients):
            raise StopIteration
        else:
            return self.ingredients[self.n]

EMPTY_MANDATORY: Final[Mandatory] = Mandatory()


@dataclass
class Optional:
    ingredients:list[Ingredient] = field(default_factory=list)
    
    def __init__(self, optional:list[dict[str,AnyType]]=[]):
        self.ingredients = list(optional | select(lambda x: Ingredient(**x)))
    
    def __iter__(self):
        self.n = -1
        return self

    def __next__(self) -> Ingredient:
        self.n += 1
        if self.n >= len(self.ingredients):
            raise StopIteration
        else:
            return self.ingredients[self.n]

EMPTY_OPTIONAL: Final[Optional] = Optional()


@dataclass
class Oneof:
    ingredients:list[list[Ingredient]] = field(default_factory=list)

    def __init__(self, oneof:list[dict[str,AnyType]]=[]):
        # [{'list':[{str, AnyType}, ...]}, ...]
        if not oneof:
            self.ingredients = []
            return
        _ing_group = []
        _ing = []
        for e1 in oneof:
            _ing_group.append(e1['list'])
            #_ing_group.append(list(e1.values())[0])
            # The zero index is a magic number hack. There is something weird happening between
            # Wurm's json format, PY's json import. Removing the 'list' here ends up making
            # another list...[{'list': [...]}, {'list': [...]}]
        for i, v in enumerate(_ing_group):
            _ing.append([])
            _ing[i].append(list (v | select(lambda x: Ingredient(**x))))
        self.ingredients = _ing
    
    def __iter__(self):
        self.n = -1
        return self

    def __next__(self) -> Ingredient:
        self.n += 1
        if self.n >= len(self.ingredients):
            raise StopIteration
        else:
            return self.ingredients[self.n]

EMPTY_ONEOF: Final[Oneof] = Oneof()


@dataclass
class Zeroorone:
    ingredients:list[list[Ingredient]] = field(default_factory=list)
    
    def __init__(self, zeroorone:list[dict[str,AnyType]]=[]):
        # [{'list':[{str, AnyType}, ...]}, ...]
        if not zeroorone:
            self.ingredients = []
            return
        _ing_group = []
        _ing = []
        for e1 in zeroorone:
            _ing_group.append(e1['list'])
            #_ing_group.append(list(e1.values())[0])
            # The zero index is a magic number hack. There is something weird happening between
            # Wurm's json format, PY's json import. Removing the 'list' here ends up making
            # another list...[{'list': [...]}, {'list': [...]}]
        for i, v in enumerate(_ing_group):
            _ing.append([])
            _ing[i].append(list (v | select(lambda x: Ingredient(**x))))
        self.ingredients = _ing

    def __iter__(self):
        self.n = -1
        return self

    def __next__(self) -> Ingredient:
        self.n += 1
        if self.n >= len(self.ingredients):
            raise StopIteration
        else:
            return self.ingredients[self.n]

EMPTY_ZEROORONE: Final[Zeroorone] = Zeroorone()


@dataclass
class Oneormore:
    ingredients:list[list[Ingredient]] = field(default_factory=list)
    
    def __init__(self, oneormore:list[dict[str,AnyType]]=[]):
        # [{'list':[{str, AnyType}, ...]}, ...]
        if not oneormore:
            self.ingredients = []
            return
        _ing_group = []
        _ing = []
        for e1 in oneormore:
            _ing_group.append(e1['list'])
            #_ing_group.append(list(e1.values())[0])
            # The zero index is a magic number hack. There is something weird happening between
            # Wurm's json format, PY's json import. Removing the 'list' here ends up making
            # another list...[{'list': [...]}, {'list': [...]}]
        for i, v in enumerate(_ing_group):
            _ing.append([])
            _ing[i].append(list (v | select(lambda x: Ingredient(**x))))
        self.ingredients = _ing
        abc = 0
    
    def __iter__(self):
        self.n = -1
        return self

    def __next__(self) -> Ingredient:
        self.n += 1
        if self.n >= len(self.ingredients):
            raise StopIteration
        else:
            return self.ingredients[self.n]

EMPTY_ONEORMORE: Final[Oneormore] = Oneormore()


@dataclass
class AnyIngredient:
    ingredients:list[Ingredient] = field(default_factory=list)
    
    def __init__(self, anyIngredient:list[dict[str,AnyType]]=[]):
        self.ingredients = list(anyIngredient | select(lambda x: Ingredient(**x)))
    
    def __iter__(self):
        self.n = -1
        return self

    def __next__(self) -> Ingredient:
        self.n += 1
        if self.n >= len(self.ingredients):
            raise StopIteration
        else:
            return self.ingredients[self.n]

EMPTY_ANYINGREDIENT: Final[AnyIngredient] = AnyIngredient()


@dataclass
class Result:
    id:str
    difficulty:int = -1
    name:str = ""
    realtemplate:str = ""
    refrealtemplate:str = ""
    cstate:str = ""
    pstate:str = ""
    refmaterial:str = ""
    description:str = ""
    usetemplateweight:bool = False
    achievement:str = ""
    material:str = ""
    icon:str = ""
EMPTY_RESULT: Final[Result] = Result(id="", difficulty=-1)
    

class SortException(ValueError):
    '''Raise exception if trying to sort Recipes list in the middle of iteration.'''
    def __init__(self, message, _ind, *args):
        self.message = message
        self.iter_index = _ind
        super(SortException, self).__init__(message, _ind, *args)


@dataclass
class Recipe:
    name: str
    recipeid: int
    skill: str
    result: Result
    trigger: str = ""
    cookers: list[Cooker] = field(default_factory=list)
    containers:  list[Container] = field(default_factory=list)
    active: Ingredient = EMPTY_INGREDIENT
    target: Ingredient = EMPTY_INGREDIENT
    mandatory:Mandatory = EMPTY_MANDATORY
    optional: Optional = EMPTY_OPTIONAL
    oneof: Oneof = EMPTY_ONEOF
    zeroorone: Zeroorone = EMPTY_ZEROORONE
    oneormore: Oneormore = EMPTY_ONEORMORE
    anyIngredient: AnyIngredient = EMPTY_ANYINGREDIENT
    known: bool = False
    nameable: bool = False
    lootable: bool = False

EMPTY_RECIPE: Final[Recipe] = Recipe(name="", recipeid=-1, skill="", trigger="", result=EMPTY_RESULT)

    
class Recipes(object):

    def __init__(self, folder_path: Path):
        self.folder_path:Path = folder_path
        self.recipes:list[Recipe] = []
        self._index:int = -1
        for r in list([ x for x in folder_path.iterdir() if x.is_file()]):
            with open(r, "r") as file:
                data = jsonload(file)
                abc = 0
                if "name" not in data or "recipeid" not in data or "skill" not in data or "result" not in data :
                    # Recipes should always have these.
                    pass
                if "id" not in data["result"]:
                    # Result should always have.
                    pass
                rec = Recipe(name=data["name"], recipeid=int(data["recipeid"]), skill=data["skill"], result=Result(**data["result"]))
                if "cookers" in data:
                    rec.cookers = list(data["cookers"] | select(lambda x: Cooker(**x)))
                if "containers" in data:
                    rec.containers = list(data["containers"] | select(lambda x: Container(**x)))
                if "active" in data:
                    if not data["active"]["id"]:
                        # Active always needs id.
                        pass
                    rec.active = Ingredient(**data["active"])
                if "target" in data:
                    if not data["target"]["id"]:
                        # Target always needs id.
                        pass
                    rec.target = Ingredient(**data["target"])
                if "ingredients" in data and "mandatory" in data["ingredients"]:
                    rec.mandatory = Mandatory(data["ingredients"]["mandatory"])
                if "ingredients" in data and "optional" in data["ingredients"]:
                    rec.optional = Optional(data["ingredients"]["optional"])
                
                # oneof, zeroorone, oneormore are lists of list and need different handling.
                if "ingredients" in data and "oneof" in data["ingredients"]:
                    rec.oneof = Oneof(data["ingredients"]["oneof"])
                if "ingredients" in data and "zeroorone" in data["ingredients"]:
                    rec.zeroorone = Zeroorone(data["ingredients"]["zeroorone"])
                if "ingredients" in data and "oneormore" in data["ingredients"]:
                    rec.oneormore = Oneormore(data["ingredients"]["oneormore"])

                if "ingredients" in data and "any" in data["ingredients"]:
                    rec.anyIngredient = AnyIngredient(data["ingredients"]["any"])
                self.recipes.append(rec)

    def __iter__(self):
        return self
    
    def __next__(self) -> Recipe:
        self._index += 1
        if self._index >= len(self.recipes):
            self._index = -1
            raise StopIteration
        else:
            return self.recipes[self._index]

    def sort_recipes_name(self, _reverse:bool):
        if self._index != -1:
            raise SortException("No sorting while iterating.", self._index)
        self.recipes = list(self.recipes | sort(key=lambda rec: rec.name.lower(), reverse=_reverse))

    def sort_recipes_id(self, _reverse:bool):
        if self._index != -1:
            raise SortException("No sorting while iterating.", self._index)
        self.recipes = list(self.recipes | sort(key=lambda rec: rec.recipeid, reverse=_reverse))

    def get(self) -> list[Recipe]:
        return self.recipes

recipes : Recipes = Recipes(Path(r'.\recipes'))


class RecipeBook:

    def __init__(self, root) -> None:
        root.title("Cooking Recipes")
        root.geometry('400x1000')
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        t = Treeview(root)
        t.grid(column=0, row=0, sticky="nwes")
        t.heading('#0', text="Recipe name")

        s = Scrollbar(root, orient=VERTICAL, command=t.yview)
        s.grid(column=1, row=0, sticky="ns")
        t['yscrollcommand'] = s.set
        
        Label(root, text="Place holder for search tools.", anchor="w").grid(column=0, columnspan=2, row=1, sticky="we")
        
        recipes.sort_recipes_name(False)
        for rec in recipes:
            t.insert("", "end", str(rec.recipeid), text=rec.name, open=False)
            # recipeid isn't useful to show.
            t.insert(str(rec.recipeid), "end", text=f"skill: {rec.skill}")
            if rec.trigger != "":
                t.insert(str(rec.recipeid), "end", text=f"trigger: {rec.trigger}")
            if rec.cookers:
                c_id = "{}_cookers".format(rec.recipeid)
                t.insert(str(rec.recipeid), "end", c_id, text="Cookers", open=True)
                for v in rec.cookers:
                    t.insert(c_id, "end", text= str(v))
                    # "{cooker}{diff}".format(cooker= v.id, diff="" if v.difficulty == 0 else " adds {} difficulty".format(v.difficulty)))
            if rec.containers:
                con_id = f"{rec.recipeid}_cont"
                t.insert(str(rec.recipeid), "end", con_id, text="Containers", open=True)
                for v in rec.containers:
                    t.insert(con_id, "end", text=str(v))
                    #"{container}{diff}".format(container= v.id, diff="" if v.difficulty == 0 else " adds {} difficulty".format(v.difficulty)))
            if rec.active != EMPTY_INGREDIENT:
                t.insert(str(rec.recipeid), "end", text="active: {}".format(str(rec.active).rstrip(", ")))
            if rec.target != EMPTY_INGREDIENT:
                t.insert(str(rec.recipeid), "end", text="target: {}".format(str(rec.target).rstrip(", ")))
            if rec.mandatory != EMPTY_MANDATORY:
                im_id = "{}_mandatory".format(rec.recipeid)
                t.insert(str(rec.recipeid), "end", im_id, text="Mandatory",  open=True)
                for i in rec.mandatory:
                    t.insert(im_id, "end", text=f"{str(i).rstrip(', ')}")
            if rec.optional != EMPTY_OPTIONAL:
                io_id = "{}_optional".format(rec.recipeid)
                t.insert(rec.recipeid, "end", io_id, text="Optional")
                for i in rec.optional:
                    t.insert(io_id, "end", text=f"{str(i).rstrip(', ')}")

            # TODO  oneof, zeroorone, oneormore are lists of list and need different handeling.
            if rec.oneof != EMPTY_ONEOF:
                ioo_id = f"{rec.recipeid}_oneof"
                t.insert(rec.recipeid, "end", ioo_id, text="One of")
                for i, v1 in enumerate(rec.oneof):
                    ioog_id = f"{rec.recipeid}_oneof_{i}"
                    t.insert(ioo_id, "end", ioog_id, text=f"One of group")
                    for v2 in v1[0]:
                        t.insert(ioog_id, "end", text=f"{str(v2).rstrip(', ')}")
            if rec.zeroorone != EMPTY_ZEROORONE:
                izo_id = f"{rec.recipeid}_zeroorone"
                t.insert(rec.recipeid, "end", izo_id, text="Zero or one")
                for i, v1 in enumerate(rec.zeroorone):
                    izog_id = f"{rec.recipeid}_zeroorone_{i}"
                    t.insert(izo_id, "end", izog_id, text=f"Zero or one group")
                    for v2 in v1[0]:
                        t.insert(izog_id, "end", text=f"{str(v2).rstrip(', ')}")
            if rec.oneormore != EMPTY_ONEORMORE:
                iom_id = f"{rec.recipeid}_oneormore"
                t.insert(rec.recipeid, "end", iom_id, text="One or more")
                for i, v1 in enumerate(rec.oneormore):
                    iorg_id = f"{rec.recipeid}_oneormore_{i}"
                    t.insert(iom_id, "end", iorg_id, text=f"One or more group")
                    for v2 in v1[0]:
                        t.insert(iorg_id, "end", text=f"{str(v2).rstrip(', ')}")
            if rec.anyIngredient != EMPTY_ANYINGREDIENT:
                ia_id = "{}_any".format(rec.recipeid)
                t.insert(rec.recipeid, "end", ia_id, text="Any")
                for i in rec.anyIngredient:
                    t.insert(ia_id, "end", tex=f"{str(i).rstrip(', ')}")

        '''
            ingredients: object = None
            result: object = None
            known: bool = False
            nameable: bool = False
            lootable: bool = False
        '''


def main():
    root = Tk()
    RecipeBook(root)
    root.mainloop()

if __name__ == '__main__':
    main()