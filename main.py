from menu import Menu

if __name__ == "__main__":
    agent = Menu()

    while agent.running:
        agent.get_action()

        
