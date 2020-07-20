
import save
import account

BankAccount = account.BankAccount

if "bank" in save.state.keys():
    bank = save.state["bank"]
else:
    bank = {}

def get_account(owner_id):
    if owner_id in bank.keys():
        return bank[owner_id]
    else:
        bank[owner_id] = BankAccount()
        return bank[owner_id]

def save_bank():
    save.save_state("bank", bank)
