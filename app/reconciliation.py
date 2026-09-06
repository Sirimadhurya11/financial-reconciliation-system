from datetime import timedelta


def reconcile_transactions(
    bank_transaction,
    payment_transaction
):
    differences = []

    # Compare amount
    if bank_transaction.amount != payment_transaction.amount:
        differences.append("amount")

    # Compare currency
    if bank_transaction.currency != payment_transaction.currency:
        differences.append("currency")

    # Compare status
    if bank_transaction.status != payment_transaction.status:
        differences.append("status")

    # Compare transaction time
    time_difference = abs(
        bank_transaction.transaction_time
        - payment_transaction.transaction_time
    )

    if time_difference > timedelta(minutes=5):
        differences.append("transaction_time")

    # Return reconciliation result
    if differences:
        return {
            "transaction_id": bank_transaction.transaction_id,
            "status": "MISMATCH",
            "differences": differences
        }

    return {
        "transaction_id": bank_transaction.transaction_id,
        "status": "MATCHED",
        "differences": []
    }


def check_transaction_presence(transactions):
    sources = {
        transaction.source
        for transaction in transactions
    }

    has_bank = "bank" in sources
    has_payment_system = "payment_system" in sources

    if has_bank and has_payment_system:
        return {
            "status": "READY",
            "message": "Both transaction records are available"
        }

    if has_bank:
        return {
            "status": "MISSING_PAYMENT",
            "message": "Payment-system transaction is missing"
        }

    if has_payment_system:
        return {
            "status": "MISSING_BANK",
            "message": "Bank transaction is missing"
        }

    return {
        "status": "NOT_FOUND",
        "message": "No transaction records found"
    }