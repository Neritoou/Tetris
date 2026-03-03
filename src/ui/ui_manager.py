from src.ui import UIElement

class UIManager:
    """Clase que se encarga de administrar todas las elementos de la UI disponibles."""
    def __init__(self) -> None:
        """Inicializa la lista de elementos de la UI."""
        self.elements: list[UIElement] = []

    def add_element(self, element: UIElement) -> None:
        """Agrega elementos de la UI a la lista siempre y cuando sean instancias de UIElement."""
        if not isinstance(element, UIElement):
            raise TypeError(f"UIManager: {element} no es un UIElement válido.")
        
        self.elements.append(element)

    def get_element(self, name: str) -> UIElement | None:
        """Busca un elemento por su nombre."""
        for element in self.elements:
            if element.name == name:
                return element
        return None
    
    def set_all_visible(self, visible: bool):
        for element in self.elements:
            element.visible = visible

    def render(self, surface) -> None:
        """Dibuja solo los elementos visibles."""
        for element in self.elements:
            if element.visible:
                element.render(surface)

    def update(self, dt: float) -> None:
        """Actualiza solo los elementos habilitados."""
        for element in self.elements:
            if element.visible:
                element.update(dt)

    def clear(self):
        self.elements = []