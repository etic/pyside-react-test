import inspect
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class Window:
    def render(self, child):
        app = QtWidgets.QApplication([])
        self.child = child
        self.widget = QtWidgets.QWidget()
        self.root = QtWidgets.QVBoxLayout(self.widget)
        self.refresh()
        self.widget.resize(800, 600)
        self.widget.show()
        sys.exit(app.exec())
        
    def refresh(self):
        self.child.window = self
        result = self.child.render()
        self.root.addLayout(result)
    
    def update(self):
        if self.child.dirty():
            self.refresh()
        else:
            self.child.update()

class BoxLayout:
    LeftToRight = QtWidgets.QBoxLayout.LeftToRight
    RightToLeft = QtWidgets.QBoxLayout.RightToLeft
    TopToBottom = QtWidgets.QBoxLayout.TopToBottom
    BottomToTop = QtWidgets.QBoxLayout.BottomToTop
    
    def __init__(self, *, direction=TopToBottom, children=None):
        self.direction = direction
        self.children = children
        self.window = None
        self.layout = None
    
    def delete(self):
        if self.layout:
            self.layout.deleteLater()
        for child in self.children:
            child.delete()
    
    def render(self):
        self.delete()
        self.layout = QtWidgets.QBoxLayout(self.direction)
        self.refresh()
        return self.layout
    
    def refresh(self):
        for child in self.children:
            child.delete()
        for child in self.children:
            child.parent = self.layout
            child.window = self.window
            result = child.render()
            if isinstance(result, QtWidgets.QLayout):
                self.layout.addLayout(result)
            elif isinstance(result, QtWidgets.QWidget):
                self.layout.addWidget(result)
    
    def dirty(self):
        return False
                
    def update(self):
        if any([x.dirty() for x in self.children]):
            self.refresh()
        else:
            for child in self.children:
                child.update()


class Label:
    def __init__(self, *, text=None):
        self.text = text
        self.window = None
        self.label = None
    
    def delete(self):
        if self.label:
            self.label.deleteLater()
    
    def render(self):
        self.delete()
        self.label = QtWidgets.QLabel(self.text)
        return self.label
    
    def dirty(self):
        return False
    
    def update(self):
        pass
            

class Button:
    def __init__(self, *, text=None, onClick=None):
        self.text = text
        self.onClick = onClick
        self.window = None
        self.button = None
    
    def delete(self):
        if self.button:
            self.button.deleteLater()
        
    def render(self):
        self.delete()
        self.button = QtWidgets.QPushButton(self.text)
        self.button.clicked.connect(self.buttonClicked)
        return self.button
    
    @QtCore.Slot()
    def buttonClicked(self):
        self.onClick()
        self.window.update()
        
    def dirty(self):
        return False
    
    def update(self):
        pass
        

def component(renderFunction):
    def buildComponent(*args, **kwargs):
        return _Component(renderFunction, *args, **kwargs)
    return buildComponent


class _Component:
    def __init__(self, renderFunction, *args, **kwargs):
        self.renderFunction = renderFunction
        self.rArgs = args
        self.rKwargs = kwargs
        self.state = []
        self.stateIndex = 0
        self.window = None
        self.child = None
        self.initialized = False
        
    def delete(self):
        if self.child:
            self.child.delete()

    def render(self):
        self.delete()
        self.child = self.renderFunction(*self.rArgs, **self.rKwargs)
        self.child.window = self.window
        result = self.child.render()
        
        self.stateIndex = 0
        for state in self.state:
            state.changed = False
        self.initialized = True
            
        return result

    def getNextState(self):
        index = self.stateIndex
        self.stateIndex += 1
        return self.state[index]
    
    def dirty(self):
        if any([x.changed for x in self.state]):
            return True
        return self.child.dirty()
    
    def update(self):
        self.child.update()
    

class _State:
    def __init__(self, defaultValue):
        self.value = defaultValue
        self.changed = False
    def setValue(self, value):
        if self.value != value:
            self.value = value
            self.changed = True


def useState(defaultValue):
    frame = inspect.currentframe()
    try:
        caller_frame = frame.f_back.f_back
        caller_self = caller_frame.f_locals.get('self', None)
        if not caller_self.initialized:
            state = _State(defaultValue)
            caller_self.state.append(state)
        else:
            state = caller_self.getNextState()
        return state.value, state.setValue
    finally:
        del frame
