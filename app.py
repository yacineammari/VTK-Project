from vtk import (vtkRenderer,
                vtkNamedColors,
                vtkRenderWindow,
                vtkRenderWindowInteractor,
                vtkOBJImporter,
                vtkPropPicker,
                vtkTextMapper,
                vtkActor2D
                )


class UI():

    def __init__(self):
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(vtkNamedColors().GetColor3d('SlateGray'))
        self.renderWindow = vtkRenderWindow()
        self.renderWindow.SetSize(640,480)
        self.renderWindow.AddRenderer(self.renderer)
        self.renderWindowInteractor = vtkRenderWindowInteractor()
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)

        self.importer = vtkOBJImporter()
        self.importer.SetFileNameMTL('tnt.mtl')
        self.importer.SetFileName('tnt.obj')
        self.importer.Update()
        self.importer.SetRenderWindow(self.renderWindow)
        self.importer.Update()    
        
        
        # text
        self.text_mapper = vtkTextMapper()
        self.text_mapper.GetTextProperty().SetColor((1,1,1))
        self.text_mapper.GetTextProperty().BoldOn()
        self.text_mapper.GetTextProperty().ShadowOn()
        self.text_mapper.GetTextProperty().SetLineSpacing(0.8)
        self.text_mapper.GetTextProperty().SetFontFamilyToArial()
        self.text_mapper.GetTextProperty().SetFontSize(50)

        self.text_actor = vtkActor2D()
        self.text_actor.SetMapper(self.text_mapper)
        self.text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
        self.text_actor.GetPositionCoordinate().SetValue(0.41,0.89)

        # text
        self.text_mapper1 = vtkTextMapper()
        self.text_mapper1.GetTextProperty().SetColor((1,1,1))
        self.text_mapper1.GetTextProperty().BoldOn()
        self.text_mapper1.GetTextProperty().ShadowOn()
        self.text_mapper1.GetTextProperty().SetLineSpacing(0.8)
        self.text_mapper1.GetTextProperty().SetFontFamilyToArial()
        self.text_mapper1.GetTextProperty().SetFontSize(15)

        self.text_actor1 = vtkActor2D()
        self.text_actor1.SetMapper(self.text_mapper1)
        self.text_actor1.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
        self.text_actor1.GetPositionCoordinate().SetValue(0.01,0.01)

        self.text_mapper1.SetInput(f'TNT : Trinitrotoluene 3D Model C7H5N3O6')

        c  = [i for i in range(1,8)]
        h  = [i for i in range(17,22)]
        n  = [i for i in range(27,30)]
        o  = [i for i in range(30,36)]
        
        actors = self.renderer.GetActors()
        actors.InitTraversal()

        self.map = {'Carbon':[],'Hydrogène':[],'Nitrogen':[],'Oxygen':[]}
        
        for a in range(actors.GetNumberOfItems()):
            actor =  actors.GetNextActor()
            if a in c:
                actor.GetProperty().SetColor((0,0,0))
                self.map['Carbon'].append(actor.GetBounds())               
            elif a in h:
                actor.GetProperty().SetColor((0,1,0))
                self.map['Hydrogène'].append(actor.GetBounds())                        
            elif a in n:
                actor.GetProperty().SetColor((0,0,1))
                self.map['Nitrogen'].append(actor.GetBounds())        
            elif a in o:
                actor.GetProperty().SetColor((1,0,0))
                self.map['Oxygen'].append(actor.GetBounds())
        self.renderer.AddActor2D(self.text_actor)
        self.renderer.AddActor2D(self.text_actor1)
   
    def show(self):
        self.renderer.ResetCamera()
        self.renderWindowInteractor.AddObserver('MouseMoveEvent', self.update, 1.0)
        self.renderWindowInteractor.Initialize()
        self.renderWindow.Render()
        self.renderWindowInteractor.Start()

    def update(self,obj,ev):
        picker = vtkPropPicker ()
        picker.Pick(obj.GetEventPosition()[0],obj.GetEventPosition()[1], 0, obj.GetRenderWindow().GetRenderers().GetFirstRenderer())
        try:
            x = picker.GetActor().GetBounds()
            found = False
            name = None
            for atom in self.map.keys():
                if x in self.map[atom]:
                    found = True
                    name = atom
                    break
        
            if found :
                self.text_mapper.SetInput(name)
                
            else:
                self.text_mapper.SetInput('')
        except:
            self.text_mapper.SetInput('')
        self.renderWindowInteractor.GetRenderWindow().Render()


app = UI()
app.show()