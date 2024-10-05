from src.shared.errors import CardboardGenericException, ErrorCodes


class DiagramNotFoundError(CardboardGenericException):

    error_code = ErrorCodes.RESOURCE_NOT_FOUND.value
    error_message = "Diagram with this UID not found"


class NodeNotFoundError(CardboardGenericException):

    def __init__(self, node_class: str = "Node", *args, **kwargs):

        self.error_message = f"{node_class} with this UID not found"
        super().__init__(*args, **kwargs)

    error_code = ErrorCodes.RESOURCE_NOT_FOUND.value
    error_message = "Cluster with this UID not found"


class ResourceNotFoundError(CardboardGenericException):

    error_code = ErrorCodes.RESOURCE_NOT_FOUND.value
    error_message = "Resource with this UID not found"


class EdgeNotFoundError(CardboardGenericException):

    error_code = ErrorCodes.RESOURCE_NOT_FOUND.value
    error_message = "Edge with this UID not found"
