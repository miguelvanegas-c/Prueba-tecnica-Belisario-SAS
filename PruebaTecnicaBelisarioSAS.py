import datetime  

class ChatbotController:
    def __init__(self, db_connection):
        self.db = db_connection

    def procesar_mensaje(self, mensaje_data):
        # mensaje_data es un diccionario: {'usuario': 'andres', 'texto': 'Hola', 'tipo': 'mensaje'}
        usuario = mensaje_data.get('usuario')
        texto = mensaje_data.get('texto')
        esInterno = usuario and usuario.endswith('.loc')
        esError = texto and texto.startswith('[ERROR]')
        try:
            self.reglas_guardado(esInterno, esError, usuario, texto)
        except Exception as e:
            self.error_sistema(str(e), usuario)


    def reglas_guardado(self,esInterno, esError, usuario, texto):
        if esError:
                timestamp = datetime.datetime.now()
                self.db.execute(
                "INSERT INTO alertas_criticas (usuario, texto, timestamp) VALUES (%s, %s, %s)",
                (usuario, texto, timestamp)
                )
        else:
            if esInterno:
                self.db.execute(
                    "INSERT INTO historial_interno (usuario, texto) VALUES (%s, %s)",
                    (usuario, texto)
                )
            else:
                self.db.execute(
                    "INSERT INTO historial (usuario, texto) VALUES (%s, %s)",
                    (usuario, texto)
                )

    def error_sistema(self, mensaje_error, usuario):
        timestamp = datetime.datetime.now()
        self.db.execute(
            "INSERT INTO errores_sistema (mensaje_error, usuario, fecha) VALUES (%s, %s, %s)",
            (mensaje_error, usuario, timestamp)
        )