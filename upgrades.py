def upgrade_menu(score_board):
    print("\nALL THE SPACE INVADERS BASE ARE BELONG TO YOU.\nBut there will be more coming soon...\n")
    print("In the meantime, take a look at what we have in stock (QTY 1 each):\n")
    print(f"         Your Credits: {score_board}\n")
    print("           Ship Armor: 200    [Type 'a' to add to cart]")
    print("          Machine Gun: 500    [Type 'b' to add to cart]")
    print("       SPECIAL DEVICE: 1000   [Type 'c' to add to cart]")

    next_round_items = order_output(score_board=score_board)

    print(f"\nYou have {next_round_items['score']} credits remaining.")

    input("\nHit [RETURN] to start next round:")

    print("\nNEXT ROUND STARTED")

    return next_round_items


def order_output(score_board):
    order = input("\nWhat would you like to purchase? "
                  "(separate multiple orders by comma i.e. 'a,b', or skip with 'n'): ").lower().strip()

    checkout_output = {
        "score": score_board,
        "armor": [],
        "fire_rate": None,
        "device": False,
    }

    cost = 0
    if order == "n":
        return checkout_output

    else:
        order_confirm = []
        if "a" in order:
            checkout_output["armor"] = ["⛊", "⛊"]
            order_confirm.append("a")
            cost += 200
        if "b" in order:
            checkout_output["fire_rate"] = -300
            order_confirm.append("b")
            cost += 500
        if "c" in order:
            checkout_output["device"] = True
            order_confirm.append("c")
            cost += 1000

        if score_board >= cost:
            confirm = input(f"\nPlease confirm your purchase of {order_confirm} for {cost} credits "
                            f"('y' for Yes, anything else for No): ").lower().strip()
            if confirm == "y":
                checkout_output["score"] = score_board - cost
                return checkout_output
            else:
                return order_output(score_board)
        else:
            print("\nSorry, you do not have sufficient credits for your purchase!")
            return order_output(score_board)

