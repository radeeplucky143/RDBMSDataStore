from abc import ABC, abstractmethod

class SQLConnection(ABC):
    """Abstract class representing a SQL connection."""

    @abstractmethod
    def connect(self):
        """Establishes a connection to the SQL database."""
        pass

    @abstractmethod
    def commit(self):
        """Commiting the changes done in the database"""
        pass

    @abstractmethod
    def disconnect(self):
        """Closes the connection to the SQL database."""
        pass
