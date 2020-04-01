start cmd /k "cd %__CD__%ui && docker-compose down && docker-compose build && docker-compose up"
start cmd /k "cd %__CD__%order_processing && docker-compose down && docker-compose build && docker-compose up"
start cmd /k "cd %__CD__%crm && docker-compose down && docker-compose build && docker-compose up"
start cmd /k "cd %__CD__%menu && docker-compose down && docker-compose build && docker-compose up"
start cmd /k "cd %__CD__%recommendation && docker-compose down && docker-compose build && docker-compose up"
start cmd /k "cd %__CD__%rabbitmq && docker-compose down && docker-compose build && docker-compose up"
start cmd /k "cd %__CD__%notification && docker-compose down && docker-compose build && docker-compose up"
start cmd /k "cd %__CD__%payment_facilitation && docker-compose down && docker-compose build && docker-compose up"

