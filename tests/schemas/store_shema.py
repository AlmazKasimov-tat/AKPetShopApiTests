STORE_SCHEMA = {
  "type": "object",
  "title": "Order",
  "description": "Схема тела запроса для создания заказа в Petstore API",
  "properties": {
    "id": {
      "type": "integer",
      "description": "Уникальный идентификатор заказа. При создании (POST) обычно генерируется сервером, поэтому поле необязательное.",
    },
    "petId": {
      "type": "integer",
      "description": "Идентификатор питомца, которого заказывают",
    },
    "quantity": {
      "type": "integer",
      "description": "Количество заказываемых питомцев",
    },
    "shipDate": {
      "type": "string",
      "format": "date-time",
      "description": "Дата и время отправки заказа в формате ISO 8601",
      "example": "2026-08-21T11:46:34.717Z"
    },
    "status": {
      "type": "string",
      "description": "Статус заказа",
      "enum": ["placed", "approved", "delivered"],
      "example": "approved"
    },
    "complete": {
      "type": "boolean",
      "description": "Флаг, указывающий, полностью ли выполнен заказ",
    }
  },
  "required": ["petId", "quantity"]
}

INVENTORY_SCHEMA = {
    "type": "object",
    "title": "Inventory Response",
    "description": "Ответ инвентаря: словарь, где ключи - строки (статусы заказов), а значения - целые числа (количество)",
    "additionalProperties": {
        "type": "integer"
    }
}