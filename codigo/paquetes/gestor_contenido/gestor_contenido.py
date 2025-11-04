"""
Gestor de Contenido
====================
Implementa la lógica de negocio para la gestión de contenidos.
"""

from typing import List
import sys
sys.path.append('..')
from modelos import Contenido, Texto, Imagen, Video, Objeto3D
from repositorios import RepositorioContenido


class GestorContenido:
    """
    Gestor de la lógica de negocio para contenidos.
    
    Attributes:
        repositorio: Repositorio de contenidos
    """
    
    def __init__(self, repositorio: RepositorioContenido):
        """
        Inicializa el gestor de contenido.
        
        Args:
            repositorio: Repositorio de contenidos a utilizar
        """
        self.repositorio = repositorio
    
    def crear_bloque_texto(self, cuerpo_texto: str, tema: str) -> Texto:
        """
        Crea un nuevo bloque de texto.
        
        Args:
            cuerpo_texto: Contenido del texto
            tema: Tema del contenido
            
        Returns:
            El objeto Texto creado y guardado
        """
        texto = Texto(cuerpo_texto=cuerpo_texto, tema=tema)
        return self.repositorio.guardar(texto)
    
    def crear_bloque_imagen(self, url_archivo: str, formato: str, tema: str) -> Imagen:
        """
        Crea un nuevo bloque de imagen.
        
        Args:
            url_archivo: URL o ruta del archivo de imagen
            formato: Formato de la imagen
            tema: Tema del contenido
            
        Returns:
            El objeto Imagen creado y guardado
        """
        imagen = Imagen(url_archivo=url_archivo, formato=formato, tema=tema)
        return self.repositorio.guardar(imagen)
    
    def crear_bloque_video(self, url_archivo: str, duracion: float, tema: str) -> Video:
        """
        Crea un nuevo bloque de video.
        
        Args:
            url_archivo: URL o ruta del archivo de video
            duracion: Duración del video en segundos
            tema: Tema del contenido
            
        Returns:
            El objeto Video creado y guardado
        """
        video = Video(url_archivo=url_archivo, duracion=duracion, tema=tema)
        return self.repositorio.guardar(video)
    
    def crear_bloque_objeto3D(self, url_archivo: str, formato: str, tema: str) -> Objeto3D:
        """
        Crea un nuevo bloque de objeto 3D.
        
        Args:
            url_archivo: URL o ruta del archivo del objeto 3D
            formato: Formato del objeto 3D
            tema: Tema del contenido
            
        Returns:
            El objeto Objeto3D creado y guardado
        """
        objeto3d = Objeto3D(url_archivo=url_archivo, formato=formato, tema=tema)
        return self.repositorio.guardar(objeto3d)
    
    def actualizar_bloque_texto(self, id_contenido: str, texto_nuevo: str, tema_nuevo: str) -> Texto:
        """
        Actualiza un bloque de texto existente.
        
        Args:
            id_contenido: ID del contenido a actualizar
            texto_nuevo: Nuevo contenido de texto
            tema_nuevo: Nuevo tema
            
        Returns:
            El objeto Texto actualizado
            
        Raises:
            ValueError: Si el contenido no existe o no es de tipo Texto
        """
        contenido = self.repositorio.buscar_por_id(id_contenido)
        if contenido is None:
            raise ValueError(f"No se encontró contenido con ID {id_contenido}")
        if not isinstance(contenido, Texto):
            raise ValueError(f"El contenido {id_contenido} no es de tipo Texto")
        
        contenido.cuerpo_texto = texto_nuevo
        contenido.tema = tema_nuevo
        return self.repositorio.guardar(contenido)
    
    def eliminar_contenido(self, id_contenido: str) -> None:
        """
        Elimina un contenido.
        
        Args:
            id_contenido: ID del contenido a eliminar
        """
        self.repositorio.eliminar(id_contenido)
    
    def obtener_contenido_por_id(self, id_contenido: str) -> Contenido:
        """
        Obtiene un contenido por su ID.
        
        Args:
            id_contenido: ID del contenido a buscar
            
        Returns:
            El contenido encontrado
            
        Raises:
            ValueError: Si el contenido no existe
        """
        contenido = self.repositorio.buscar_por_id(id_contenido)
        if contenido is None:
            raise ValueError(f"No se encontró contenido con ID {id_contenido}")
        return contenido
    
    def buscar_contenidos_por_tema(self, tema: str) -> List[Contenido]:
        """
        Busca contenidos por tema.
        
        Args:
            tema: Tema a buscar
            
        Returns:
            Lista de contenidos con ese tema
        """
        return self.repositorio.buscar_por_tema(tema)
