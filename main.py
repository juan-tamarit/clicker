from time import time
import tkinter as tk
from tkinter import ttk

class Clicker:

    def __init__(self,count:int,)->None:
        self.count=count
        self.delta=int(1)

    def click(self)->None:
        self.count+=self.delta

    def set_count(self,count:int)->None:
        self.count=count

    def refresh_delta(self,mod:int)->None:
        self.delta=int(1+mod)

class Perfil:

    def __init__(self,lvl:int,objects:list[Objeto])->None:
        self.lvl=lvl
        self.objects=objects

    def click(self)->None:
        self.lvl+=1

class Objeto:

    def __init__(self,nombre:str,clicker:Clicker,lvl:int,activo:bool)->None:
        self.nombre=nombre
        self.clicker=clicker
        self.lvl=lvl
        self.activo=activo
        self.umbral=500

    def action(self)->None:
        pass

    def next_lvl(self,clicks:int):
        if clicks>=self.umbral*2**self.lvl:
            self.lvl+=1

    def activate(self,clicks:int)->None:
        if clicks>=self.umbral:
            self.activo=True

class AutoClicker(Objeto):

    def __init__(self,nombre:str,clicker:Clicker,lvl:int)->None:
        super().__init__(nombre,clicker,lvl,False)

    def action(self)->None:
        if self.activo:
            for _ in range(self.lvl):
                self.clicker.click()

class ClickerWindow:

    def __init__(self, root:tk.Tk,clicker:Clicker,perfil:Perfil)->None:
        self.root=root
        self.clicker=clicker
        self.perfil=perfil
        root.title(f"Clicker")
        self._build_ui()
        self._handle_autoclick()

    def _build_ui(self)->None:
        clicks_row=ttk.Frame(self.root)
        clicks_row.pack(fill="x",padx=10,pady=10)
        
        clicks_label=ttk.Label(clicks_row,text="Clicks: ")
        self.num_clicks=ttk.Label(clicks_row,text=str(self.clicker.count))#self para que pueda actualizarse en vivo 
        click_button=ttk.Button(clicks_row,command=self._handle_click,text="Click")

        clicks_label.pack(side="left",padx=5)
        self.num_clicks.pack(side="left",padx=5)
        click_button.pack(side="right",padx=5)

        lvl_row=ttk.Frame(self.root)
        lvl_row.pack(fill="x",padx=10,pady=10)

        lvl_label=ttk.Label(lvl_row,text="Nivel: ")
        self.num_lvl=ttk.Label(lvl_row,text=str(self.perfil.lvl))
        lvl_button=ttk.Button(lvl_row,command=self._handle_lvl,text="Level Up")

        lvl_label.pack(side="left",padx=5)
        self.num_lvl.pack(side="left",padx=5)
        lvl_button.pack(side="right", padx=5)

        objects_row=ttk.Frame(self.root)
        objects_row.pack(fill="x",padx=10,pady=10)

        for obj in self.perfil.objects:
            obj_row=ttk.Frame(objects_row)
            obj_row.pack(fill="x", padx=2)

            object_label=ttk.Label(obj_row,text=f"{obj.nombre} Lvl: {obj.lvl}")
            object_button=ttk.Button(obj_row)

            if not obj.activo:
                object_button.config(
                    text=f"Comprar",
                    command=lambda o=obj, btn=object_button, lbl=object_label:(
                        o.activate(self.clicker.count),
                        o.next_lvl(self.clicker.count),
                        self.clicker.set_count(0),
                        self.num_clicks.config(text=str(self.clicker.count)),
                        btn.config(
                            text=f"Level Up",
                            command= lambda x=o, lbl=lbl:(
                                x.next_lvl(self.clicker.count),
                                self.clicker.set_count(0),
                                self.num_clicks.config(text=str(self.clicker.count)),
                                lbl.config(text=f"{x.nombre} Lvl: {x.lvl}")
                            )
                        )   
                    )
                )
            else:
                object_button.config(
                    text=f"Level Up",
                    command= lambda o=obj, lbl=object_label:(
                        o.next_lvl(self.clicker.count),
                        self.clicker.set_count(0),
                        self.num_clicks.config(text=str(self.clicker.count)),
                        lbl.config(text=f"{o.nombre} Lvl: {o.lvl}")
                    )
                )

            object_label.pack(side="left", padx=5)
            object_button.pack(side="right", padx=5)


    def _handle_autoclick(self)->None:
        self.perfil.objects[0].action()
        self.num_clicks.config(text=str(self.clicker.count))
        self.root.after(5000,self._handle_autoclick)

    def _handle_click(self)->None:
        """Nos permite manejar a la vez el cambio del contador y el label que muestra el número de clicks"""
        self.clicker.click()
        self.num_clicks.config(text=str(self.clicker.count))

    def _handle_lvl(self)->None:
        """Nos permite manejar a la vez el cambio del nivel y el label que muestra el número de niveles"""
        import math
        umbral=0 if self.clicker.count < 100 else int(math.log2(self.clicker.count))
        if self.perfil.lvl < umbral:
            self.perfil.click()
            self.clicker.refresh_delta(self.perfil.lvl)
            self.num_lvl.config(text=str(self.perfil.lvl))
            self.clicker.set_count(0)
            self.num_clicks.config(text=str(self.clicker.count))

    
def main()->None:
    root=tk.Tk()
    clicker=Clicker(0)
    auto_clicker=AutoClicker("AutoClicker",clicker,0)
    objects=[auto_clicker]
    perfil=Perfil(0,objects)
    ventana=ClickerWindow(root,clicker,perfil)
    root.mainloop()
if __name__=="__main__":
    main()