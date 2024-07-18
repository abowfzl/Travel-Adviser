import os
import uuid


class Session:
    def __init__(
            self,
            byte=16
    ) -> None:
        self.byte = byte
        self.session_id = ""

    def generate_session_id(self) -> uuid:
        self.session_id = uuid.UUID(bytes=os.urandom(self.byte))
        return self.session_id
