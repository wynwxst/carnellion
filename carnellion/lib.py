
import os
import copy
import random
import json as js
class objects:
    def function(con="",type="def"):
        l = {}
        te = ""
        conn = con.split(" |s ")
        for i in conn:
            te += f"\n\t{i}"

        exec(f"{type} func(*args):\n{te}",l,l)
        return copy.deepcopy(l["func"])
    def json(*args):
        with open(*args,"r") as x:

            return objects.object(data=js.load(x))

    def model(li):
        def obj(*args):
            k = {}

            pos = 0
            for i in li:
                k[i] = args[pos]
                pos += 1






            return objects.object(**k)
        return obj


    class object_class:
        def __init__(self,**kwargs):
            pass







        def call(self,sv,**kwargs):
            d = {"c":self}
            exec(f"x = c.{sv}",d,d)
            if type(d["x"]) == type(self.call):
                return d["x"](**kwargs)
            else:
                return d["x"]
    def object(**k):
        x = copy.deepcopy(objects.object_class)()
        for i in k:
            setattr(x,i,k[i])
        return x
