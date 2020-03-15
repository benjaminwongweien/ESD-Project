Menu Microservice

To Start:

1:     CD <to this directory>
2:     RUN docker-compose up -d

To Stop:

1:     CD <to this directory>
2:     RUN docker-compose down   

To Access this service:
1:     http://localhost:86/bootstrap


Fake Test Card Details

***Visa***

4242 4242 4242 4242 Charge is successful.

These errors occur at stripe's side:
4000 0000 0000 0002 Charge is declined with a card_declined code.
4000 0000 0000 9995 Charge is declined with a card_declined code. The decline_code attribute is insufficient_funds.
4000 0000 0000 9987 Charge is declined with a card_declined code. The decline_code attribute is lost_card.
4000 0000 0000 9979 Charge is declined with a card_declined code. The decline_code attribute is stolen_card.
4000 0000 0000 0069 Charge is declined with an expired_card code.
4000 0000 0000 0127 Charge is declined with an incorrect_cvc code.
4000 0000 0000 0119 Charge is declined with a processing_error code.
4242 4242 4242 4241 Charge is declined with an incorrect_number code as the card number fails the Luhn check.

***Mastercard***
5555 5555 5555 4444 Charge is successful.