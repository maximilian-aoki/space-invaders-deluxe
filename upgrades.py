def upgrade_menu(score_board):
    print("\nALL THE SPACE INVADERS BASE ARE BELONG TO YOU.\nBut there will be more coming soon...\n")
    print("In the meantime, take a look at what we have in stock (QTY 1 each):\n")
    print(f"         Your Credits: {score_board}\n")
    print("           Ship Armor: 200    [Type 'a' to add to cart]")
    print("          Base Repair: 500    [Type 'r' to add to cart]")
    print("       SPECIAL DEVICE: 1000   [Type 'd' to add to cart]")

    next_round_items = order_output(score_board=score_board)

    return next_round_items


def order_output(score_board):
    order = input("\nWhat would you like to purchase? "
                  "(separate multiple orders by comma i.e. 'a,d', or skip with 'n'): ").lower().strip()

    checkout_output = {
        "score": score_board,
        "armor": [],
        "base_repair": "",
        "device": "",
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
        if "r" in order:
            checkout_output["base_repair"] = "Yes"
            order_confirm.append("r")
            cost += 500
        if "d" in order:
            checkout_output["device"] = "Armed..."
            order_confirm.append("d")
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

