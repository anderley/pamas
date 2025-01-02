from django.db import models

class LogEntry(models.Model):
    app = models.CharField(max_length=100, default='pagamentos') 
    level = models.CharField(max_length=10)  # Nível do log (DEBUG, INFO, etc.)
    message = models.TextField()              # Mensagem do log
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora da criação

    def __str__(self):
        return f"{self.level} - {self.created_at}: {self.message}"
    

class Log:
    def __init__(self, app):
        self.app = app

    def info(self, message):
        LogEntry.objects.create(app=self.app, level='INFO', message=message)

    def debug(self, message):
        LogEntry.objects.create(app=self.app, level='DEBUG', message=message)

    def warning(self, message):
        LogEntry.objects.create(app=self.app, level='WARNING', message=message)

    def error(self, message):
        LogEntry.objects.create(app=self.app, level='ERROR', message=message)

    def critical(self, message):
        LogEntry.objects.create(app=self.app, level='CRITICAL', message=message)